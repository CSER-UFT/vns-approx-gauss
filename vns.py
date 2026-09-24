"""
VNS (Variable Neighborhood Search) aplicado ao DSE de multiplicadores aproximados
no filtro Gaussiano.

Fluxo (conforme o fluxograma):
    Biblioteca de multiplicadores pré-caracterizada (metrics_all.csv)
        -> Parametrização do filtro (cada multiplicador do filtro é uma "posição" de x)
        -> Execução do VNS  (Perturbação -> Busca Local -> Mudar Vizinhança)
        -> Validação        (solução final comparada com a imagem de referência)

Formulação:
    minimizar  R(x) = sum_i (LUT_{x_i} + FF_{x_i})
    sujeito a  SSIM(filtro_x(img), filtro_exato(img)) >= T

Onde x é um vetor com uma entrada por multiplicador do filtro; cada entrada é o
índice de um componente da biblioteca. A solução inicial usa apenas o
multiplicador exato.

Modos de parametrização do filtro (--mode):
    direct    : 1 multiplicador por tap não nulo do kernel 2D (ex.: 3x3 -> 9)
    symmetry  : 1 multiplicador por peso único (taps de mesmo peso compartilham)
    separable : 1 multiplicador por tap não nulo de cada passe 1D (H + V)

Uso:
    python vns.py --image foto.png --threshold 0.95 --time 30 --kmax 4 --seed 42
"""

import argparse
import csv
import os
import random
import time
from dataclasses import dataclass, field
from typing import Callable, Dict, Iterator, List, Optional, Tuple

import numpy as np
from PIL import Image

from evaluate import create_synthetic_test_image, load_hardware_metrics
from gaussian_filter import (
    apply_gaussian_filter,
    apply_gaussian_filter_separable,
    get_gaussian_kernel,
    get_gaussian_kernel_1d,
    group_kernel_by_weight,
)
from metrics import evaluate_image_errors
from multipliers import get_multiplier

Solution = Tuple[int, ...]  # x[i] = índice do componente da biblioteca na posição i


# ===========================================================================
# Biblioteca de componentes
# ===========================================================================

@dataclass(frozen=True)
class Component:
    name: str
    fn: Callable[[np.ndarray, np.ndarray], np.ndarray]
    lut: int
    ff: int
    dsp: int

    @property
    def cost(self) -> int:
        """Custo de hardware do componente: LUT + FF (como em Avaliar(x))."""
        return self.lut + self.ff

    @property
    def is_exact(self) -> bool:
        n = self.name.lower()
        return "exato" in n or "exact" in n


def build_library(csv_path: str) -> List[Component]:
    """Monta a biblioteca a partir do metrics_all.csv, mantendo apenas os
    multiplicadores que possuem modelo Python em multipliers.py."""
    library: List[Component] = []
    for e in load_hardware_metrics(csv_path):
        try:
            fn = get_multiplier(e["Multiplier"])
        except ValueError:
            print(f"[biblioteca] ignorando {e['Multiplier']}: sem modelo Python.")
            continue
        library.append(Component(e["Multiplier"], fn, e["LUT"], e["FF"], e["DSP"]))

    if not any(c.is_exact for c in library):
        raise RuntimeError("A biblioteca precisa conter o multiplicador exato (multExato).")
    if len(library) < 2:
        raise RuntimeError("A biblioteca precisa ter pelo menos 2 componentes.")
    return library


# ===========================================================================
# Problema de DSE: parametriza o filtro e avalia uma solução x
# ===========================================================================

class _SlotDispatcher:
    """Faz o filtro existente (gaussian_filter.py) usar um multiplicador
    DIFERENTE por posição.

    Os filtros chamam multiplier_fn uma vez por multiplicador físico, sempre na
    mesma ordem (varredura row-major dos taps não nulos; ou grupos de peso na
    ordem de group_kernel_by_weight; ou passe H seguido do passe V). O
    dispatcher devolve a i-ésima função da lista na i-ésima chamada.
    """

    def __init__(self, fns: List[Callable]):
        self.fns = fns
        self.calls = 0

    def __call__(self, a, b):
        fn = self.fns[self.calls % len(self.fns)]
        self.calls += 1
        return fn(a, b)


class DSEProblem:
    def __init__(
        self,
        image: np.ndarray,
        library: List[Component],
        mode: str = "direct",
        kernel_size: int = 3,
        sigma: float = 1.0,
        sep_scale: Optional[int] = None,
        threshold: float = 0.95,
    ):
        if mode not in ("direct", "symmetry", "separable"):
            raise ValueError(f"Modo inválido: {mode}")
        self.image = image
        self.library = library
        self.mode = mode
        self.threshold = threshold

        # Mesmos kernels usados em evaluate.py
        self.kernel, self.norm = get_gaussian_kernel(size=kernel_size, sigma=sigma)
        self.kernel_1d, self.norm_1d = get_gaussian_kernel_1d(
            size=kernel_size, sigma=sigma, scale_to_sum=sep_scale
        )

        # Imagem de referência: filtro 2D com multiplicador exato
        self.reference = apply_gaussian_filter(
            image, get_multiplier("multExato"), kernel=self.kernel, norm_factor=self.norm
        )

        self.exact_idx = next(i for i, c in enumerate(library) if c.is_exact)
        self.slot_labels = self._build_slot_labels()
        self.n_slots = len(self.slot_labels)

        self._cache: Dict[Solution, Tuple[int, float]] = {}
        self.n_evals = 0  # avaliações reais (cache misses)

    # -- parametrização ------------------------------------------------------
    def _build_slot_labels(self) -> List[str]:
        if self.mode == "direct":
            k_h, k_w = self.kernel.shape
            return [
                f"tap({r},{c}) w={int(self.kernel[r, c])}"
                for r in range(k_h) for c in range(k_w) if self.kernel[r, c] != 0
            ]
        if self.mode == "symmetry":
            return [
                f"w={w} ({len(offs)} taps)"
                for w, offs in group_kernel_by_weight(self.kernel).items()
            ]
        taps = [(i, int(w)) for i, w in enumerate(self.kernel_1d) if w != 0]
        return [f"H[{i}] w={w}" for i, w in taps] + [f"V[{i}] w={w}" for i, w in taps]

    def initial_solution(self) -> Solution:
        """Solução inicial: apenas multiplicadores exatos."""
        return tuple([self.exact_idx] * self.n_slots)

    # -- avaliação -----------------------------------------------------------
    def cost(self, x: Solution) -> int:
        return sum(self.library[i].cost for i in x)

    def render(self, x: Solution) -> np.ndarray:
        """Executa o filtro parametrizado com a configuração x."""
        disp = _SlotDispatcher([self.library[i].fn for i in x])
        if self.mode == "direct":
            out = apply_gaussian_filter(
                self.image, disp, kernel=self.kernel, norm_factor=self.norm
            )
        elif self.mode == "symmetry":
            out = apply_gaussian_filter(
                self.image, disp, kernel=self.kernel, norm_factor=self.norm,
                exploit_symmetry=True,
            )
        else:
            out = apply_gaussian_filter_separable(
                self.image, disp, kernel_1d=self.kernel_1d, norm_factor=self.norm_1d
            )
        # Garante que a ordem/quantidade de chamadas bate com as posições de x
        assert disp.calls == self.n_slots, (
            f"O filtro chamou {disp.calls} multiplicadores, mas x tem {self.n_slots} posições."
        )
        return out

    def evaluate(self, x: Solution) -> Tuple[int, float]:
        """Avaliar(x): devolve (R(x), SSIM). Resultados são memorizados."""
        if x not in self._cache:
            self.n_evals += 1
            img = self.render(x)
            ssim = float(evaluate_image_errors(self.reference, img)["SSIM"])
            self._cache[x] = (self.cost(x), ssim)
        return self._cache[x]

    def is_feasible(self, ssim: float) -> bool:
        return ssim >= self.threshold

    def is_better(self, R_a: float, s_a: float, R_b: float, s_b: float) -> bool:
        """a é melhor que b? Viável sempre vence inviável; entre viáveis vence o
        menor custo; entre inviáveis vence o maior SSIM (reparo)."""
        fa, fb = self.is_feasible(s_a), self.is_feasible(s_b)
        if fa and fb:
            return R_a < R_b
        if fa != fb:
            return fa
        return s_a > s_b

    def describe(self, x: Solution) -> List[Dict]:
        return [
            {
                "Posicao": self.slot_labels[i],
                "Multiplicador": self.library[j].name,
                "LUT": self.library[j].lut,
                "FF": self.library[j].ff,
                "DSP": self.library[j].dsp,
            }
            for i, j in enumerate(x)
        ]


# ===========================================================================
# Componentes do VNS
# ===========================================================================

def perturbation_dse(problem: DSEProblem, x: Solution, k: int, rng: random.Random) -> Solution:
    """PerturbaçãoDSE(x, k): troca k multiplicadores (posições distintas,
    sorteadas) por outro componente da biblioteca, também sorteado."""
    n_lib = len(problem.library)
    new = list(x)
    for pos in rng.sample(range(problem.n_slots), k):
        new[pos] = rng.choice([j for j in range(n_lib) if j != x[pos]])
    return tuple(new)


def neighbors_n1(problem: DSEProblem, x: Solution) -> Iterator[Solution]:
    """N_1(x): todas as soluções obtidas removendo 1 multiplicador e inserindo
    1 componente diferente da biblioteca."""
    for pos in range(problem.n_slots):
        for j in range(len(problem.library)):
            if j != x[pos]:
                yield x[:pos] + (j,) + x[pos + 1:]


def local_search_dse(problem: DSEProblem, x: Solution, descent: bool = True) -> Solution:
    """BuscaLocalDSE(x): varre N_1(x) e fica com o melhor vizinho que respeita
    SSIM >= T e reduz R. Com descent=True repete a varredura a partir do novo
    ponto até não haver melhoria (ótimo local em N_1); com False faz uma única
    varredura, como no pseudocódigo do artigo."""
    x_best = x
    R_best, s_best = problem.evaluate(x_best)
    while True:
        center = x_best
        improved = False
        for y in neighbors_n1(problem, center):
            R_y, s_y = problem.evaluate(y)
            if problem.is_better(R_y, s_y, R_best, s_best):
                x_best, R_best, s_best = y, R_y, s_y
                improved = True
        if not (improved and descent):
            return x_best


def change_neighborhood_dse(
    problem: DSEProblem, x: Solution, x_new: Solution, k: int
) -> Tuple[Solution, int]:
    """MudarVizinhançaDSE: aceita x_new se SSIM >= T e R menor que o de x
    (volta a k=1); caso contrário, k <- k+1."""
    R_x, _ = problem.evaluate(x)
    R_n, s_n = problem.evaluate(x_new)
    if problem.is_feasible(s_n) and R_n < R_x:
        return x_new, 1
    return x, k + 1


@dataclass
class VNSResult:
    x: Solution
    cost: int
    ssim: float
    elapsed: float
    iterations: int
    evaluations: int
    history: List[Dict] = field(default_factory=list)  # cada melhoria encontrada


def vns(
    problem: DSEProblem,
    t_max: float = 30.0,
    k_max: int = 4,
    seed: Optional[int] = None,
    descent: bool = True,
    verbose: bool = True,
) -> VNSResult:
    """Algoritmo principal (VNS para seleção de multiplicadores)."""
    rng = random.Random(seed)
    k_max = max(1, min(k_max, problem.n_slots))

    x = problem.initial_solution()
    R, s = problem.evaluate(x)
    history = [{"time_s": 0.0, "evals": problem.n_evals, "cost": R, "ssim": s, "k": 0}]
    if verbose:
        print(f"[VNS] inicial (todos exatos): R={R}  SSIM={s:.4f}  "
              f"posições={problem.n_slots}  biblioteca={len(problem.library)}  T={problem.threshold}")

    t0 = time.process_time()
    elapsed = lambda: time.process_time() - t0  # CpuTime()
    iterations = 0

    while elapsed() < t_max:
        k = 1
        while k <= k_max and elapsed() < t_max:
            x1 = perturbation_dse(problem, x, k, rng)
            x2 = local_search_dse(problem, x1, descent)
            x_new, k_new = change_neighborhood_dse(problem, x, x2, k)
            iterations += 1

            if x_new != x:
                R, s = problem.evaluate(x_new)
                history.append({"time_s": elapsed(), "evals": problem.n_evals,
                                "cost": R, "ssim": s, "k": k})
                if verbose:
                    print(f"[VNS] t={elapsed():6.2f}s  k={k}  nova melhor: "
                          f"R={R}  SSIM={s:.4f}  (avaliações={problem.n_evals})")
            x, k = x_new, k_new

    R, s = problem.evaluate(x)
    return VNSResult(x, R, s, elapsed(), iterations, problem.n_evals, history)


# ===========================================================================
# Validação e relatórios
# ===========================================================================

def validate(problem: DSEProblem, result: VNSResult, output_dir: str) -> List[Dict]:
    """Valida a solução do VNS contra a imagem de referência e a compara com a
    referência exata e com todas as configurações uniformes (mesmo componente
    em todas as posições)."""
    R_exact = problem.cost(problem.initial_solution())

    def make_row(label: str, x: Solution) -> Dict:
        m = evaluate_image_errors(problem.reference, problem.render(x))
        R = problem.cost(x)
        return {
            "Configuracao": label,
            "LUT+FF": R,
            "Economia (%)": round((R_exact - R) / R_exact * 100.0, 2) if R_exact else 0.0,
            "SSIM": m["SSIM"],
            "PSNR (dB)": m["PSNR (dB)"],
            "MAE": m["MAE"],
            "Max Error": m["Max Error"],
            "Viavel": problem.is_feasible(m["SSIM"]),
        }

    rows = [make_row(f"uniforme: {c.name}", tuple([i] * problem.n_slots))
            for i, c in enumerate(problem.library)]
    rows.append(make_row("VNS (solução final)", result.x))
    rows.sort(key=lambda r: (r["LUT+FF"], -float(r["SSIM"])))

    fmt = "{:<30} | {:>7} | {:>9} | {:>7} | {:>10} | {:>7} | {:>7} | {:>6}"
    line = "=" * 102
    print("\n" + line)
    print(f"VALIDAÇÃO  (T = {problem.threshold}, modo = {problem.mode})")
    print(line)
    print(fmt.format("Configuração", "LUT+FF", "Economia", "SSIM", "PSNR (dB)", "MAE", "MaxErr", "Viável"))
    print("-" * 102)
    for r in rows:
        psnr = "inf" if r["PSNR (dB)"] == float("inf") else f"{r['PSNR (dB)']:.2f}"
        mark = "  <== VNS" if r["Configuracao"].startswith("VNS") else ""
        print(fmt.format(r["Configuracao"], r["LUT+FF"], f"{r['Economia (%)']:.1f}%",
                         f"{r['SSIM']:.4f}", psnr, f"{r['MAE']:.3f}", r["Max Error"],
                         "sim" if r["Viavel"] else "não") + mark)
    print(line + "\n")

    with open(os.path.join(output_dir, "vns_validation.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    return rows


def save_outputs(problem: DSEProblem, result: VNSResult, output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)

    Image.fromarray(problem.reference).save(os.path.join(output_dir, "filtered_reference.png"))
    Image.fromarray(problem.render(result.x)).save(os.path.join(output_dir, "filtered_vns.png"))

    rows = problem.describe(result.x)
    with open(os.path.join(output_dir, "vns_solution.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    with open(os.path.join(output_dir, "vns_history.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(result.history[0].keys()))
        w.writeheader()
        w.writerows(result.history)

    try:
        import matplotlib.pyplot as plt
        t = [h["time_s"] for h in result.history] + [result.elapsed]
        c = [h["cost"] for h in result.history] + [result.history[-1]["cost"]]
        plt.figure(figsize=(7, 4))
        plt.step(t, c, where="post", color="royalblue")
        plt.scatter(t[:-1], c[:-1], color="royalblue", zorder=3)
        plt.xlabel("Tempo de CPU (s)")
        plt.ylabel("Custo R(x) = LUT + FF")
        plt.title("Convergência do VNS")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "vns_convergence.png"), dpi=200)
        plt.close()
    except Exception as e:  # o gráfico é opcional
        print(f"[aviso] gráfico de convergência não gerado: {e}")


def main():
    p = argparse.ArgumentParser(description="VNS para DSE de multiplicadores aproximados (filtro Gaussiano)")
    p.add_argument("--image", "-i", default=None, help="Imagem de entrada (default: padrão sintético)")
    p.add_argument("--csv", "-c", default="metrics_all.csv", help="metrics_all.csv da síntese HLS")
    p.add_argument("--output", "-o", default="output/vns", help="Diretório de saída")
    p.add_argument("--kernel-size", "-k", type=int, default=3, choices=[3, 5, 7])
    p.add_argument("--sigma", "-s", type=float, default=1.0)
    p.add_argument("--mode", choices=["direct", "symmetry", "separable"], default="direct",
                   help="Parametrização do filtro (default: direct)")
    p.add_argument("--sep-scale", type=int, default=None, choices=[16, 64, 256],
                   help="Soma dos pesos 1D no modo separable")
    p.add_argument("--threshold", "-T", type=float, default=0.95, help="Limiar mínimo de SSIM (default: 0.95)")
    p.add_argument("--time", "-t", type=float, default=30.0, help="Tempo máximo de CPU em segundos (default: 30)")
    p.add_argument("--kmax", type=int, default=4, help="Número máximo de vizinhanças (default: 4)")
    p.add_argument("--seed", type=int, default=None, help="Semente aleatória (reprodutibilidade)")
    p.add_argument("--single-sweep", action="store_true",
                   help="Busca local com uma única varredura (como no pseudocódigo do artigo)")
    args = p.parse_args()

    # Imagem de entrada
    if args.image and os.path.exists(args.image):
        img = np.array(Image.open(args.image).convert("L"), dtype=np.uint8)
        print(f"Imagem '{args.image}' carregada ({img.shape[1]}x{img.shape[0]})")
    else:
        img = create_synthetic_test_image(256, 256)
        print("Usando padrão sintético 256x256")

    library = build_library(args.csv)
    print("Biblioteca:", ", ".join(f"{c.name}({c.cost})" for c in library))

    problem = DSEProblem(img, library, mode=args.mode, kernel_size=args.kernel_size,
                         sigma=args.sigma, sep_scale=args.sep_scale, threshold=args.threshold)

    result = vns(problem, t_max=args.time, k_max=args.kmax, seed=args.seed,
                 descent=not args.single_sweep)

    print(f"\n[VNS] fim: {result.iterations} iterações, {result.evaluations} avaliações, "
          f"{result.elapsed:.2f}s de CPU")
    print(f"[VNS] melhor solução: R={result.cost}  SSIM={result.ssim:.4f}")
    for row in problem.describe(result.x):
        print(f"    {row['Posicao']:<22} -> {row['Multiplicador']}")

    save_outputs(problem, result, args.output)
    validate(problem, result, args.output)
    print(f"Arquivos salvos em {args.output}/")


if __name__ == "__main__":
    main()