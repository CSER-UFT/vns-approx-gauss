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

Parametrização: 1 multiplicador por tap não nulo do kernel 2D (ex.: 3x3 -> 9).

O VNS é executado em loop sobre uma sequência de limiares de SSIM
(padrão: T = 0.95, 0.90, ..., 0.70).

Execução em DUAS FASES sobre um dataset (padrão: 100 imagens):
    1. TREINO    (imagens 1..70)   -> o VNS otimiza R(x) com a restrição
                                      SSIM_médio(treino) >= T. A SSIM usada em
                                      Avaliar(x) é a MÉDIA sobre todas as imagens de treino.
    2. VALIDAÇÃO (imagens 71..100) -> a configuração final de cada T
                                      (vns_solution_Txx) é aplicada às imagens
                                      restantes e o desempenho médio é reportado.

As imagens são ordenadas por nome em ordem NATURAL (img2 < img10), então
"imagem 1" é a primeira do diretório e "imagem 100" a última.

Uso:
    python vns2.py --dataset imagens/ --train-count 70 --total 100 \
                   --t-start 95 --t-end 70 --t-step 5 --max-evals 500 --kmax 4 --seed 42

    # Paralelismo: --threads N (ou -w N). Sem valor ou omitido usa todas as threads da CPU.
    # Orçamento: --max-evals N = nº máximo de avaliações REAIS (cache misses) POR limiar.
    # --time S (opcional) é apenas um teto de segurança em tempo de relógio (wall-clock); vale o que ocorrer primeiro.
    # --patience P (opcional) interrompe o limiar após P avaliações reais sem melhoria do melhor viável.

    # Só validar soluções já geradas (lê output/vns/vns_solution_Txx.csv):
    python vns2.py --dataset imagens/ --validate-only
"""

import argparse
import csv
import os
import random
import re
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field
from typing import Callable, Dict, Iterator, List, Optional, Tuple

import matplotlib
matplotlib.use("Agg")
import numpy as np
from PIL import Image

from evaluate import create_synthetic_test_image, load_hardware_metrics
from gaussian_filter import apply_gaussian_filter, get_gaussian_kernel
from metrics import (calc_error_rate, calc_mae, calc_max_error, calc_mse,
                     calc_psnr, calc_ssim)
from multipliers import get_multiplier

Solution = Tuple[int, ...]  # x[i] = índice do componente da biblioteca na posição i


# ===========================================================================
# Dataset: carga, ordenação e divisão treino / validação
# ===========================================================================

IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp", ".pgm", ".ppm")


def _natural_key(name: str):
    """'img10.png' > 'img2.png' (ordem natural, não lexicográfica)."""
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", name)]


def load_dataset(path: str, total: int) -> List[Tuple[str, np.ndarray]]:
    """Carrega as primeiras `total` imagens do diretório (ordem natural) em tons de cinza."""
    files = sorted(
        (f for f in os.listdir(path) if f.lower().endswith(IMAGE_EXTS)),
        key=_natural_key,
    )
    if len(files) < total:
        raise RuntimeError(f"O dataset tem {len(files)} imagens, mas --total={total}.")
    files = files[:total]
    return [(f, np.array(Image.open(os.path.join(path, f)).convert("L"), dtype=np.uint8))
            for f in files]


def create_synthetic_dataset(total: int, seed: int = 0, size: int = 128) -> List[Tuple[str, np.ndarray]]:
    """Dataset sintético (apenas para testar o fluxo quando --dataset não é dado):
    padrões variados (gradiente + círculos + xadrez + ruído) com parâmetros aleatórios."""
    rng = np.random.RandomState(seed)
    y, x = np.mgrid[0:size, 0:size]
    out = []
    for n in range(1, total + 1):
        gx, gy = rng.uniform(0, 1.2, 2)
        cx, cy = rng.uniform(0.2, 0.8, 2) * size
        period = rng.uniform(3.0, 10.0)
        cell = int(rng.choice([4, 8, 16]))
        noise = rng.uniform(0, 25)
        img = (gx * x + gy * y) / size * 120.0
        img += np.sin(np.hypot(x - cx, y - cy) / period) * 45.0 + 45.0
        img += (((x // cell) + (y // cell)) % 2) * rng.uniform(10, 60)
        img += rng.normal(0, noise, img.shape)
        img = np.clip(img, 0, 255)
        out.append((f"synthetic_{n:03d}.png", img.astype(np.uint8)))
    return out


def split_dataset(data: List, train_count: int) -> Tuple[List, List]:
    """Imagens 1..train_count -> treino; train_count+1..fim -> validação."""
    if not 0 < train_count < len(data):
        raise ValueError("--train-count deve estar entre 1 e (total - 1).")
    return data[:train_count], data[train_count:]


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
    DIFERENTE por posição do kernel.

    CONTRATO / PREMISSA:
    Assume que `apply_gaussian_filter` varre o kernel 2D em ordem row-major
    (linha por linha, da esquerda para a direita) e invoca a função multiplicadora
    exatamente uma vez por tap não nulo para a imagem completa.
    O dispatcher devolve a i-ésima função da lista na i-ésima chamada.
    """

    def __init__(self, fns: List[Callable]):
        self.fns = fns
        self.calls = 0

    def __call__(self, a, b):
        fn = self.fns[self.calls % len(self.fns)]
        self.calls += 1
        return fn(a, b)


# Estado global nos processos workers do ProcessPoolExecutor.
# Carregado apenas uma vez via _init_worker na inicialização de cada worker do pool,
# eliminando a serialização e transmissão IPC de imagens a cada avaliação.
_WORKER_IMAGES: List[np.ndarray] = []
_WORKER_REFERENCES: List[np.ndarray] = []
_WORKER_KERNEL: Optional[np.ndarray] = None
_WORKER_NORM: Optional[int] = None


def _init_worker(
    images: List[np.ndarray],
    references: List[np.ndarray],
    kernel: np.ndarray,
    norm: int,
) -> None:
    """Inicializador do processo worker: armazena imagens e referências imutáveis
    na memória local do processo filho."""
    global _WORKER_IMAGES, _WORKER_REFERENCES, _WORKER_KERNEL, _WORKER_NORM
    _WORKER_IMAGES = images
    _WORKER_REFERENCES = references
    _WORKER_KERNEL = kernel
    _WORKER_NORM = norm


def _eval_one_image(item: Tuple[int, Tuple[str, ...]]) -> float:
    """Aplica o filtro e calcula a SSIM de UMA imagem no processo worker.
    Recebe apenas (img_idx, mult_names), lendo os arrays pesados da memória local."""
    img_idx, mult_names = item
    img = _WORKER_IMAGES[img_idx]
    ref = _WORKER_REFERENCES[img_idx]
    from multipliers import get_multiplier
    from gaussian_filter import apply_gaussian_filter
    from metrics import calc_ssim as _calc_ssim
    fns = [get_multiplier(name) for name in mult_names]
    disp = _SlotDispatcher(fns)
    out = apply_gaussian_filter(img, disp, kernel=_WORKER_KERNEL, norm_factor=_WORKER_NORM)
    return float(_calc_ssim(ref, out))


def aggregate_ssim(vals: List[float], mode: str = "mean") -> float:
    """Agrega os valores de SSIM de acordo com o modo escolhido:
    - 'mean': média aritmética simples.
    - 'geomean': média geométrica exp(mean(log(ssim_i))), com proteção ssim_i <= 0.
    - 'median': mediana dos valores.
    """
    arr = np.asarray(vals, dtype=np.float64)
    if mode == "geomean":
        clipped = np.clip(arr, 1e-12, 1.0)
        return float(np.exp(np.mean(np.log(clipped))))
    elif mode == "median":
        return float(np.median(arr))
    elif mode == "mean":
        return float(np.mean(arr))
    else:
        raise ValueError(f"Modo de agregação de SSIM desconhecido: '{mode}'. Opções: 'mean', 'geomean', 'median'.")


class DSEProblem:
    """Problema de DSE sobre um CONJUNTO de imagens.

    Avaliar(x) devolve (R(x), SSIM_agregada): a SSIM de cada imagem é calculada contra
    a respectiva referência (filtro exato) e agregada conforme ssim_agg.
    """

    def __init__(
        self,
        images: List[np.ndarray],
        library: List[Component],
        kernel_size: int = 3,
        sigma: float = 1.0,
        threshold: float = 0.95,
        names: Optional[List[str]] = None,
        reference_images: Optional[List[np.ndarray]] = None,
        ssim_agg: str = "mean",
        patience: Optional[int] = 100,
        max_workers: Optional[int] = None,
    ):
        if isinstance(images, np.ndarray):  # compatibilidade: imagem única
            images = [images]
        self.images = list(images)
        self.names = names or [f"img{i + 1}" for i in range(len(self.images))]
        self.library = library
        self.threshold = threshold
        self.ssim_agg = ssim_agg
        self.patience = patience
        self.max_workers = max_workers if max_workers is not None else (os.cpu_count() or 1)
        self._evals_since_improvement = 0

        # Mesmo kernel usado em evaluate.py
        self.kernel, self.norm = get_gaussian_kernel(size=kernel_size, sigma=sigma)

        # Imagens de referência: reutiliza pré-computadas (se passadas) ou calcula
        if reference_images is not None:
            if len(reference_images) != len(self.images):
                raise ValueError(
                    f"reference_images tem {len(reference_images)} imagens, mas images tem {len(self.images)}."
                )
            self.references = list(reference_images)
        else:
            exact_fn = get_multiplier("multExato")
            self.references = [
                apply_gaussian_filter(im, exact_fn, kernel=self.kernel, norm_factor=self.norm)
                for im in self.images
            ]

        self.exact_idx = next(i for i, c in enumerate(library) if c.is_exact)
        self.slot_labels = self._build_slot_labels()
        self.n_slots = len(self.slot_labels)

        self._cache: Dict[Solution, Tuple[int, float]] = {}
        self.n_evals = 0  # avaliações reais (cache misses)

        # Trajetória de convergência e melhor solução viável encontrada
        self.trace: List[Dict] = []
        self.best_cost: Optional[int] = None
        self.best_solution: Optional[Solution] = None
        self.best_ssim: Optional[float] = None
        self.t0: float = time.perf_counter()
        self.current_k: int = 0
        # Orçamento da execução atual (definido em vns()):
        self.max_evals: Optional[int] = None   # máx. de avaliações reais (cache misses)
        self.deadline: Optional[float] = None  # teto opcional de tempo wall-clock (perf_counter)

        # Pool de processos reutilizável durante todo o ciclo de vida deste problema
        self._pool: Optional[ProcessPoolExecutor] = ProcessPoolExecutor(
            max_workers=self.max_workers,
            initializer=_init_worker,
            initargs=(self.images, self.references, self.kernel, self.norm),
        )

    def close(self) -> None:
        """Encerra o pool de processos worker e desaloca seus recursos."""
        if self._pool is not None:
            self._pool.shutdown(wait=True)
            self._pool = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    # -- parametrização ------------------------------------------------------
    def _build_slot_labels(self) -> List[str]:
        """Gera os rótulos de cada tap não nulo do kernel em ordem row-major.
        Essa ordem corresponde exatamente à sequência de chamadas feitas por
        apply_gaussian_filter através do _SlotDispatcher.
        """
        k_h, k_w = self.kernel.shape
        return [
            f"tap({r},{c}) w={int(self.kernel[r, c])}"
            for r in range(k_h) for c in range(k_w) if self.kernel[r, c] != 0
        ]

    def initial_solution(self) -> Solution:
        """Solução inicial: apenas multiplicadores exatos."""
        return tuple([self.exact_idx] * self.n_slots)

    # -- avaliação -----------------------------------------------------------
    def cost(self, x: Solution) -> int:
        return sum(self.library[i].cost for i in x)

    def render(self, x: Solution, idx: int = 0) -> np.ndarray:
        """Executa o filtro parametrizado com a configuração x na imagem `idx`."""
        disp = _SlotDispatcher([self.library[i].fn for i in x])
        out = apply_gaussian_filter(
            self.images[idx], disp, kernel=self.kernel, norm_factor=self.norm
        )
        # Garante que a ordem/quantidade de chamadas bate com as posições de x
        assert disp.calls == self.n_slots, (
            f"O filtro chamou {disp.calls} multiplicadores, mas x tem {self.n_slots} posições."
        )
        return out

    def aggregate_ssim(self, vals: List[float]) -> float:
        """Agrega a lista de valores de SSIM conforme self.ssim_agg."""
        return aggregate_ssim(vals, self.ssim_agg)

    def dataset_ssim(self, x: Solution) -> float:
        """SSIM agregada de x sobre todas as imagens do conjunto.
        Distribui as imagens pelo ProcessPoolExecutor persistente enviando apenas
        índices e tupla de multiplicadores para evitar sobrecarga de IPC."""
        mult_names = tuple(self.library[i].name for i in x)
        if self._pool is not None:
            tasks = [(i, mult_names) for i in range(len(self.images))]
            chunk = max(1, len(self.images) // self.max_workers)
            vals = list(self._pool.map(_eval_one_image, tasks, chunksize=chunk))
        else:
            vals = []
            for i in range(len(self.images)):
                disp = _SlotDispatcher([self.library[idx].fn for idx in x])
                out = apply_gaussian_filter(self.images[i], disp, kernel=self.kernel, norm_factor=self.norm)
                vals.append(calc_ssim(self.references[i], out))
        return self.aggregate_ssim(vals)

    def mean_ssim(self, x: Solution) -> float:
        """Alias para dataset_ssim mantido para compatibilidade retroativa."""
        return self.dataset_ssim(x)

    def per_image_metrics(self, x: Solution) -> List[Dict]:
        """Métricas de qualidade de x, imagem por imagem (usado na validação)."""
        rows = []
        for i in range(len(self.images)):
            out = self.render(x, i)
            ref = self.references[i]
            rows.append({
                "Imagem": self.names[i],
                "SSIM": calc_ssim(ref, out),
                "MSE": calc_mse(ref, out),
                "PSNR (dB)": calc_psnr(ref, out),
                "MAE": calc_mae(ref, out),
                "Max Error": int(calc_max_error(ref, out)),
                "Error Rate (%)": calc_error_rate(ref, out),
            })
        return rows

    def evaluate(self, x: Solution) -> Tuple[int, float]:
        """Avaliar(x): devolve (R(x), SSIM agregada no conjunto). Resultados são memorizados."""
        if x not in self._cache:
            self.n_evals += 1
            self._evals_since_improvement += 1
            ssim = round(self.dataset_ssim(x), 4)
            cost = self.cost(x)
            self._cache[x] = (cost, ssim)
            if self.is_feasible(ssim) and (self.best_cost is None or cost < self.best_cost):
                self.best_cost = cost
                self.best_solution = x
                self.best_ssim = ssim
                self._evals_since_improvement = 0
                self.trace.append({
                    "time_s": time.perf_counter() - self.t0,
                    "evals": self.n_evals,
                    "cost": cost,
                    "ssim": ssim,
                    "k": self.current_k,
                })
        return self._cache[x]

    def budget_exhausted(self) -> bool:
        """True quando o orçamento de avaliações (ou o teto opcional de tempo wall-clock) acabou."""
        if self.max_evals is not None and self.n_evals >= self.max_evals:
            return True
        return self.deadline is not None and time.perf_counter() >= self.deadline

    def patience_exhausted(self) -> bool:
        """True quando a paciência de avaliações sem melhoria viável foi esgotada."""
        return (
            self.patience is not None
            and self.patience > 0
            and self._evals_since_improvement >= self.patience
        )

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
            # Respeita o orçamento também DENTRO da busca local (cada avaliação é
            # cara com várias imagens), devolvendo o melhor encontrado até agora.
            if problem.budget_exhausted() or problem.patience_exhausted():
                return x_best
            R_y, s_y = problem.evaluate(y)
            if problem.is_better(R_y, s_y, R_best, s_best):
                x_best, R_best, s_best = y, R_y, s_y
                improved = True
        if not (improved and descent):
            return x_best


def change_neighborhood_dse(
    problem: DSEProblem, x: Solution, x_new: Solution, k: int
) -> Tuple[Solution, int]:
    """MudarVizinhançaDSE (Opção A - exploração e reparo de soluções inviáveis):
    Aceita x_new e reseta a vizinhança para k=1 se:
      1) x_new é viável e (x era inviável OU R(x_new) < R(x));
      2) x_new é inviável, mas possui SSIM superior a x (avanço no reparo).
    Caso contrário, rejeita e incrementa a vizinhança: k <- k + 1.
    """
    R_x, s_x = problem.evaluate(x)
    R_n, s_n = problem.evaluate(x_new)

    feasible_x = problem.is_feasible(s_x)
    feasible_n = problem.is_feasible(s_n)

    # 1. Solução viável com menor custo (ou que recuperou a viabilidade)
    if feasible_n and (not feasible_x or R_n < R_x):
        return x_new, 1

    # 2. Ambas inviáveis, mas x_new melhora o SSIM (avanço no reparo)
    if not feasible_n and not feasible_x and s_n > s_x:
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
    history: List[Dict] = field(default_factory=list)  # best-so-far: cada avaliação que melhora o custo viável
    ssim_agg: str = "mean"


def vns(
    problem: DSEProblem,
    max_evals: Optional[int] = 500,
    t_max: Optional[float] = None,
    k_max: int = 4,
    seed: Optional[int] = None,
    descent: bool = True,
    verbose: bool = True,
    patience: Optional[int] = 100,
) -> VNSResult:
    """Algoritmo principal (VNS para seleção de multiplicadores).

    Critério de parada: `max_evals` avaliações reais (a avaliação da solução inicial
    conta), `patience` avaliações sem melhoria do melhor viável, e/ou `t_max` segundos
    de relógio (wall-clock); vale o que ocorrer primeiro.
    """
    if max_evals is None and t_max is None:
        raise ValueError("Defina max_evals e/ou t_max.")
    rng = random.Random(seed)
    k_max = max(1, min(k_max, problem.n_slots))

    t0 = time.perf_counter()
    problem.t0 = t0
    problem.max_evals = max_evals
    problem.deadline = None if t_max is None else t0 + t_max
    if patience is not None:
        problem.patience = patience
    problem._evals_since_improvement = 0
    elapsed = lambda: time.perf_counter() - t0

    x = problem.initial_solution()
    R, s = problem.evaluate(x)
    start_time_str = time.strftime('%Y-%m-%d %H:%M:%S')
    teto_str = f"{t_max}s" if t_max is not None else "sem teto"
    if verbose:
        print(f"[VNS] wall-clock start: {start_time_str}")
        print(f"[VNS] inicial (todos exatos): R={R}  SSIM={s:.4f}  "
              f"posições={problem.n_slots}  biblioteca={len(problem.library)}  T={problem.threshold}  "
              f"max_evals={max_evals}  teto_tempo={teto_str}  patience={problem.patience}")

    iterations = 0
    idle = 0  # iterações seguidas sem nenhuma avaliação nova (espaço esgotado)
    MAX_IDLE = 1000

    while not problem.budget_exhausted() and not problem.patience_exhausted() and idle < MAX_IDLE:
        k = 1
        while k <= k_max and not problem.budget_exhausted() and not problem.patience_exhausted() and idle < MAX_IDLE:
            problem.current_k = k
            evals_before = problem.n_evals
            x1 = perturbation_dse(problem, x, k, rng)
            x2 = local_search_dse(problem, x1, descent)
            x_new, k_new = change_neighborhood_dse(problem, x, x2, k)
            iterations += 1
            idle = idle + 1 if problem.n_evals == evals_before else 0

            if x_new != x:
                R_cur, s_cur = problem.evaluate(x_new)
                if verbose:
                    status = "viável" if problem.is_feasible(s_cur) else "inviável (reparo)"
                    print(f"[VNS] t={elapsed():6.2f}s  k={k}  nova melhor ({status}): "
                          f"R={R_cur}  SSIM={s_cur:.4f}  (avaliações={problem.n_evals})")
            x, k = x_new, k_new

    if problem.patience_exhausted():
        print(f"[VNS] paciência esgotada após {problem._evals_since_improvement} avaliações sem melhoria (T={problem.threshold})")

    # Garante que a solução final retornada seja SEMPRE viável (SSIM >= T).
    # Se problem.best_solution estiver disponível, usa a melhor viável encontrada;
    # caso contrário, retrocede para a solução inicial exata (garantidamente viável).
    if problem.best_solution is not None and problem.is_feasible(problem.best_ssim):
        final_x = problem.best_solution
        final_R = problem.best_cost
        final_s = problem.best_ssim
    else:
        init_x = problem.initial_solution()
        init_R, init_s = problem.evaluate(init_x)
        final_x, final_R, final_s = init_x, init_R, init_s

    total_elapsed = elapsed()
    end_time_str = time.strftime('%Y-%m-%d %H:%M:%S')
    if verbose:
        print(f"[VNS] wall-clock end: {end_time_str} (duração: {total_elapsed:.2f}s)")

    return VNSResult(
        final_x, final_R, final_s, total_elapsed, iterations,
        problem.n_evals, list(problem.trace), problem.ssim_agg
    )


# ===========================================================================
# Validação e relatórios
# ===========================================================================

def threshold_tag(T: float) -> str:
    """0.95 -> 'T95' (usado em nomes de arquivo)."""
    return f"T{int(round(T * 100))}"


def aggregate(per_image: List[Dict], ssim_agg: str = "mean") -> Dict:
    """Agrega as métricas por imagem em médias sobre o conjunto.
    PSNR: média apenas dos valores finitos (imagem idêntica à referência dá inf);
    se todas forem inf, o resultado é inf.
    MSE: média aritmética simples entre imagens (padrão em benchmarks de processamento de imagem).
    SSIM: agregada conforme o modo ssim_agg (mean, geomean, median)."""
    psnrs = [m["PSNR (dB)"] for m in per_image if np.isfinite(m["PSNR (dB)"])]
    ssim_vals = [m["SSIM"] for m in per_image]
    return {
        "SSIM": aggregate_ssim(ssim_vals, ssim_agg),
        "SSIM min": float(np.min(ssim_vals)),
        "MSE": float(np.mean([m["MSE"] for m in per_image])),
        "PSNR (dB)": float(np.mean(psnrs)) if psnrs else float("inf"),
        "MAE": float(np.mean([m["MAE"] for m in per_image])),
        "Max Error": int(np.max([m["Max Error"] for m in per_image])),
        "Error Rate (%)": float(np.mean([m["Error Rate (%)"] for m in per_image])),
    }


def validate(
    runs: List[Tuple[DSEProblem, VNSResult]],
    val_problem: DSEProblem,
    output_dir: str,
) -> List[Dict]:
    """FASE 2 - VALIDAÇÃO: aplica as soluções do VNS (obtidas no treino) às imagens
    de validação e reporta o desempenho MÉDIO sobre esse conjunto.

    A tabela contém as configurações uniformes (mesmo componente em todas as
    posições) e UMA linha de VNS por limiar T. 'SSIM treino' é a SSIM média no
    conjunto de treino (a que o VNS otimizou) e 'SSIM val' a média no conjunto de
    validação. 'Viavel (val)' = SSIM val >= T (só nas linhas do VNS)."""
    if not runs:
        raise RuntimeError("Nenhuma execução fornecida para validação (runs está vazio).")

    train = runs[0][0]  # biblioteca/kernel iguais em todas as execuções
    R_exact = train.cost(train.initial_solution())

    # Cache de SSIM de treino para configurações uniformes para não reavaliar o treino
    uniform_train_cache: Dict[Solution, float] = {}

    def get_uniform_train_ssim(x: Solution) -> float:
        if x not in uniform_train_cache:
            # Verifica se algum problema das execuções já tem a solução no cache
            for prob, _ in runs:
                if x in prob._cache:
                    uniform_train_cache[x] = prob._cache[x][1]
                    break
            else:
                uniform_train_cache[x] = round(train.evaluate(x)[1], 4)
        return uniform_train_cache[x]

    def make_row(
        label: str,
        x: Solution,
        threshold: Optional[float] = None,
        train_ssim: Optional[float] = None,
    ) -> Dict:
        per_image = val_problem.per_image_metrics(x)
        m = aggregate(per_image, ssim_agg=val_problem.ssim_agg)
        R = train.cost(x)
        if train_ssim is None:
            train_ssim = get_uniform_train_ssim(x)

        return {
            "Configuracao": label,
            "Threshold": "" if threshold is None else threshold,
            "SSIM agg": val_problem.ssim_agg,
            "LUT+FF": R,
            "Economia (%)": round((R_exact - R) / R_exact * 100.0, 2) if R_exact else 0.0,
            "SSIM treino": round(train_ssim, 4),
            "SSIM val": round(m["SSIM"], 4),
            "SSIM val (min)": round(m["SSIM min"], 4),
            "MSE val": round(m["MSE"], 6),
            "PSNR val (dB)": m["PSNR (dB)"] if np.isinf(m["PSNR (dB)"]) else round(m["PSNR (dB)"], 2),
            "MAE val": round(m["MAE"], 4),
            "Max Error val": m["Max Error"],
            "Error Rate val (%)": round(m["Error Rate (%)"], 2),
            "Viavel (val)": "" if threshold is None else round(m["SSIM"], 4) >= threshold,
        }

    rows = []
    # 1. Configurações uniformes (avaliadas e cacheadas apenas uma vez)
    for i, c in enumerate(train.library):
        uniform_x = tuple([i] * train.n_slots)
        rows.append(make_row(f"uniforme: {c.name}", uniform_x))

    # 2. Soluções do VNS (reutiliza diretamente result.ssim do treino sem reavaliar)
    for problem, result in runs:
        rows.append(make_row(
            f"VNS (solução final T={problem.threshold:.2f})",
            result.x,
            threshold=problem.threshold,
            train_ssim=result.ssim,
        ))

    rows.sort(key=lambda r: (r["LUT+FF"], -float(r["SSIM val"])))

    fmt = "{:<34} | {:>7} | {:>9} | {:>11} | {:>9} | {:>9} | {:>10} | {:>10} | {:>7} | {:>6} | {:>6}"
    line = "=" * 148
    print("\n" + line)
    print(f"VALIDAÇÃO  ({len(val_problem.images)} imagens de validação; médias sobre o conjunto)")
    print(line)
    print(fmt.format("Configuração", "LUT+FF", "Economia", "SSIM treino", "SSIM val",
                     "SSIM min", "MSE", "PSNR (dB)", "MAE", "MaxErr", "Viável"))
    print("-" * 148)
    for r in rows:
        psnr = "inf" if r["PSNR val (dB)"] == float("inf") else f"{r['PSNR val (dB)']:.2f}"
        mse_str = f"{r['MSE val']:.4f}"
        is_vns = r["Configuracao"].startswith("VNS")
        viavel = (("sim" if r["Viavel (val)"] else "não") if is_vns else "-")
        mark = "  <== VNS" if is_vns else ""
        print(fmt.format(r["Configuracao"], r["LUT+FF"], f"{r['Economia (%)']:.1f}%",
                         f"{r['SSIM treino']:.4f}", f"{r['SSIM val']:.4f}",
                         f"{r['SSIM val (min)']:.4f}", mse_str, psnr, f"{r['MAE val']:.3f}",
                         r["Max Error val"], viavel) + mark)
    print(line + "\n")

    with open(os.path.join(output_dir, "vns_validation.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # Detalhe por imagem de validação para cada solução do VNS
    def _round_metric(k: str, v):
        if isinstance(v, float) and np.isfinite(v):
            return round(v, 6) if k == "MSE" else round(v, 4)
        return v

    detail = []
    for problem, result in runs:
        for m in val_problem.per_image_metrics(result.x):
            row = {"Threshold": problem.threshold}
            row.update({k: _round_metric(k, v) for k, v in m.items()})
            detail.append(row)
    with open(os.path.join(output_dir, "vns_validation_per_image.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(detail[0].keys()))
        w.writeheader()
        w.writerows(detail)
    return rows


def load_solution(path: str, library: List[Component], n_slots: int) -> Solution:
    """Lê um vns_solution_Txx.csv (gerado no treino) e devolve o vetor x."""
    by_name = {c.name: i for i, c in enumerate(library)}
    with open(path, newline="") as f:
        names = [r["Multiplicador"] for r in csv.DictReader(f)]
    if len(names) != n_slots:
        raise RuntimeError(f"{path}: {len(names)} posições, esperado {n_slots}.")
    return tuple(by_name[n] for n in names)  # KeyError => multiplicador fora da biblioteca


def append_rows(path: str, fieldnames: List[str], rows: List[Dict]) -> None:
    """Acrescenta linhas a um CSV (cria com cabeçalho se não existir).

    Se o arquivo já existir com cabeçalho diferente, emite aviso e anexa
    respeitando o cabeçalho existente sem destruir os dados anteriores.
    """
    if not rows:
        return

    write_header = not os.path.exists(path) or os.path.getsize(path) == 0
    if not write_header:
        with open(path, newline="") as f:
            existing = next(csv.reader(f), [])
        if existing != fieldnames:
            print(f"[aviso] cabeçalho de {path} diferente ({existing} != {fieldnames}); mantendo cabeçalho existente para não corromper histórico.")
            fieldnames = existing

    with open(path, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        if write_header:
            w.writeheader()
        w.writerows(rows)


def append_history(path: str, threshold: float, result: VNSResult, ssim_agg: str = "mean") -> None:
    """vns_history.csv: UMA linha por execução (resumo final), acumulada entre execuções."""
    row = {
        "Threshold": threshold,
        "Cost": result.cost,
        "SSIM": round(result.ssim, 4),
        "SSIM agg": ssim_agg,
        "Evaluations": result.evaluations,
        "Iterations": result.iterations,
        "Time_s": round(result.elapsed, 2),
    }
    append_rows(path, list(row.keys()), [row])


def append_trace(path: str, threshold: float, trace: List[Dict]) -> None:
    """vns_trace.csv: pontos de convergência (best-so-far a cada avaliação que melhora),
    acumulados entre execuções. É a fonte do gráfico de convergência."""
    if not trace:
        return
    fieldnames = ["Threshold"] + list(trace[0].keys())
    append_rows(path, fieldnames, [{"Threshold": threshold, **t} for t in trace])


def save_outputs(problem: DSEProblem, result: VNSResult, output_dir: str) -> None:
    """Salva os artefatos de UMA execução de treino (nomes com sufixo do limiar, ex.: _T95)."""
    os.makedirs(output_dir, exist_ok=True)
    tag = threshold_tag(problem.threshold)

    # Pré-visualização: apenas a primeira imagem de treino (o VNS usa todas)
    Image.fromarray(problem.references[0]).save(os.path.join(output_dir, "filtered_reference.png"))
    Image.fromarray(problem.render(result.x, 0)).save(os.path.join(output_dir, f"filtered_vns_{tag}.png"))

    rows = problem.describe(result.x)
    with open(os.path.join(output_dir, f"vns_solution_{tag}.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    append_history(os.path.join(output_dir, "vns_history.csv"), problem.threshold, result, problem.ssim_agg)
    append_trace(os.path.join(output_dir, "vns_trace.csv"), problem.threshold, result.history)

    try:
        import matplotlib.pyplot as plt
        if result.history:
            e = [h["evals"] for h in result.history] + [result.evaluations]
            c = [h["cost"] for h in result.history] + [result.cost]
        else:
            e = [0, result.evaluations]
            c = [result.cost, result.cost]
        fig = plt.figure(figsize=(7, 4))
        plt.step(e, c, where="post", color="royalblue")
        if result.history:
            plt.scatter([h["evals"] for h in result.history], [h["cost"] for h in result.history], color="royalblue", zorder=3)
        plt.xlabel("Avaliações (evals)")
        plt.ylabel("Custo R(x) = LUT + FF")
        plt.title(f"Convergência do VNS - treino (T={problem.threshold:.2f})")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"vns_convergence_{tag}.png"), dpi=200)
        plt.close(fig)
        plt.close("all")
    except Exception as e:  # o gráfico é opcional
        print(f"[aviso] gráfico de convergência não gerado: {e}")


def threshold_sequence(start_pct: int, end_pct: int, step_pct: int) -> List[float]:
    """[95, 70, 5] -> [0.95, 0.90, 0.85, 0.80, 0.75, 0.70] (em inteiros para evitar erro de float)."""
    if step_pct <= 0:
        raise ValueError("--t-step deve ser > 0")
    if start_pct < end_pct:
        raise ValueError(f"--t-start ({start_pct}) deve ser >= --t-end ({end_pct}) para decremento.")
    seq = [p / 100.0 for p in range(start_pct, end_pct - 1, -step_pct)]
    if not seq:
        raise ValueError(f"Sequência de limiares vazia para start={start_pct}, end={end_pct}, step={step_pct}.")
    return seq


def main():
    p = argparse.ArgumentParser(description="VNS para DSE de multiplicadores aproximados "
                                            "(filtro Gaussiano) - treino + validação")
    p.add_argument("--dataset", "-d", default=None,
                   help="Diretório com as imagens (default: dataset sintético, só para teste)")
    p.add_argument("--total", type=int, default=100, help="Nº de imagens usadas do dataset (default: 100)")
    p.add_argument("--train-count", type=int, default=70,
                   help="Imagens 1..N para treino; as restantes para validação (default: 70)")
    p.add_argument("--csv", "-c", default="metrics_all.csv", help="metrics_all.csv da síntese HLS")
    p.add_argument("--output", "-o", default="output/vns", help="Diretório de saída")
    p.add_argument("--kernel-size", "-k", type=int, default=5, choices=[3, 5, 7])
    p.add_argument("--sigma", "-s", type=float, default=1.0)
    p.add_argument("--t-start", "-ts", type=int, default=95, help="Primeiro limiar de SSIM, em %% (default: 95)")
    p.add_argument("--t-end", "-te", type=int, default=70, help="Último limiar de SSIM, em %% (default: 70)")
    p.add_argument("--t-step", type=int, default=5, help="Decremento do limiar, em %% (default: 5)")
    p.add_argument("--max-evals", "-mev", type=int, default=500,
                   help="Nº máximo de avaliações reais (cache misses) POR limiar (default: 500)")
    p.add_argument("--patience", "-p", type=int, default=100,
                   help="Nº de avaliações sem melhoria do melhor viável antes de parar (0 para desativar, default: 100)")
    p.add_argument("--ssim-agg", choices=["mean", "geomean", "median"], default="mean",
                   help="Modo de agregação de SSIM sobre o conjunto de imagens (default: mean)")
    p.add_argument("--time", "-t", type=float, default=None,
                   help="Teto OPCIONAL de tempo de relógio (wall-clock) POR limiar, em segundos (default: sem teto)")
    p.add_argument("--kmax", type=int, default=4, help="Número máximo de vizinhanças (default: 4)")
    p.add_argument("--seed", type=int, default=None, help="Semente aleatória (reprodutibilidade)")
    p.add_argument("--single-sweep", action="store_true",
                   help="Busca local com uma única varredura (como no pseudocódigo do artigo)")
    p.add_argument("--validate-only", action="store_true",
                   help="Pula o treino: lê vns_solution_Txx.csv do diretório de saída e só valida")
    max_cpu = os.cpu_count() or 1
    p.add_argument("--threads", "-w", "--workers", type=int, nargs="?",
                   const=max_cpu, default=max_cpu,
                   help=f"Número de threads/workers para processamento paralelo (default: {max_cpu}, máx. da CPU)")
    args = p.parse_args()
    if args.threads is not None and args.threads < 1:
        p.error("--threads deve ser >= 1")
    if args.max_evals is not None and args.max_evals < 1:
        p.error("--max-evals deve ser >= 1")
    if args.patience < 0:
        p.error("--patience deve ser >= 0")

    # Dataset e divisão treino / validação
    if args.dataset:
        data = load_dataset(args.dataset, args.total)
        print(f"Dataset '{args.dataset}': {len(data)} imagens carregadas")
    else:
        data = create_synthetic_dataset(args.total, seed=args.seed or 0)
        print(f"Usando dataset SINTÉTICO com {len(data)} imagens (use --dataset para o real)")
    train_set, val_set = split_dataset(data, args.train_count)
    print(f"Treino:    imagens 1..{len(train_set)}  ({train_set[0][0]} ... {train_set[-1][0]})")
    print(f"Validação: imagens {len(train_set) + 1}..{len(data)}  ({val_set[0][0]} ... {val_set[-1][0]})")

    train_imgs, train_names = [im for _, im in train_set], [n for n, _ in train_set]
    val_imgs, val_names = [im for _, im in val_set], [n for n, _ in val_set]
    print(f"Workers paralelos: {args.threads}")

    library = build_library(args.csv)
    print("Biblioteca:", ", ".join(f"{c.name}({c.cost})" for c in library))

    thresholds = threshold_sequence(args.t_start, args.t_end, args.t_step)
    print("Limiares:", ", ".join(f"{T:.2f}" for T in thresholds))

    # Fix 3: Pré-computar referências exatas uma única vez para treino e validação
    exact_kernel, exact_norm = get_gaussian_kernel(size=args.kernel_size, sigma=args.sigma)
    exact_fn = get_multiplier("multExato")
    print(f"Pré-computando referências exatas para treino ({len(train_imgs)} imagens)...")
    train_refs = [
        apply_gaussian_filter(im, exact_fn, kernel=exact_kernel, norm_factor=exact_norm)
        for im in train_imgs
    ]
    print(f"Pré-computando referências exatas para validação ({len(val_imgs)} imagens)...")
    val_refs = [
        apply_gaussian_filter(im, exact_fn, kernel=exact_kernel, norm_factor=exact_norm)
        for im in val_imgs
    ]

    def new_problem(imgs, names, T, reference_images=None):
        return DSEProblem(
            imgs, library, kernel_size=args.kernel_size,
            sigma=args.sigma, threshold=T, names=names,
            reference_images=reference_images,
            ssim_agg=args.ssim_agg,
            patience=args.patience,
            max_workers=args.threads,
        )

    os.makedirs(args.output, exist_ok=True)
    runs: List[Tuple[DSEProblem, VNSResult]] = []

    for T in thresholds:
        # Problema novo por limiar (cache próprio): cada execução parte do zero,
        # para que o orçamento de avaliações seja idêntico entre limiares.
        problem = new_problem(train_imgs, train_names, T, reference_images=train_refs)

        # Pré-avalia e cacheia as configurações uniformes no primeiro problem enquanto o pool está ativo
        if len(runs) == 0:
            for c_idx in range(len(library)):
                u_x = tuple([c_idx] * problem.n_slots)
                problem.evaluate(u_x)

        if args.validate_only:
            path = os.path.join(args.output, f"vns_solution_{threshold_tag(T)}.csv")
            x = load_solution(path, library, problem.n_slots)
            R, s = problem.evaluate(x)
            runs.append((problem, VNSResult(x, R, s, 0.0, 0, problem.n_evals, ssim_agg=problem.ssim_agg)))
            print(f"[validate-only] {path}: R={R}  SSIM treino={s:.4f}")
            problem.close()
            continue

        print("\n" + "#" * 70)
        print(f"# FASE 1 - TREINO: VNS com T = {T:.2f}  ({len(train_imgs)} imagens)")
        print("#" * 70)
        result = vns(problem, max_evals=args.max_evals, t_max=args.time,
                     k_max=args.kmax, seed=args.seed,
                     descent=not args.single_sweep, patience=args.patience)

        print(f"\n[VNS] fim (T={T:.2f}): {result.iterations} iterações, {result.evaluations} avaliações, "
              f"{result.elapsed:.2f}s (wall-clock)")
        print(f"[VNS] melhor solução: R={result.cost}  SSIM média (treino)={result.ssim:.4f}")
        for row in problem.describe(result.x):
            print(f"    {row['Posicao']:<22} -> {row['Multiplicador']}")

        save_outputs(problem, result, args.output)
        runs.append((problem, result))
        problem.close()

    print("\n" + "#" * 70)
    print(f"# FASE 2 - VALIDAÇÃO: {len(val_imgs)} imagens")
    print("#" * 70)
    val_problem = new_problem(val_imgs, val_names, thresholds[0], reference_images=val_refs)
    try:
        validate(runs, val_problem, args.output)
    finally:
        val_problem.close()
    print(f"Arquivos salvos em {args.output}/")


if __name__ == "__main__":
    main()