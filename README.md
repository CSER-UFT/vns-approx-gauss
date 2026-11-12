# Como executar o projeto

## 1. Visão geral
Este repositório contém scripts Python que automatizam a Variable Neighborhood Search (VNS) para otimizar filtros Gaussiano em FPGA, além de ferramentas para gerar gráficos a partir dos resultados. O fluxo típico é:

1. **Instalar as dependências** (uv ou pip).  
2. **Executar o VNS** (`vns.py`) com as flags desejadas.  
3. **Compilar o projeto Vitis HLS**
4. **Plotar os resultados** (`plot_graficos.py`).

---

## 2. Requisitos

Todas as dependências Python estão listadas em `requirements.txt`. Instale-as usando `uv` (recomendado) ou `pip` conforme descrito na seção seguinte.

O `uv` é um gerenciador de pacotes Python moderno e significativamente mais rápido que o `pip`. Caso ainda não o tenha instalado:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

> **Obs.:** Se preferir o método clássico, crie e ative um *virtualenv* antes de usar `pip` (ver seção 3.2).

---

## 3. Instalação

### 3.1 Opção 1 – Usando **uv** (recomendado)

```bash
# Na raiz do repositório
uv sync            # lê uv.lock/requirements.txt e cria o ambiente virtual
```

### 3.2 Opção 2 – Usando **pip**

```bash
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

---

## 4. Execução do VNS

O script principal é **`vns.py`**. Ele aceita as seguintes flags (listadas em `--help`):

| Flag | Tipo | Valor padrão | Descrição |
|------|------|--------------|----------|
| `--dataset <caminho>` | `str` | – | Diretório contendo as imagens de entrada. |
| `--train-count <N>` | `int` | – | Quantidade de imagens usadas na fase de treino. |
| `--total <N>` | `int` | – | Número total de imagens (treino + validação). |
| `--t-start <int>` | `int` | 95 | SSIM inicial (ex.: 95). |
| `--t-end <int>` | `int` | 70 | SSIM final (ex.: 70). |
| `--t-step <int>` | `int` | 5 | Passo entre limites (ex.: 5). |
| `--max-evals <N>` | `int` | – | Máximo de avaliações reais por limiar. |
| `--kmax <N>` | `int` | – | Número máximo de vizinhanças (k). |
| `--threads <N>` ou `-w <N>` | `int` | *todas* | Número de threads/processos. |
| `--time <s>` | `float` | – | Teto de tempo em segundos (opcional). |
| `--patience <N>` | `int` | 100 | Interrompe o limiar após N avaliações sem melhora. |
| `--seed <int>` | `int` | 42 | Semente aleatória para reprodutibilidade. |
| `--validate-only` | flag | off | Apenas valida soluções já geradas (`output/vns/...`). |
| `--ssim-agg <media\|geomean\|mediana>` | `str` | `media` | Tipo de agregação de SSIM a usar. |
| `--k-size <3\|5>` | `int` | Detectado | Força o tamanho do kernel (3×3 ou 5×5). |
| `--output <caminho>` | `str` | `output/` | Diretório onde os CSVs de solução são gravados. |
| `-h` / `--help` | flag | – | Exibe a mensagem de ajuda com todas as opções. |

**Exemplo de execução completa**

```bash
python vns.py \
    --dataset image_dataset/ \
    --train-count 70 \
    --total 100 \
    --t-start 95 --t-end 70 --t-step 5 \
    --max-evals 6000 \
    --kmax 4 \
    --threads 12 \
    --seed 21 \
    --ssim-agg geomean \
    --patience 0 \
    --k-size 3 \
    --output output/vns3GeoMean0
```

O VNS grava, em `output/`, arquivos CSV contendo métricas de custo, SSIM, etc., organizados por limiar e por vizinhança (`k=3` ou `k=5`). Para que o script `run_all_hls.py` reconheça corretamente as soluções, os diretórios devem seguir o padrão `vns{kernel-size}{opt_agg}{patience}` (por exemplo `vns3Media0`, `vns5Geomean230`).

---

## 5. Compilação com Vitis HLS

Após a fase de VNS, os projetos HLS são gerados em `build/`. O fluxo de síntese pode ser realizado de três formas:

### 5.1 Script genérico `run_hls.tcl`
```bash
vitis_hls -f run_hls.tcl <caminho‑para‑solution.csv>
```
O script detecta automaticamente o tamanho do kernel (3×3 ou 5×5) a partir do nome da pasta e executa as etapas padrão de síntese, implementação e geração do relatório `gaussian_csynth.rpt`.

### 5.2 Scripts especializados
- **`run_hls3.tcl`** – otimizado para projetos com kernel 3×3, definindo diretivas de otimização específicas.
- **`run_hls5.tcl`** – otimizado para projetos com kernel 5×5, ajustando parâmetros de paralelismo e restrições de recurso.

Exemplo:
```bash
vitis_hls -f run_hls3.tcl output/vns3Media0/vns_solution_T95.csv
vitis_hls -f run_hls5.tcl output/vns5Media0/vns_solution_T95.csv
```

### 5.3 Automatização com `run_all_hls.py`
`run_all_hls.py` percorre recursivamente o diretório `output/`, localiza todos os arquivos `vns_solution_*.csv` e invoca a síntese correspondente. Possui opções:
- `--dry-run` : lista as ações sem executar o Vitis HLS.
- `--force` : reexecuta a síntese mesmo que o relatório já exista.
- `--k-size 3|5` : restringe a execução a um tamanho de kernel específico.

Exemplo:
```bash
python run_all_hls.py --dry-run          # mostra o que seria feito
python run_all_hls.py --force            # recompila tudo
python run_all_hls.py --k-size 5         # apenas soluções 5×5
```
---

## 6. Geração de gráficos

O script **`plot_graficos.py`** contém varios modos. Os mais comuns são:

| Modo | Descrição |
|------|-----------|
| `all` | Gera **todos** os gráficos disponíveis. |
| `main` | Gera os gráficos **principais**. |


Mais infos/flags para serem utilizadas no `--help`

**Exemplo de uso**

```bash
python plot_graficos.py main \
    --output-dir <você define> por padrão vai para `graficos`
```

Os gráficos são salvos no formato PDF.

---

## 7. Estrutura de diretórios

```
├── README.md                # Este documento
├── requirements.txt         # Dependências Python
├── uv.lock                  # Lockfile de uv (opcional)
├── vns.py                   # Algoritmo VNS
├── plot_graficos.py         # Ferramenta de visualização
├── src/                     # Código C++ para Vitis HLS
├── tb/                      # Testbenches
├── build/                   # Projetos HLS gerados (vns*_Media0, etc.)
├── output/                  # Resultados do VNS (CSV, imagens, logs)
└── graficos/                   # Gráficos produzidos pelo plot_graficos.py
```

---