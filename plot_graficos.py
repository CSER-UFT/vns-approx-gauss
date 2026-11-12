#!/usr/bin/env python3
"""
plot_graficos.py — Gera gráficos de recursos FPGA e qualidade para o TCC
                   (VNS + multiplicadores truncados em FPGA)

Modos disponíveis:
  stacked            — barras empilhadas LUT+FF+DSP por threshold (subplots por k_size)
  panels             — três subplots (LUT, FF, DSP) lado a lado, barras por threshold
  normalized         — barras de % de redução vs baseline, agrupadas por threshold
  boxplot            — boxplots de SSIM por threshold × opt_agg (gráfico 3.1)
  boxplot_psnr       — boxplots de PSNR por threshold × opt_agg (gráfico 3.2)
  tradeoff           — trade-off qualidade × área (gráfico 3.3)
  savings            — economia de recursos vs threshold (gráfico 3.4)
  patience_quality   — efeito da patience na qualidade (gráfico 3.5)
  patience_resources — efeito da patience nos recursos (gráfico 3.6)
  compliance         — taxa de cumprimento do threshold (gráfico 3.7)
  gap                — gap treino × validação (gráfico 3.8)
  k_comparison       — comparação k=3 vs k=5 (gráfico 3.9)
  convergence        — convergência do VNS (gráfico 3.10)
  heatmaps           — heatmaps de resumo (gráfico 3.11)
  ssim_threshold     — SSIM médio/mediano × threshold, um gráfico por k
  runtime            — tempo total de execução por cenário
  comparison         — comparação visual de imagens filtradas (95 a 70) de uma solução
  all                — gerar todos os gráficos

Uso:
  uv run plot_graficos.py [modo] [opções]
  uv run plot_graficos.py all
  uv run plot_graficos.py boxplot --k 3 --patience 0
  uv run plot_graficos.py tradeoff
  uv run plot_graficos.py comparison --solution output/vns3Media0 --image 71.ppm
"""

import argparse
import sys
import os
import csv
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import seaborn as sns

# ── Constantes visuais ──────────────────────────────────────────────
DPI = 300
RESOURCE_COLORS = {"LUT": "#1d4ed8", "FF": "#d97706", "DSP": "#059669"}
RESOURCE_NAMES = {"LUT": "Look-Up Tables (LUT)", "FF": "Flip-Flops (FF)", "DSP": "DSP Blocks"}
THRESHOLD_ORDER = [95, 90, 85, 80, 75, 70]          # mais restritivo → menos
THRESHOLD_LABELS = {t: f"0,{t}" for t in THRESHOLD_ORDER}
OPT_AGG_COLORS = {"media": "#2563eb", "geomean": "#059669", "mediana": "#dc2626"}
OPT_AGG_FILLS = {"media": "#dbeafe", "geomean": "#d1fae5", "mediana": "#fee2e2"}
OPT_AGG_EDGES = {"media": "#1d4ed8", "geomean": "#047857", "mediana": "#b91c1c"}
OPT_AGG_LABELS = {"media": "Média", "geomean": "Geométrica", "mediana": "Mediana"}
OPT_AGG_ORDER = ["media", "geomean", "mediana"]
OPT_AGG_DIR_MAP = {"media": "Media", "geomean": "GeoMean", "mediana": "Mediana"}
K_SIZES = [3, 5]
PATIENCE_VALUES = [0, 230, 350]

# Recursos totais disponíveis na FPGA (Artix-7 / plataforma do TCC)
FPGA_TOTAL = {"LUT": 32600, "FF": 65200, "DSP": 120}


def apply_theme():
    """Aplica estilo visual moderno e limpo para publicação científica."""
    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica", "Liberation Sans"],
        "axes.edgecolor": "#94a3b8",
        "axes.linewidth": 0.8,
        "axes.labelcolor": "#1e293b",
        "xtick.color": "#334155",
        "ytick.color": "#334155",
        "grid.color": "#f1f5f9",
        "grid.linestyle": "-",
        "grid.linewidth": 0.8,
        "axes.titlesize": 11,
        "axes.titleweight": "bold",
        "axes.titlecolor": "#0f172a",
        "axes.labelsize": 9.5,
        "axes.labelweight": "bold",
        "xtick.labelsize": 8.5,
        "ytick.labelsize": 8.5,
        "legend.fontsize": 8,
        "legend.edgecolor": "#cbd5e1",
        "legend.fancybox": True,
        "legend.framealpha": 0.95,
        "figure.titlesize": 12.5,
        "figure.titleweight": "bold",
    })


def add_tooltip_badge(ax, x, y, text, color="#1d4ed8", fontsize=6.5,
                      ha="center", va="bottom", offset=(0, 4), bg_color="#ffffff",
                      alpha=0.92, zorder=10):
    """Desenha um badge visual em estilo tooltip sobre um ponto ou barra."""
    ax.annotate(
        text,
        xy=(x, y),
        xytext=offset,
        textcoords="offset points",
        ha=ha,
        va=va,
        fontsize=fontsize,
        fontweight="bold",
        color="#0f172a",
        bbox=dict(
            boxstyle="round,pad=0.22,rounding_size=0.3",
            facecolor=bg_color,
            edgecolor=color,
            linewidth=0.8,
            alpha=alpha,
        ),
        zorder=zorder,
    )

# ── Helpers ─────────────────────────────────────────────────────────

def load_configs(csv_path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Carrega configs_encontradas.csv e separa baselines."""
    df = pd.read_csv(csv_path, dtype=str)
    df.columns = df.columns.str.strip()

    baselines = df[df["threshold"].str.strip() == "baseline"].copy()
    configs = df[df["threshold"].str.strip() != "baseline"].copy()

    for col in ("threshold", "k_size", "patience", "LUT", "FF", "DSP"):
        configs[col] = pd.to_numeric(configs[col])
    for col in ("k_size", "LUT", "FF", "DSP"):
        baselines[col] = pd.to_numeric(baselines[col])

    return configs, baselines


def get_baseline(baselines: pd.DataFrame, k: int) -> dict[str, int]:
    """Retorna dict {LUT, FF, DSP} do baseline para o k dado."""
    row = baselines[baselines["k_size"] == k].iloc[0]
    return {r: int(row[r]) for r in ("LUT", "FF", "DSP")}


def dir_name(k: int, opt_agg: str, patience: int) -> str:
    """Monta o nome da pasta: vns{k}{OptAgg}{patience}."""
    return f"vns{k}{OPT_AGG_DIR_MAP[opt_agg]}{patience}"


def load_validation(root: str, k: int, opt_agg: str, patience: int) -> pd.DataFrame:
    """Carrega vns_validation_per_image.csv de uma pasta de execução.

    Normaliza os nomes de colunas para:
      threshold, image, ssim, psnr, mae, max_error, error_rate
    (MSE pode estar ausente em execuções antigas — é ignorado nos gráficos.)
    """
    folder = Path(root) / dir_name(k, opt_agg, patience)
    csv_path = folder / "vns_validation_per_image.csv"
    if not csv_path.exists():
        print(f"⚠ Validação não encontrada: {csv_path}")
        return pd.DataFrame()
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()

    rename_map = {
        "Threshold": "threshold",
        "Imagem": "image",
        "SSIM": "ssim",
        "PSNR (dB)": "psnr",
        "MAE": "mae",
        "Max Error": "max_error",
        "Error Rate (%)": "error_rate",
    }
    df = df.rename(columns=rename_map)

    if "error_rate" in df.columns and df["error_rate"].max() > 1:
        df["error_rate"] = df["error_rate"] / 100.0

    df["k_size"] = k
    df["opt_agg"] = opt_agg
    df["patience"] = patience
    return df


def load_history(root: str, k: int, opt_agg: str, patience: int) -> pd.DataFrame:
    """Carrega vns_history.csv de uma pasta de execução.

    Normaliza colunas para: threshold, cost, ssim, ssim_agg, evaluations, iterations, time_s
    vns5Media0 não tem a coluna 'SSIM agg' (execução anterior à mudança) — default 'mean'.
    """
    folder = Path(root) / dir_name(k, opt_agg, patience)
    csv_path = folder / "vns_history.csv"
    if not csv_path.exists():
        print(f"⚠ Histórico não encontrado: {csv_path}")
        return pd.DataFrame()
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()

    rename_map = {
        "Threshold": "threshold",
        "Cost": "cost",
        "SSIM": "best_ssim",
        "SSIM agg": "ssim_agg",
        "Evaluations": "evaluations",
        "Iterations": "iterations",
        "Time_s": "time_s",
    }
    df = df.rename(columns=rename_map)

    # Se 'ssim_agg' não existir, preencher com 'mean' (execução antiga)
    if "ssim_agg" not in df.columns:
        df["ssim_agg"] = "mean"

    df["k_size"] = k
    df["opt_agg"] = opt_agg
    df["patience"] = patience
    return df


def load_trace(root: str, k: int, opt_agg: str, patience: int) -> pd.DataFrame:
    """Carrega vns_trace.csv de uma pasta de execução.

    Colunas: Threshold, time_s, evals, cost, ssim, k
    """
    folder = Path(root) / dir_name(k, opt_agg, patience)
    csv_path = folder / "vns_trace.csv"
    if not csv_path.exists():
        return pd.DataFrame()
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()
    rename_map = {"Threshold": "threshold"}
    df = df.rename(columns=rename_map)
    df["k_size"] = k
    df["opt_agg"] = opt_agg
    df["patience"] = patience
    return df


def build_long_validation(root: str) -> pd.DataFrame:
    """Monta a tabela longa de validação (config × imagem × threshold)."""
    frames = []
    for k in K_SIZES:
        for agg in OPT_AGG_ORDER:
            for pat in PATIENCE_VALUES:
                df = load_validation(root, k, agg, pat)
                if not df.empty:
                    frames.append(df)
    if not frames:
        sys.exit("✖ Nenhuma validação encontrada.")
    long = pd.concat(frames, ignore_index=True)
    # normalizar threshold para inteiro (70-95) para junção com configs
    if long["threshold"].max() <= 1:
        long["threshold"] = (long["threshold"] * 100).round().astype(int)
    return long


def build_long_history(root: str) -> pd.DataFrame:
    """Monta a tabela longa de histórico do VNS."""
    frames = []
    for k in K_SIZES:
        for agg in OPT_AGG_ORDER:
            for pat in PATIENCE_VALUES:
                df = load_history(root, k, agg, pat)
                if not df.empty:
                    frames.append(df)
    if not frames:
        print("⚠ Nenhum histórico encontrado.")
        return pd.DataFrame()
    hist = pd.concat(frames, ignore_index=True)
    if hist["threshold"].max() <= 1:
        hist["threshold"] = (hist["threshold"] * 100).round().astype(int)
    return hist


def build_long_trace(root: str) -> pd.DataFrame:
    """Monta a tabela longa de trace do VNS."""
    frames = []
    for k in K_SIZES:
        for agg in OPT_AGG_ORDER:
            for pat in PATIENCE_VALUES:
                df = load_trace(root, k, agg, pat)
                if not df.empty:
                    frames.append(df)
    if not frames:
        print("⚠ Nenhum trace encontrado.")
        return pd.DataFrame()
    trace = pd.concat(frames, ignore_index=True)
    if trace["threshold"].max() <= 1:
        trace["threshold"] = (trace["threshold"] * 100).round().astype(int)
    return trace


def build_aggregated(long_val: pd.DataFrame, configs: pd.DataFrame,
                     baselines: pd.DataFrame, history: pd.DataFrame) -> pd.DataFrame:
    """Monta a tabela agregada por config (1 linha por k/opt_agg/patience/threshold)."""
    grp_cols = ["k_size", "opt_agg", "patience", "threshold"]
    grp = long_val.groupby(grp_cols)

    agg_cols = {"ssim": ["mean", "median", "min", "std"],
                "psnr": ["mean", "median", "min", "std"],
                "mae": ["mean", "median"],
                "max_error": ["max"],
                "error_rate": ["mean"]}

    # Agregar manualmente para controlar nomes
    agg = grp.agg(
        ssim_mean=("ssim", "mean"),
        ssim_median=("ssim", "median"),
        ssim_min=("ssim", "min"),
        ssim_std=("ssim", "std"),
        ssim_q25=("ssim", lambda x: x.quantile(0.25)),
        ssim_q75=("ssim", lambda x: x.quantile(0.75)),
        psnr_mean=("psnr", "mean"),
        psnr_median=("psnr", "median"),
        psnr_min=("psnr", "min"),
        psnr_std=("psnr", "std"),
        mae_mean=("mae", "mean"),
        mae_median=("mae", "median"),
        max_error_max=("max_error", "max"),
        error_rate_mean=("error_rate", "mean"),
        n_images=("image", "nunique"),
    ).reset_index()

    # taxa de cumprimento: fração de imagens com SSIM ≥ threshold exigido
    # def compliance(sub):
    #     thr = sub["threshold"].iloc[0] / 100.0
    #     return (sub["ssim"] >= thr).mean()
    # comp = grp.apply(compliance, include_groups=False).reset_index(name="compliance_rate")
    # agg = agg.merge(comp, on=grp_cols)

    met = (long_val["ssim"] >= long_val["threshold"] / 100.0).rename("met")
    comp = (met.groupby([long_val[c] for c in grp_cols])
               .mean().reset_index(name="compliance_rate"))
    agg = agg.merge(comp, on=grp_cols)

    # juntar recursos de hardware
    agg = agg.merge(
        configs[["threshold", "k_size", "opt_agg", "patience", "LUT", "FF", "DSP"]],
        on=grp_cols,
        how="left",
    )

    # Uso de FPGA (% do total), economia em pp e redução relativa vs baseline
    for res in ("LUT", "FF", "DSP"):
        total = FPGA_TOTAL[res]
        # % do total da FPGA usado pela config
        agg[f"{res}_fpga_pct"] = agg[res].apply(
            lambda v: 100 * v / total if pd.notna(v) else np.nan
        )
        # economia em pp do total da FPGA (baseline% − config%)
        agg[f"{res}_pct"] = agg.apply(
            lambda r, _res=res, _total=total: (
                100 * (get_baseline(baselines, int(r["k_size"]))[_res] - r[_res]) / _total
            ) if pd.notna(r[_res]) else np.nan,
            axis=1,
        )
        # % de redução relativa ao baseline do circuito
        agg[f"{res}_rel_pct"] = agg.apply(
            lambda r, _res=res: (
                100 * (get_baseline(baselines, int(r["k_size"]))[_res] - r[_res])
                / get_baseline(baselines, int(r["k_size"]))[_res]
            ) if pd.notna(r[_res]) and get_baseline(baselines, int(r["k_size"]))[_res] > 0 else 0.0,
            axis=1,
        )
        # valor absoluto do baseline
        agg[f"{res}_baseline"] = agg.apply(
            lambda r, _res=res: get_baseline(baselines, int(r["k_size"]))[_res],
            axis=1,
        )

    # SSIM de treino (do histórico)
    if not history.empty:
        hist_merge = history[["threshold", "k_size", "opt_agg", "patience", "best_ssim"]].rename(
            columns={"best_ssim": "train_ssim"}
        )
        agg = agg.merge(hist_merge, on=grp_cols, how="left")
        agg["gap_train_val"] = agg["train_ssim"] - agg["ssim_median"]
    else:
        agg["train_ssim"] = np.nan
        agg["gap_train_val"] = np.nan

    return agg


def run_checks(long_val: pd.DataFrame, configs: pd.DataFrame, root: str):
    """Verificações obrigatórias antes de plotar."""
    n_ok = 0
    n_warn = 0

    # verificar pastas
    for k in K_SIZES:
        for agg in OPT_AGG_ORDER:
            for pat in PATIENCE_VALUES:
                d = Path(root) / dir_name(k, agg, pat)
                if d.exists():
                    n_ok += 1
                else:
                    print(f"⚠ Pasta faltando: {d}")
                    n_warn += 1

    # thresholds por pasta
    grp = long_val.groupby(["k_size", "opt_agg", "patience"])
    for name, sub in grp:
        thrs = sorted(sub["threshold"].unique())
        imgs = sorted(sub["image"].unique())
        n_imgs = len(imgs)
        if thrs != sorted(THRESHOLD_ORDER):
            print(f"⚠ Thresholds inesperados em {name}: {thrs}")
            n_warn += 1
        if n_imgs != 30:
            print(f"⚠ Número de imagens diferente de 30 em {name}: {n_imgs}")
            n_warn += 1

    # lista de imagens consistente
    all_imgs = long_val.groupby(["k_size", "opt_agg", "patience"])["image"].apply(
        lambda s: frozenset(s.unique())
    )
    if all_imgs.nunique() > 1:
        print("⚠ Listas de imagens diferem entre pastas!")
        n_warn += 1
    else:
        n_img = len(all_imgs.iloc[0])
        print(f"✔ Todas as {n_ok} pastas usam as mesmas {n_img} imagens.")

    # duplicatas
    dup = long_val.duplicated(subset=["k_size", "opt_agg", "patience", "threshold", "image"])
    if dup.any():
        print(f"⚠ {dup.sum()} linhas duplicadas na validação!")
        n_warn += 1
    else:
        print("✔ Sem duplicatas na validação.")

    if n_warn == 0:
        print(f"✔ Todas as {n_ok} pastas OK, {len(long_val)} linhas de validação.")
    else:
        print(f"⚠ {n_warn} avisos encontrados.")


def _apply_filters(df: pd.DataFrame, k_filter=None, opt_agg_filter=None,
                   patience_filter=None) -> pd.DataFrame:
    """Aplica filtros de k, opt_agg e patience a um DataFrame."""
    sub = df.copy()
    if k_filter is not None:
        sub = sub[sub["k_size"] == k_filter]
    if opt_agg_filter is not None:
        sub = sub[sub["opt_agg"] == opt_agg_filter]
    if patience_filter is not None:
        sub = sub[sub["patience"] == patience_filter]
    return sub


def _pareto_front(pts: np.ndarray) -> np.ndarray:
    """Retorna pontos na fronteira de Pareto (maximizar ambas as coordenadas)."""
    if len(pts) == 0:
        return np.array([])
    pts = np.unique(pts, axis=0)
    sorted_idx = np.argsort(-pts[:, 0])
    pts_sorted = pts[sorted_idx]
    front = [pts_sorted[0]]
    max_y = pts_sorted[0, 1]
    for p in pts_sorted[1:]:
        if p[1] > max_y:
            front.append(p)
            max_y = p[1]
    return np.array(front)


# ══════════════════════════════════════════════════════════════════════
# Gráficos de hardware (LUT / FF / DSP)
# ══════════════════════════════════════════════════════════════════════

def plot_stacked(configs, baselines, outdir, k_filter=None, opt_agg_filter=None,
                 patience_filter=None):
    """Barras empilhadas LUT+FF+DSP por threshold (subplots por k_size)."""
    sub = _apply_filters(configs, k_filter, opt_agg_filter, patience_filter)
    if sub.empty:
        print("✖ Sem dados após filtros para stacked."); return

    ks = sorted(sub["k_size"].unique())
    fig, axes = plt.subplots(1, len(ks), figsize=(7 * len(ks), 5), squeeze=False)

    for ax, k in zip(axes[0], ks):
        bl = get_baseline(baselines, k)
        dk = sub[sub["k_size"] == k].groupby("threshold")[["LUT", "FF", "DSP"]].mean()
        dk = dk.reindex(THRESHOLD_ORDER).dropna()

        labels = [THRESHOLD_LABELS.get(t, str(t)) for t in dk.index]
        x = np.arange(len(labels))
        bottom = np.zeros(len(x))

        for res in ("LUT", "FF", "DSP"):
            vals = dk[res].values
            ax.bar(x, vals, bottom=bottom, label=res, color=RESOURCE_COLORS[res], width=0.6)
            bottom += vals

        # baseline como linha
        bl_total = bl["LUT"] + bl["FF"] + bl["DSP"]
        ax.axhline(bl_total, color="black", ls="--", lw=1, label=f"Baseline (k={k})")

        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_xlabel("Threshold (SSIM)")
        ax.set_ylabel("Recursos (soma)")
        ax.set_title(f"Recursos FPGA — k = {k}")
        ax.legend(fontsize=8)

    fig.tight_layout()
    path = Path(outdir) / "stacked.pdf"
    fig.savefig(path, dpi=DPI)
    plt.close(fig)
    print(f"✔ Salvo: {path}")


def plot_panels(configs, baselines, outdir, k_filter=None, opt_agg_filter=None,
                patience_filter=None):
    """Três subplots (LUT, FF, DSP) lado a lado, barras por threshold."""
    sub = _apply_filters(configs, k_filter, opt_agg_filter, patience_filter)
    if sub.empty:
        print("✖ Sem dados após filtros para panels."); return

    ks = sorted(sub["k_size"].unique())
    resources = ["LUT", "FF", "DSP"]

    for k in ks:
        bl = get_baseline(baselines, k)
        dk = sub[sub["k_size"] == k].groupby("threshold")[resources].mean()
        dk = dk.reindex(THRESHOLD_ORDER).dropna()

        fig, axes = plt.subplots(1, 3, figsize=(14, 4.5), squeeze=False)
        labels = [THRESHOLD_LABELS.get(t, str(t)) for t in dk.index]
        x = np.arange(len(labels))

        for ax, res in zip(axes[0], resources):
            vals = dk[res].values
            ax.bar(x, vals, color=RESOURCE_COLORS[res], width=0.55)
            ax.axhline(bl[res], color="black", ls="--", lw=1, label=f"Baseline ({bl[res]})")
            ax.set_xticks(x)
            ax.set_xticklabels(labels)
            ax.set_xlabel("Threshold")
            ax.set_ylabel(res)
            ax.set_title(res)
            ax.legend(fontsize=8)

        fig.suptitle(f"Recursos FPGA por threshold — k = {k}", fontsize=13)
        fig.tight_layout()
        path = Path(outdir) / f"panels_k{k}.pdf"
        fig.savefig(path, dpi=DPI)
        plt.close(fig)
        print(f"✔ Salvo: {path}")


def plot_normalized(configs, baselines, outdir, k_filter=None, opt_agg_filter=None,
                    patience_filter=None):
    """Barras de utilização da FPGA (%) por threshold, com baseline como referência.

    Cada barra mostra o % do recurso total da FPGA usado pela config;
    a linha tracejada indica o % do baseline.
    """
    sub = _apply_filters(configs, k_filter, opt_agg_filter, patience_filter)
    if sub.empty:
        print("✖ Sem dados após filtros para normalized."); return

    ks = sorted(sub["k_size"].unique())
    resources = ["LUT", "FF", "DSP"]
    n_res = len(resources)

    for k in ks:
        bl = get_baseline(baselines, k)
        dk = sub[sub["k_size"] == k].groupby("threshold")[resources].mean()
        dk = dk.reindex(THRESHOLD_ORDER).dropna()

        fig, ax = plt.subplots(figsize=(9, 5))
        labels = [THRESHOLD_LABELS.get(t, str(t)) for t in dk.index]
        x = np.arange(len(labels))
        w = 0.22

        for i, res in enumerate(resources):
            total = FPGA_TOTAL[res]
            config_pct = 100 * dk[res].values / total
            bl_pct = 100 * bl[res] / total
            bars = ax.bar(x + (i - 1) * w, config_pct, width=w, label=res,
                          color=RESOURCE_COLORS[res])
            # linha do baseline para este recurso
            ax.axhline(bl_pct, color=RESOURCE_COLORS[res], ls="--", lw=0.9, alpha=0.5)

        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_xlabel("Threshold (SSIM)")
        ax.set_ylabel("Utilização da FPGA (%)")
        ax.set_title(f"Utilização de recursos da FPGA — k = {k} (tracejado = baseline)")
        ax.legend()

        fig.tight_layout()
        path = Path(outdir) / f"normalized_k{k}.pdf"
        fig.savefig(path, dpi=DPI)
        plt.close(fig)
        print(f"✔ Salvo: {path}")


# ══════════════════════════════════════════════════════════════════════
# 3.1 — Boxplot de SSIM por threshold × opt_agg
# ══════════════════════════════════════════════════════════════════════

def plot_boxplot_ssim(agg, long_val, history, outdir, k_filter=None,
                      patience_filter=None):
    """Boxplot de SSIM por threshold × opt_agg (gráfico 3.1).

    - Um painel por k_size (k=3 e k=5 lado a lado).
    - Por padrão, as 3 patiences (0, 230, 350) são AGRUPADAS: cada box (3 por
      threshold, um por opt_agg) reúne as imagens de validação de todas as
      patiences. Gera boxplot_ssim.pdf (painéis k=3 e k=5 juntos) e também
      boxplot_ssim_k3.pdf e boxplot_ssim_k5.pdf (um kernel por arquivo).
    - Com --patience N, gera apenas o gráfico daquela patience
      (boxplot_ssim_patN.pdf), como antes.
    - Linha tracejada vermelha com o threshold mínimo exigido.
    - Losango escuro marcando o SSIM de treino (vns_history.csv); no modo
      agrupado, é a média do SSIM de treino entre as patiences.
    - Badges acima de cada cluster: SSIM mediano e taxa de cumprimento.
    """
    apply_theme()
    sub = long_val.copy()
    if k_filter is not None:
        sub = sub[sub["k_size"] == k_filter]
    if patience_filter is not None:
        sub = sub[sub["patience"] == patience_filter]
    if sub.empty:
        print("✖ Sem dados para boxplot SSIM."); return

    ks = sorted(sub["k_size"].unique())
    pats = sorted(sub["patience"].unique())
    pooled = patience_filter is None
    n_agg = len(OPT_AGG_ORDER)

    # cada grupo = (sufixo do arquivo, patiences, rótulo, kernels do arquivo)
    if pooled:
        pat_txt = " + ".join(str(p) for p in pats)
        lbl = f"Patience = {pat_txt} (agrupadas)"
        groups = [("", pats, lbl, ks)]                      # figura com todos os painéis
        if len(ks) > 1:                                      # + uma figura por kernel
            groups += [(f"_k{k}", pats, lbl, [k]) for k in ks]
    else:
        groups = [(f"_pat{p}", [p], f"Patience = {p}", ks) for p in pats]

    for suffix, pat_list, pat_label, ks_fig in groups:
        sp = sub[sub["patience"].isin(pat_list)]
        leg_w = 3.2  # largura (pol.) da faixa à direita reservada p/ a legenda
        fig_w = 8.8 * len(ks_fig) + leg_w
        fig, axes = plt.subplots(1, len(ks_fig), figsize=(fig_w, 6.2), squeeze=False)

        for ax, k in zip(axes[0], ks_fig):
            sk = sp[sp["k_size"] == k]
            positions = []
            colors_fill = []
            colors_edge = []
            data = []
            tick_pos = []
            tick_lab = []

            for i, thr in enumerate(THRESHOLD_ORDER):
                base = i * (n_agg + 1)
                sub_thr = sk[sk["threshold"] == thr]
                for j, ag in enumerate(OPT_AGG_ORDER):
                    vals = sub_thr[sub_thr["opt_agg"] == ag]["ssim"]
                    data.append(vals.values if len(vals) else [])
                    positions.append(base + j)
                    colors_fill.append(OPT_AGG_FILLS[ag])
                    colors_edge.append(OPT_AGG_EDGES[ag])
                tick_pos.append(base + 1)
                tick_lab.append(THRESHOLD_LABELS.get(thr, str(thr)))

                # Badge com resumo de qualidade (mediana e taxa de cumprimento)
                if not sub_thr.empty:
                    med_val = sub_thr["ssim"].median()
                    comp_rate = (sub_thr["ssim"] >= (thr / 100.0)).mean() * 100
                    pill_txt = f"Med: {med_val:.3f}\nCumpr: {comp_rate:.0f}%"
                    ax.annotate(
                        pill_txt,
                        xy=(base + 1, 1.004),
                        xytext=(0, 0),
                        textcoords="offset points",
                        ha="center",
                        va="bottom",
                        fontsize=10,
                        fontweight="bold",
                        color="#334155",
                        bbox=dict(
                            boxstyle="round,pad=0.22,rounding_size=0.3",
                            facecolor="#f8fafc",
                            edgecolor="#94a3b8",
                            linewidth=0.6,
                            alpha=0.92,
                        ),
                        zorder=8,
                    )

            bp = ax.boxplot(
                data,
                positions=positions,
                widths=0.65,
                patch_artist=True,
                showmeans=False,
                showfliers=True,
                medianprops=dict(color="#0f172a", linewidth=2.0),
                flierprops=dict(
                    marker="o",
                    markersize=3.5,
                    alpha=0.45,
                    markerfacecolor="#475569",
                    markeredgecolor="#475569",
                ),
            )
            for patch, c_fill, c_edge in zip(bp["boxes"], colors_fill, colors_edge):
                patch.set_facecolor(c_fill)
                patch.set_edgecolor(c_edge)
                patch.set_linewidth(1.3)

            for i in range(len(data)):
                bp["whiskers"][2 * i].set(color=colors_edge[i], linewidth=1.1)
                bp["whiskers"][2 * i + 1].set(color=colors_edge[i], linewidth=1.1)
                bp["caps"][2 * i].set(color=colors_edge[i], linewidth=1.1)
                bp["caps"][2 * i + 1].set(color=colors_edge[i], linewidth=1.1)

            # Linha do threshold exigido
            for i, thr in enumerate(THRESHOLD_ORDER):
                base = i * (n_agg + 1)
                ax.plot([base - 0.45, base + n_agg - 0.55], [thr / 100, thr / 100],
                        color="#ef4444", ls="--", lw=1.5, alpha=0.85, zorder=4)

            # Losango com SSIM de treino (média entre as patiences do grupo)
            has_hist = not history.empty
            if has_hist:
                hist_sub = history[(history["k_size"] == k) &
                                   (history["patience"].isin(pat_list))]
                for i, thr in enumerate(THRESHOLD_ORDER):
                    base = i * (n_agg + 1)
                    for j, ag in enumerate(OPT_AGG_ORDER):
                        rows = hist_sub[(hist_sub["threshold"] == thr) &
                                        (hist_sub["opt_agg"] == ag)]
                        if not rows.empty:
                            ax.plot(base + j, rows["best_ssim"].mean(), "D",
                                    color="#0f172a", markersize=5.5, zorder=7)

            ax.set_xticks(tick_pos)
            ax.set_xticklabels(tick_lab)
            ax.set_xlabel("Threshold Exigido")
            n_txt = (f"{len(pat_list)} paciência × 30 imagens" if pooled
                     else "n = 30 imagens")
            ax.set_ylabel(f"SSIM na Validação ({n_txt})")
            # ax.set_title(f"Kernel {k}×{k} ({pat_label})", pad=10)

            # Limite inferior do eixo Y dinâmico (passos de 0.05)
            data_min = min(sk["ssim"].min(), min(THRESHOLD_ORDER) / 100.0) if not sk.empty else 0.70
            y_min = max(0.0, np.floor((data_min - 0.03) * 20) / 20.0)
            ax.set_ylim(y_min, 1.038)
            ax.grid(axis="y", color="#e2e8f0", linestyle="-", alpha=0.5, zorder=0)


        # fig.suptitle(f"Distribuição de SSIM por Threshold e Agregação — {pat_label}\n"
        #              "[Badges no topo: SSIM mediano e % de imagens cumprindo o threshold]",
        #              fontsize=12.5)
        fig.tight_layout(rect=(0, 0, 1 - leg_w / fig_w, 1))  # faixa à direita p/ a legenda

        # Legenda fora do gráfico, canto superior direito, alinhada ao topo dos eixos
        handles = [
            Patch(facecolor=OPT_AGG_FILLS[a], edgecolor=OPT_AGG_EDGES[a],
                  linewidth=1.2, label=OPT_AGG_LABELS[a])
            for a in OPT_AGG_ORDER
        ]
        handles.append(Line2D([], [], color="#ef4444", ls="--", lw=1.5,
                              label="Threshold exigido (corte)"))
        if not history.empty:
            lbl = "SSIM treino (média das patiences)" if pooled else "SSIM treino (VNS)"
            handles.append(Line2D([], [], marker="D", color="#0f172a", ls="",
                                  ms=5.5, label=lbl))
        y_top = axes[0][0].get_position().y1
        fig.legend(handles=handles, loc="upper right",
                   bbox_to_anchor=(0.99, y_top + 0.01), bbox_transform=fig.transFigure,
                   fontsize=10, labelcolor="black", frameon=True, fancybox=True, edgecolor="#1e293b",
                   framealpha=1.0)

        path = Path(outdir) / f"boxplot_ssim{suffix}.pdf"
        fig.savefig(path, dpi=DPI)
        plt.close(fig)
        print(f"✔ Salvo: {path}")


# ══════════════════════════════════════════════════════════════════════
# 3.2 — Boxplot de PSNR (ignorado por padrão devido a ruído)
# ══════════════════════════════════════════════════════════════════════

def plot_boxplot_psnr(agg, long_val, outdir, k_filter=None, patience_filter=None):
    """Boxplot de PSNR por threshold × opt_agg (ignorado por padrão)."""
    apply_theme()
    sub = long_val.copy()
    if k_filter is not None:
        sub = sub[sub["k_size"] == k_filter]
    if patience_filter is not None:
        sub = sub[sub["patience"] == patience_filter]
    if sub.empty:
        print("✖ Sem dados para boxplot PSNR."); return

    ks = sorted(sub["k_size"].unique())
    pats = sorted(sub["patience"].unique())

    for pat in pats:
        sp = sub[sub["patience"] == pat]
        fig, axes = plt.subplots(1, len(ks), figsize=(8 * len(ks), 6), squeeze=False)

        for ax, k in zip(axes[0], ks):
            sk = sp[sp["k_size"] == k]
            n_agg = len(OPT_AGG_ORDER)
            positions = []
            colors = []
            data = []
            tick_pos = []
            tick_lab = []

            for i, thr in enumerate(THRESHOLD_ORDER):
                base = i * (n_agg + 1)
                for j, ag in enumerate(OPT_AGG_ORDER):
                    vals = sk[(sk["threshold"] == thr) & (sk["opt_agg"] == ag)]["psnr"]
                    data.append(vals.values if len(vals) else [])
                    positions.append(base + j)
                    colors.append(OPT_AGG_COLORS[ag])
                tick_pos.append(base + 1)
                tick_lab.append(THRESHOLD_LABELS.get(thr, str(thr)))

            bp = ax.boxplot(data, positions=positions, widths=0.7, patch_artist=True,
                            showmeans=False, showfliers=True,
                            flierprops={"marker": "o", "markersize": 3, "alpha": 0.5})
            for patch, c in zip(bp["boxes"], colors):
                patch.set_facecolor(c)
                patch.set_alpha(0.7)

            ax.axhline(30, color="gray", ls=":", lw=0.8, alpha=0.5)
            ax.set_xticks(tick_pos)
            ax.set_xticklabels(tick_lab)
            ax.set_xlabel("Threshold (SSIM)")
            ax.set_ylabel("PSNR (dB, validação, 30 imagens)")
            ax.set_title(f"k = {k}")
            ax.grid(axis="y", alpha=0.3)

            handles = [Patch(facecolor=OPT_AGG_COLORS[a], alpha=0.7, label=OPT_AGG_LABELS[a])
                       for a in OPT_AGG_ORDER]
            handles.append(Line2D([], [], color="gray", ls=":", lw=0.8, label="30 dB (ref.)"))
            ax.legend(handles=handles, fontsize=8, loc="lower left")

        fig.suptitle(f"PSNR por threshold e agregação — patience = {pat}", fontsize=13)
        fig.tight_layout()
        path = Path(outdir) / f"boxplot_psnr_pat{pat}.pdf"
        fig.savefig(path, dpi=DPI)
        plt.close(fig)
        print(f"✔ Salvo: {path}")


# ══════════════════════════════════════════════════════════════════════
# 3.3 — Trade-off qualidade × área
# ══════════════════════════════════════════════════════════════════════

def plot_tradeoff(agg, baselines, outdir, k_filter=None):
    """Trade-off qualidade × área (gráfico central 3.3).

    Eixo X: Economia de recurso (LUT ou FF) em pontos percentuais (pp) do total da FPGA.
    Eixo Y: SSIM mediano na validação.
    Fronteira de Pareto destacada com tooltips de callout nos pontos-chave da fronteira.
    """
    apply_theme()
    sub = agg.copy()
    if k_filter is not None:
        sub = sub[sub["k_size"] == k_filter]
    if sub.empty:
        print("✖ Sem dados para tradeoff."); return

    markers_k = {3: "o", 5: "s"}
    patience_sizes = {0: 45, 230: 85, 350: 140}

    for res, res_col in [("LUT", "LUT_pct"), ("FF", "FF_pct")]:
        fig, ax = plt.subplots(figsize=(10.5, 6.8))

        for _, row in sub.iterrows():
            k = int(row["k_size"])
            ax.scatter(
                row[res_col], row["ssim_median"],
                c=OPT_AGG_COLORS[row["opt_agg"]],
                marker=markers_k[k],
                s=patience_sizes.get(int(row["patience"]), 70),
                edgecolors="#1e293b", linewidths=0.6, alpha=0.82,
                zorder=3,
            )

        # Fronteira de Pareto limpa (deduplicada)
        pts = np.unique(sub[[res_col, "ssim_median"]].dropna().values, axis=0)
        if len(pts) > 0:
            pareto = _pareto_front(pts)
            pareto = pareto[pareto[:, 0].argsort()]
            # Linha de Pareto em escada discreta (step line)
            ax.step(pareto[:, 0], pareto[:, 1], where="post", color="#0f172a",
                    ls="--", lw=1.8, alpha=0.85, label="Fronteira de Pareto", zorder=4)

            # Selecionar pontos-chave da fronteira de Pareto para exibir tooltips com chamada (callout)
            n_pareto = len(pareto)
            if n_pareto <= 5:
                key_indices = list(range(n_pareto))
            else:
                key_indices = sorted(list(set([0, n_pareto - 1, n_pareto // 4, n_pareto // 2, (3 * n_pareto) // 4])))

            offsets = [(-45, 25), (30, -35), (-50, -35), (35, 25), (-30, 30)]

            for idx_count, p_idx in enumerate(key_indices):
                p = pareto[p_idx]
                matching = sub[(np.isclose(sub[res_col], p[0])) & (np.isclose(sub["ssim_median"], p[1]))]
                if matching.empty:
                    continue
                row = matching.iloc[0]
                k_val = int(row["k_size"])
                thr_val = int(row["threshold"])
                opt_val = row["opt_agg"]
                pat_val = int(row["patience"])
                raw_val = row[res]
                bl_val = get_baseline(baselines, k_val)[res]
                rel_red = 100 * (bl_val - raw_val) / bl_val if bl_val > 0 else 0.0

                off = offsets[idx_count % len(offsets)]
                tooltip_txt = (
                    f"T={THRESHOLD_LABELS.get(thr_val, str(thr_val))} (k={k_val}, {OPT_AGG_LABELS[opt_val]}, p={pat_val})\n"
                    f"+{p[0]:.2f} pp (-{rel_red:.1f}% vs bl) | SSIM: {p[1]:.4f}"
                )

                ax.annotate(
                    tooltip_txt,
                    xy=(p[0], p[1]),
                    xytext=off,
                    textcoords="offset points",
                    fontsize=6.8,
                    fontweight="bold",
                    color="#0f172a",
                    bbox=dict(
                        boxstyle="round,pad=0.28,rounding_size=0.3",
                        facecolor="#ffffff",
                        edgecolor="#0f172a",
                        linewidth=0.8,
                        alpha=0.96,
                    ),
                    arrowprops=dict(
                        arrowstyle="->",
                        connectionstyle="arc3,rad=0.15",
                        color="#475569",
                        lw=0.8,
                    ),
                    zorder=10,
                )

        # Guia visual: Direção ideal no canto superior direito
        x_max = sub[res_col].max()
        y_min = sub["ssim_median"].min()
        y_max = sub["ssim_median"].max()
        ax.annotate(
            "↗ Direção Ideal\n(↑ Qualidade, ↑ Economia)",
            xy=(x_max * 0.95, y_max * 0.995),
            xytext=(0, 0),
            textcoords="offset points",
            ha="right",
            va="top",
            fontsize=7.5,
            fontweight="bold",
            color="#047857",
            bbox=dict(
                boxstyle="round,pad=0.3",
                facecolor="#f0fdf4",
                edgecolor="#86efac",
                lw=0.8,
                alpha=0.9,
            ),
            zorder=5,
        )

        # Legenda organizada
        handles = []
        for a in OPT_AGG_ORDER:
            handles.append(Patch(facecolor=OPT_AGG_COLORS[a], edgecolor="#1e293b", label=OPT_AGG_LABELS[a]))
        for k, m in markers_k.items():
            handles.append(Line2D([], [], marker=m, color="#475569", ls="", ms=7,
                                  markeredgecolor="#1e293b", label=f"Kernel {k}×{k}"))
        for p, s in patience_sizes.items():
            handles.append(Line2D([], [], marker="o", color="#475569", ls="", ms=s**0.5,
                                  markeredgecolor="#1e293b", label=f"Patience = {p}"))
        handles.append(Line2D([], [], color="#0f172a", ls="--", lw=1.8, label="Fronteira de Pareto"))

        ax.legend(handles=handles, fontsize=7.5, loc="lower left", framealpha=0.95)
        ax.set_xlabel(f"Economia de {RESOURCE_NAMES[res]} (pontos percentuais do total da FPGA)")
        ax.set_ylabel("SSIM Mediano na Validação (30 imagens)")
        ax.set_title(
            f"Trade-off: Qualidade Visual (SSIM) vs. Economia de {res}\n"
            f"[Tooltips destacam os pontos ótimos de Pareto: economia em pp da FPGA e % de redução relativa ao baseline]",
            pad=12,
        )
        ax.grid(alpha=0.5, linestyle="-", color="#e2e8f0")
        ax.set_ylim(max(0.78, y_min - 0.03), 1.01)

        fig.tight_layout()
        path = Path(outdir) / f"tradeoff_{res.lower()}.pdf"
        fig.savefig(path, dpi=DPI)
        plt.close(fig)
        print(f"✔ Salvo: {path}")


# ══════════════════════════════════════════════════════════════════════
# 3.4 — Economia de recursos vs threshold
# ══════════════════════════════════════════════════════════════════════

def plot_savings(agg, baselines, outdir, k_filter=None):
    """Economia de recursos vs baseline (gráfico 3.4).

    Mostra a economia em pontos percentuais (pp) do total da FPGA
    junto com tooltips flutuantes indicando a % de redução relativa ao baseline do circuito.
    """
    apply_theme()
    sub = agg.copy()
    if k_filter is not None:
        sub = sub[sub["k_size"] == k_filter]
    if sub.empty:
        print("✖ Sem dados para savings."); return

    ks = sorted(sub["k_size"].unique())
    resources = ["LUT", "FF", "DSP"]

    for k in ks:
        sk = sub[sub["k_size"] == k]
        grp = sk.groupby("threshold")
        bl = get_baseline(baselines, k)

        fig, ax = plt.subplots(figsize=(10.5, 5.8))
        thrs = [t for t in THRESHOLD_ORDER if t in grp.groups]
        labels = [THRESHOLD_LABELS.get(t, str(t)) for t in thrs]
        x = np.arange(len(thrs))
        w = 0.24

        max_val = 0
        for i, res in enumerate(resources):
            means = [grp.get_group(t)[f"{res}_pct"].mean() for t in thrs]
            mins = [grp.get_group(t)[f"{res}_pct"].min() for t in thrs]
            maxs = [grp.get_group(t)[f"{res}_pct"].max() for t in thrs]
            rel_pcts = [grp.get_group(t)[f"{res}_rel_pct"].mean() for t in thrs]

            yerr = [np.array(means) - np.array(mins), np.array(maxs) - np.array(means)]
            bars = ax.bar(
                x + (i - 1) * w,
                means,
                width=w,
                label=f"{res} (bl: {bl[res]} un. | {100*bl[res]/FPGA_TOTAL[res]:.2f}% FPGA)",
                color=RESOURCE_COLORS[res],
                yerr=yerr,
                capsize=3,
                edgecolor="white",
                linewidth=0.7,
                alpha=0.9,
                zorder=3,
            )

            # Adicionar badge em estilo tooltip sobre cada barra
            for j, (bx, m, top_err, rel) in enumerate(zip(x + (i - 1) * w, means, maxs, rel_pcts)):
                max_val = max(max_val, top_err, m)
                if m > 0.005:
                    txt = f"+{m:.2f} p.p.\n(-{rel:.1f}%)"
                    add_tooltip_badge(ax, bx, top_err, txt, color=RESOURCE_COLORS[res], fontsize=9, offset=(0, 5))
                else:
                    add_tooltip_badge(ax, bx, 0.0, "0.0 p.p.\n(0%)", color="#94a3b8", fontsize=9, offset=(0, 4))

        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_xlabel("Threshold de Qualidade Exigido")
        ax.set_ylabel("Economia vs. Baseline")
        ax.set_ylim(0, max_val * 1.38 if max_val > 0 else 1.0)
        ax.legend(loc="upper right", framealpha=0.95, fontsize=10)
        ax.grid(axis="y", alpha=0.5, linestyle="-", color="#e2e8f0", zorder=0)

        fig.tight_layout()
        path = Path(outdir) / f"savings_k{k}.pdf"
        fig.savefig(path, dpi=DPI)
        plt.close(fig)
        print(f"✔ Salvo: {path}")

    # Gráfico unificado lado a lado (k=3 e k=5)
    if len(ks) == 2:
        fig_both, axes_both = plt.subplots(1, 2, figsize=(16, 5.8), sharey=True)
        for ax, k in zip(axes_both, ks):
            sk = sub[sub["k_size"] == k]
            grp = sk.groupby("threshold")
            bl = get_baseline(baselines, k)
            thrs = [t for t in THRESHOLD_ORDER if t in grp.groups]
            labels = [THRESHOLD_LABELS.get(t, str(t)) for t in thrs]
            x = np.arange(len(thrs))
            w = 0.24

            for i, res in enumerate(resources):
                means = [grp.get_group(t)[f"{res}_pct"].mean() for t in thrs]
                mins = [grp.get_group(t)[f"{res}_pct"].min() for t in thrs]
                maxs = [grp.get_group(t)[f"{res}_pct"].max() for t in thrs]
                rel_pcts = [grp.get_group(t)[f"{res}_rel_pct"].mean() for t in thrs]
                yerr = [np.array(means) - np.array(mins), np.array(maxs) - np.array(means)]

                ax.bar(
                    x + (i - 1) * w,
                    means,
                    width=w,
                    label=f"{res} (bl: {bl[res]})",
                    color=RESOURCE_COLORS[res],
                    yerr=yerr,
                    capsize=3,
                    edgecolor="white",
                    linewidth=0.7,
                    alpha=0.9,
                    zorder=3,
                )

                for bx, m, top_err, rel in zip(x + (i - 1) * w, means, maxs, rel_pcts):
                    if m > 0.005:
                        add_tooltip_badge(ax, bx, top_err, f"+{m:.2f} p.p.\n(-{rel:.1f}%)",
                                          color=RESOURCE_COLORS[res], fontsize=6.2, offset=(0, 4))
                    else:
                        add_tooltip_badge(ax, bx, 0.0, "0.0\n(0%)", color="#94a3b8", fontsize=5.8, offset=(0, 4))

            ax.set_xticks(x)
            ax.set_xticklabels(labels)
            ax.set_xlabel("Threshold (SSIM Treino)")
            ax.set_title(f"Kernel {k}×{k}", pad=8)
            ax.legend(loc="upper right", fontsize=7.5, framealpha=0.95)
            ax.grid(axis="y", alpha=0.5, linestyle="-", color="#e2e8f0", zorder=0)

        axes_both[0].set_ylabel("Economia vs. Baseline (pp do total da FPGA)")
        fig_both.suptitle("Comparativo de Economia de Recursos (k=3 vs k=5)\n"
                          "[Tooltips: economia em pp da FPGA e % de redução vs baseline correspondente]", fontsize=12.5)
        fig_both.tight_layout()
        path_both = Path(outdir) / "savings_comparison.pdf"
        fig_both.savefig(path_both, dpi=DPI)
        plt.close(fig_both)
        print(f"✔ Salvo: {path_both}")


# ══════════════════════════════════════════════════════════════════════
# 3.5 — Efeito da patience (qualidade)
# ══════════════════════════════════════════════════════════════════════

def plot_patience_quality(agg, outdir, k_filter=None):
    """Efeito da patience na qualidade visual (gráfico 3.5).

    SSIM mediano vs patience (0, 230, 350) para cada agregação,
    com painéis por threshold e tooltips indicando o ganho obtido com patience=350.
    """
    apply_theme()
    sub = agg.copy()
    if k_filter is not None:
        sub = sub[sub["k_size"] == k_filter]
    if sub.empty:
        print("✖ Sem dados para patience_quality."); return

    ks = sorted(sub["k_size"].unique())
    agg_markers = {"media": "o", "geomean": "s", "mediana": "^"}

    for k in ks:
        sk = sub[sub["k_size"] == k]
        thrs = [t for t in THRESHOLD_ORDER if t in sk["threshold"].values]
        n_thr = len(thrs)
        cols = min(3, n_thr)
        rows = (n_thr + cols - 1) // cols
        fig, axes = plt.subplots(rows, cols, figsize=(4.8 * cols, 3.8 * rows), squeeze=False)

        for idx, thr in enumerate(thrs):
            ax = axes[idx // cols][idx % cols]
            st = sk[sk["threshold"] == thr]

            best_gain = None
            best_p350_val = None

            for ag in OPT_AGG_ORDER:
                sa = st[st["opt_agg"] == ag].sort_values("patience")
                if not sa.empty:
                    ax.plot(sa["patience"], sa["ssim_median"], marker=agg_markers[ag],
                            color=OPT_AGG_COLORS[ag], label=OPT_AGG_LABELS[ag],
                            lw=1.6, ms=6, zorder=3)
                    # Faixa com intervalo interquartil (IQR)
                    ax.fill_between(sa["patience"], sa["ssim_q25"], sa["ssim_q75"],
                                    color=OPT_AGG_COLORS[ag], alpha=0.12, zorder=2)

                    # Calcular delta de ganho entre p=0 e p=350
                    if len(sa) >= 2:
                        p0_val = sa[sa["patience"] == 0]["ssim_median"]
                        p350_val = sa[sa["patience"] == 350]["ssim_median"]
                        if not p0_val.empty and not p350_val.empty:
                            gain = p350_val.iloc[0] - p0_val.iloc[0]
                            if best_gain is None or gain > best_gain:
                                best_gain = gain
                                best_p350_val = p350_val.iloc[0]

            # Linha do threshold exigido
            ax.axhline(thr / 100, color="#ef4444", ls="--", lw=1.3, alpha=0.8,
                       label="Threshold exigido", zorder=2)

            # Tooltip de ganho com patience=350
            if best_gain is not None and best_p350_val is not None:
                gain_str = f"Δ(p350): {best_gain:+.4f}" if abs(best_gain) >= 0.0001 else "Δ(p350): neutro"
                badge_bg = "#f0fdf4" if best_gain > 0.0005 else ("#fef2f2" if best_gain < -0.0005 else "#f8fafc")
                badge_edge = "#86efac" if best_gain > 0.0005 else ("#fca5a5" if best_gain < -0.0005 else "#cbd5e1")
                badge_col = "#15803d" if best_gain > 0.0005 else ("#b91c1c" if best_gain < -0.0005 else "#475569")

                ax.annotate(
                    gain_str,
                    xy=(350, best_p350_val),
                    xytext=(-45, 12),
                    textcoords="offset points",
                    fontsize=6.5,
                    fontweight="bold",
                    color=badge_col,
                    bbox=dict(boxstyle="round,pad=0.22", facecolor=badge_bg, edgecolor=badge_edge, lw=0.7, alpha=0.92),
                    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.1", color="#64748b", lw=0.7),
                    zorder=8,
                )

            ax.set_xlabel("Patience")
            ax.set_ylabel("SSIM Mediano")
            ax.set_title(f"Threshold = {THRESHOLD_LABELS.get(thr, str(thr))}", pad=6)
            ax.set_xticks(PATIENCE_VALUES)
            ax.grid(alpha=0.5, linestyle="-", color="#e2e8f0")
            if idx == 0:
                ax.legend(fontsize=7, loc="lower right", framealpha=0.95)

        # Ocultar eixos extras
        for idx in range(n_thr, rows * cols):
            axes[idx // cols][idx % cols].set_visible(False)

        fig.suptitle(f"Efeito da Patience na Qualidade Visual (SSIM) — Kernel {k}×{k}\n"
                     "[Tooltips destacam o ganho de qualidade Δ(p350-p0) alcançado pelo VNS]",
                     fontsize=12)
        fig.tight_layout()
        path = Path(outdir) / f"patience_quality_k{k}.pdf"
        fig.savefig(path, dpi=DPI)
        plt.close(fig)
        print(f"✔ Salvo: {path}")


# ══════════════════════════════════════════════════════════════════════
# 3.6 — Efeito da patience (recursos)
# ══════════════════════════════════════════════════════════════════════

def plot_patience_resources(agg, baselines, outdir, k_filter=None):
    """Efeito da patience no uso de recursos de hardware (gráfico 3.6).

    Recursos agrupados: utilização = (LUT + FF + DSP) / (total LUT + total FF + total DSP) da
    FPGA. O baseline usa a mesma conta (soma dos três recursos do circuito original).

    Mostra a utilização (% do total) vs patience (0, 230, 350) para cada threshold, com a linha
    do baseline e tooltips da economia em pp e % de redução relativa.

    Saída: um gráfico por kernel (patience_resources_k3.pdf e patience_resources_k5.pdf), com a
    legenda fora do gráfico, no canto superior direito da figura.
    """
    apply_theme()
    sub = agg.copy()
    if k_filter is not None:
        sub = sub[sub["k_size"] == k_filter]
    if sub.empty:
        print("✖ Sem dados para patience_resources."); return

    ks = sorted(sub["k_size"].unique())

    RES = ("LUT", "FF", "DSP")
    total = sum(FPGA_TOTAL[r] for r in RES)   # capacidade total: LUT + FF + DSP
    fs = 1.15                                  # escala das fontes de tags e tooltips

    # Seis cores bem distintas entre si, sem vermelho (reservado ao baseline)
    thr_palette = {
        95: "#1d4ed8",  # azul
        90: "#d97706",  # âmbar/laranja
        85: "#059669",  # verde
        80: "#7c3aed",  # roxo
        75: "#0891b2",  # ciano
        70: "#475569",  # cinza-ardósia
    }

    for k in ks:
        sk = sub[sub["k_size"] == k].copy()
        sk["AREA"] = sk[list(RES)].sum(axis=1)   # LUT + FF + DSP de cada config
        thrs = [t for t in THRESHOLD_ORDER if t in sk["threshold"].values]
        bl = get_baseline(baselines, k)

        bl_raw = sum(bl[r] for r in RES)
        bl_pct = 100 * bl_raw / total

        fig, ax = plt.subplots(figsize=(9.4, 5.4))

        # Linha de referência do baseline (valores aparecem na tag ao lado da linha)
        ax.axhline(bl_pct, color="#dc2626", ls="--", lw=1.8, zorder=2)

        # Tag do baseline à esquerda, acima da linha (longe dos tooltips em patience 350)
        ax.annotate(
            f"Baseline: {bl_pct:.2f}%\n({bl_raw} LUT+FF+DSP)",
            xy=(0, bl_pct),
            xytext=(0, 8),
            textcoords="offset points",
            va="bottom",
            ha="left",
            fontsize=7.5 * fs,
            fontweight="bold",
            color="#b91c1c",
            bbox=dict(boxstyle="round,pad=0.22", facecolor="#fef2f2", edgecolor="#ef4444", lw=0.7),
            zorder=6,
        )

        min_curve_pct = bl_pct

        for thr in thrs:
            st = sk[sk["threshold"] == thr].groupby("patience")["AREA"].mean().sort_index()
            curve_pct = 100 * st.values / total
            min_curve_pct = min(min_curve_pct, curve_pct.min())

            color = thr_palette.get(thr, "#3b82f6")
            ax.plot(st.index, curve_pct, "o-", color=color, ms=5.5, lw=1.6, zorder=3)

            # Tooltip para os thresholds extremos (T=95 e T=70) na patience máxima (350)
            if thr in (70, 95):
                val_raw_350 = st.iloc[-1]
                val_pct_350 = curve_pct[-1]
                diff_pp = bl_pct - val_pct_350
                diff_rel = 100 * (bl_raw - val_raw_350) / bl_raw if bl_raw > 0 else 0.0

                # sempre acima do ponto; T=70 deslocado para a esquerda p/ não sobrepor T=95
                offset = (-45, 16 * fs) if thr == 95 else (-150 * fs, 16 * fs)
                tooltip_txt = (
                    f"T={THRESHOLD_LABELS.get(thr, str(thr))} (p=350)\n"
                    f"Economia: +{diff_pp:.2f} pp\n"
                    f"(-{diff_rel:.1f}% vs baseline)"
                )

                ax.annotate(
                    tooltip_txt,
                    xy=(350, val_pct_350),
                    xytext=offset,
                    textcoords="offset points",
                    fontsize=6.8 * fs,
                    fontweight="bold",
                    color="#0f172a",
                    bbox=dict(
                        boxstyle="round,pad=0.25,rounding_size=0.3",
                        facecolor="#ffffff",
                        edgecolor=color,
                        lw=0.8,
                        alpha=0.95,
                    ),
                    arrowprops=dict(
                        arrowstyle="->",
                        connectionstyle="arc3,rad=-0.12",
                        color="#475569",
                        lw=0.8,
                    ),
                    zorder=10,
                )

        # Faixa sombreada de economia de hardware
        ax.axhspan(min_curve_pct, bl_pct, color="#22c55e", alpha=0.06, zorder=1)

        ax.set_xlabel("Paciência")
        ax.set_ylabel("Utilização de LUT + FF + DSP (% do total da FPGA)")
        ax.set_xticks(PATIENCE_VALUES)
        ax.set_xlim(-20, 375)
        ax.set_ylim(min_curve_pct * 0.94, bl_pct * 1.14)
        ax.grid(alpha=0.5, linestyle="-", color="#e2e8f0")

        fig.tight_layout(rect=(0, 0, 0.78, 1))  # faixa à direita reservada p/ a legenda

        # Legenda fora do gráfico, canto superior direito, alinhada ao topo dos eixos
        handles = [Line2D([0], [0], color="#dc2626", ls="--", lw=1.8, label="Baseline")]
        handles += [Line2D([0], [0], color=thr_palette.get(t, "#3b82f6"), marker="o",
                           ms=5.5, lw=1.6, label=f"T = {THRESHOLD_LABELS.get(t, str(t))}")
                    for t in thrs]
        handles.append(Patch(facecolor="#22c55e", alpha=0.15, label="Zona de economia"))
        y_top = ax.get_position().y1
        fig.legend(handles=handles, loc="upper right", bbox_to_anchor=(0.96, y_top + 0.01),
                   bbox_transform=fig.transFigure, fontsize=9,
                   frameon=True, fancybox=True, edgecolor="#1e293b", framealpha=1.0)

        path = Path(outdir) / f"patience_resources_k{k}.pdf"
        fig.savefig(path, dpi=DPI)
        plt.close(fig)
        print(f"✔ Salvo: {path}")


# ══════════════════════════════════════════════════════════════════════
# 3.7 — Taxa de cumprimento do threshold
# ══════════════════════════════════════════════════════════════════════

def plot_compliance(agg, outdir, k_filter=None):
    """Heatmap threshold × opt_agg com a % de imagens que cumprem o threshold,
    um por (k, patience)."""
    sub = agg.copy()
    if k_filter is not None:
        sub = sub[sub["k_size"] == k_filter]
    if sub.empty:
        print("✖ Sem dados para compliance."); return

    ks = sorted(sub["k_size"].unique())
    pats = sorted(sub["patience"].unique())

    for k in ks:
        sk = sub[sub["k_size"] == k]
        for pat in pats:
            sp = sk[sk["patience"] == pat]
            pivot = sp.pivot_table(index="threshold", columns="opt_agg",
                                   values="compliance_rate", aggfunc="mean")
            pivot = pivot.reindex(index=THRESHOLD_ORDER,
                                  columns=OPT_AGG_ORDER)
            pivot = pivot.dropna(how="all")

            fig, ax = plt.subplots(figsize=(7, 5))
            sns.heatmap(pivot, annot=True, fmt=".0%", cmap="RdYlGn", vmin=0, vmax=1,
                        ax=ax,
                        xticklabels=[OPT_AGG_LABELS[a] for a in pivot.columns],
                        yticklabels=[THRESHOLD_LABELS.get(t, str(t)) for t in pivot.index])
            ax.set_xlabel("Agregação")
            ax.set_ylabel("Threshold (SSIM)")
            ax.set_title(f"Taxa de cumprimento — k = {k}, patience = {pat}")
            fig.tight_layout()
            path = Path(outdir) / f"compliance_k{k}_pat{pat}.pdf"
            fig.savefig(path, dpi=DPI)
            plt.close(fig)
            print(f"✔ Salvo: {path}")


# ══════════════════════════════════════════════════════════════════════
# 3.8 — Gap treino × validação
# ══════════════════════════════════════════════════════════════════════

def plot_gap(agg, outdir, k_filter=None):
    """Barras do gap (SSIM treino − SSIM validação mediano) por threshold e opt_agg."""
    sub = agg.copy()
    if k_filter is not None:
        sub = sub[sub["k_size"] == k_filter]
    if sub.empty or sub["train_ssim"].isna().all():
        print("✖ Sem dados de treino para gap."); return

    ks = sorted(sub["k_size"].unique())
    pats = sorted(sub["patience"].unique())

    for k in ks:
        sk = sub[sub["k_size"] == k]
        for pat in pats:
            sp = sk[sk["patience"] == pat]
            fig, ax = plt.subplots(figsize=(9, 5))
            n_agg = len(OPT_AGG_ORDER)
            thrs = [t for t in THRESHOLD_ORDER if t in sp["threshold"].values]
            x = np.arange(len(thrs))
            w = 0.22

            for i, ag in enumerate(OPT_AGG_ORDER):
                gaps = []
                for thr in thrs:
                    row = sp[(sp["threshold"] == thr) & (sp["opt_agg"] == ag)]
                    gaps.append(row["gap_train_val"].iloc[0] if not row.empty else 0)
                ax.bar(x + (i - 1) * w, gaps, width=w, label=OPT_AGG_LABELS[ag],
                       color=OPT_AGG_COLORS[ag])

            ax.axhline(0, color="black", lw=0.5)
            ax.set_xticks(x)
            ax.set_xticklabels([THRESHOLD_LABELS.get(t, str(t)) for t in thrs])
            ax.set_xlabel("Threshold (SSIM)")
            ax.set_ylabel("Gap (SSIM treino − SSIM validação mediano)")
            ax.set_title(f"Gap treino × validação — k = {k}, patience = {pat}")
            ax.legend(fontsize=8)
            ax.grid(axis="y", alpha=0.3)
            fig.tight_layout()
            path = Path(outdir) / f"gap_k{k}_pat{pat}.pdf"
            fig.savefig(path, dpi=DPI)
            plt.close(fig)
            print(f"✔ Salvo: {path}")


# ══════════════════════════════════════════════════════════════════════
# 3.9 — Comparação k=3 vs k=5
# ══════════════════════════════════════════════════════════════════════

def plot_k_comparison(agg, outdir):
    """Comparação k=3 vs k=5 lado a lado: economia de LUT e SSIM mediano."""
    if agg.empty:
        print("✖ Sem dados para k_comparison."); return

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Painel 1: economia de LUT (%)
    ax = axes[0]
    for k in K_SIZES:
        sk = agg[agg["k_size"] == k]
        grp = sk.groupby("threshold")["LUT_pct"].mean()
        grp = grp.reindex(THRESHOLD_ORDER).dropna()
        ax.plot([THRESHOLD_LABELS.get(t, str(t)) for t in grp.index], grp.values,
                "o-", label=f"k = {k}", ms=6)
    ax.set_xlabel("Threshold (SSIM)")
    ax.set_ylabel("Economia de LUT (pp do total da FPGA)")
    ax.set_title("Economia de LUT por kernel")
    ax.legend()
    ax.grid(alpha=0.3)

    # Painel 2: SSIM mediano
    ax = axes[1]
    for k in K_SIZES:
        sk = agg[agg["k_size"] == k]
        grp = sk.groupby("threshold")["ssim_median"].mean()
        grp = grp.reindex(THRESHOLD_ORDER).dropna()
        ax.plot([THRESHOLD_LABELS.get(t, str(t)) for t in grp.index], grp.values,
                "o-", label=f"k = {k}", ms=6)
    ax.set_xlabel("Threshold (SSIM)")
    ax.set_ylabel("SSIM mediano (validação)")
    ax.set_title("Qualidade por kernel")
    ax.legend()
    ax.grid(alpha=0.3)

    fig.suptitle("Comparação k = 3 vs. k = 5", fontsize=13)
    fig.tight_layout()
    path = Path(outdir) / "k_comparison.pdf"
    fig.savefig(path, dpi=DPI)
    plt.close(fig)
    print(f"✔ Salvo: {path}")


# ══════════════════════════════════════════════════════════════════════
# 3.10 — Convergência do VNS
# ══════════════════════════════════════════════════════════════════════

def plot_convergence(history, trace, outdir, k_filter=None):
    """Convergência do VNS: melhor SSIM vs avaliações/iterações por threshold.

    Usa o vns_trace.csv quando disponível (trajetória detalhada), senão
    o vns_history.csv (ponto final apenas).
    """
    if trace.empty and history.empty:
        print("✖ Sem dados de histórico/trace para convergência."); return

    # Se temos trace, usar trace (mais rico)
    if not trace.empty:
        sub = trace.copy()
        if k_filter is not None:
            sub = sub[sub["k_size"] == k_filter]

        ks = sorted(sub["k_size"].unique())
        for k in ks:
            sk = sub[sub["k_size"] == k]
            pats = sorted(sk["patience"].unique())
            thrs_available = sorted(sk["threshold"].unique(), reverse=True)
            # selecionar até 4 thresholds representativos para não poluir
            thrs_show = [t for t in [95, 90, 80, 70] if t in thrs_available] or thrs_available[:4]

            fig, axes = plt.subplots(1, len(pats), figsize=(6 * len(pats), 5), squeeze=False)
            for ax, pat in zip(axes[0], pats):
                sp = sk[sk["patience"] == pat]
                for ag in OPT_AGG_ORDER:
                    sa = sp[sp["opt_agg"] == ag]
                    for thr in thrs_show:
                        st = sa[sa["threshold"] == thr].sort_values("evals")
                        if st.empty:
                            continue
                        label = f"{OPT_AGG_LABELS[ag]}, T={THRESHOLD_LABELS.get(thr, str(thr))}"
                        ax.plot(st["evals"], st["ssim"], "-",
                                color=OPT_AGG_COLORS[ag],
                                alpha=0.7 if thr == 95 else 0.4,
                                lw=1.2 if thr == 95 else 0.8,
                                label=label if thr == 95 else None)
                        # marcador no ponto final
                        ax.plot(st["evals"].iloc[-1], st["ssim"].iloc[-1], "o",
                                color=OPT_AGG_COLORS[ag], ms=4, alpha=0.7)

                ax.set_xlabel("Avaliações")
                ax.set_ylabel("Melhor SSIM")
                ax.set_title(f"patience = {pat}")
                ax.grid(alpha=0.3)
                # legenda simplificada por opt_agg
                handles = [Line2D([], [], color=OPT_AGG_COLORS[a], lw=1.2,
                                  label=OPT_AGG_LABELS[a])
                           for a in OPT_AGG_ORDER]
                ax.legend(handles=handles, fontsize=7)

            fig.suptitle(f"Convergência do VNS (trace) — k = {k}", fontsize=13)
            fig.tight_layout()
            path = Path(outdir) / f"convergence_k{k}.pdf"
            fig.savefig(path, dpi=DPI)
            plt.close(fig)
            print(f"✔ Salvo: {path}")
    else:
        # fallback: usar apenas history (ponto final por threshold)
        sub = history.copy()
        if k_filter is not None:
            sub = sub[sub["k_size"] == k_filter]

        ks = sorted(sub["k_size"].unique())
        for k in ks:
            sk = sub[sub["k_size"] == k]
            pats = sorted(sk["patience"].unique())

            fig, axes = plt.subplots(1, len(pats), figsize=(6 * len(pats), 5), squeeze=False)
            for ax, pat in zip(axes[0], pats):
                sp = sk[sk["patience"] == pat]
                for ag in OPT_AGG_ORDER:
                    sa = sp[sp["opt_agg"] == ag].sort_values("threshold")
                    if sa.empty:
                        continue
                    ax.plot(sa["iterations"], sa["best_ssim"], "o-",
                            color=OPT_AGG_COLORS[ag], label=OPT_AGG_LABELS[ag], ms=5)
                    for _, r in sa.iterrows():
                        ax.annotate(THRESHOLD_LABELS.get(int(r["threshold"]), ""),
                                    (r["iterations"], r["best_ssim"]),
                                    fontsize=6, ha="left", va="bottom")
                ax.set_xlabel("Iterações")
                ax.set_ylabel("Melhor SSIM")
                ax.set_title(f"patience = {pat}")
                ax.legend(fontsize=7)
                ax.grid(alpha=0.3)

            fig.suptitle(f"Convergência do VNS — k = {k}", fontsize=13)
            fig.tight_layout()
            path = Path(outdir) / f"convergence_k{k}.pdf"
            fig.savefig(path, dpi=DPI)
            plt.close(fig)
            print(f"✔ Salvo: {path}")


# ══════════════════════════════════════════════════════════════════════
# 3.11 — Heatmaps de resumo
# ══════════════════════════════════════════════════════════════════════

def plot_heatmaps(agg, outdir, k_filter=None):
    """Heatmaps threshold × opt_agg para SSIM mediano, redução de LUT e
    taxa de cumprimento, um por k_size (média sobre patience)."""
    sub = agg.copy()
    if k_filter is not None:
        sub = sub[sub["k_size"] == k_filter]
    if sub.empty:
        print("✖ Sem dados para heatmaps."); return

    ks = sorted(sub["k_size"].unique())

    metrics = [
        ("ssim_median", "SSIM mediano", "YlGnBu", ".4f", None, None),
        ("LUT_pct", "Economia de LUT (pp da FPGA)", "YlOrRd", ".2f", None, None),
        ("compliance_rate", "Taxa de cumprimento", "RdYlGn", ".0%", 0, 1),
    ]

    for k in ks:
        sk = sub[sub["k_size"] == k]
        # média sobre patience para visão compacta
        avg = sk.groupby(["threshold", "opt_agg"]).mean(numeric_only=True).reset_index()

        for metric, title, cmap, fmt, vmin, vmax in metrics:
            pivot = avg.pivot_table(index="threshold", columns="opt_agg",
                                    values=metric, aggfunc="mean")
            pivot = pivot.reindex(index=THRESHOLD_ORDER,
                                  columns=OPT_AGG_ORDER)
            pivot = pivot.dropna(how="all")

            fig, ax = plt.subplots(figsize=(6, 5))
            sns.heatmap(pivot, annot=True, fmt=fmt, cmap=cmap, vmin=vmin, vmax=vmax,
                        ax=ax,
                        xticklabels=[OPT_AGG_LABELS[a] for a in pivot.columns],
                        yticklabels=[THRESHOLD_LABELS.get(t, str(t)) for t in pivot.index])
            ax.set_xlabel("Agregação")
            ax.set_ylabel("Threshold (SSIM)")
            ax.set_title(f"{title} — k = {k} (média sobre patience)")
            fig.tight_layout()
            safe = metric.replace("_", "").lower()
            path = Path(outdir) / f"heatmap_{safe}_k{k}.pdf"
            fig.savefig(path, dpi=DPI)
            plt.close(fig)
            print(f"✔ Salvo: {path}")



# ══════════════════════════════════════════════════════════════════════
# SSIM médio/mediano da validação × threshold (um gráfico por kernel)
# ══════════════════════════════════════════════════════════════════════

def plot_ssim_threshold(long_val, outdir, k_filter=None):
    """SSIM médio e mediano da validação em função do threshold.

    Considera TODOS os resultados (todas as opt_agg, todas as patiences e
    todas as imagens de validação), agrupados apenas por k e threshold.
    Gera um gráfico por kernel (ssim_threshold_k3.pdf e ssim_threshold_k5.pdf).
    """
    apply_theme()
    sub = long_val.copy()
    if k_filter is not None:
        sub = sub[sub["k_size"] == k_filter]
    if sub.empty:
        print("✖ Sem dados para ssim_threshold."); return

    for k in sorted(sub["k_size"].unique()):
        sk = sub[sub["k_size"] == k]
        stats = (sk.groupby("threshold")["ssim"]
                   .agg(mean="mean", median="median", n="count")
                   .reindex(THRESHOLD_ORDER).dropna(how="all"))
        if stats.empty:
            continue

        x = stats.index.values / 100.0
        fig, ax = plt.subplots(figsize=(8.2, 5.2))

        # Referência: threshold exigido (linha ideal de corte)
        ax.plot(x, x, ls="--", lw=1.6, color="#ef4444", alpha=0.85, label="Threshold exigido (corte)", zorder=2)

        # Curva da Média
        ax.plot(
            x, stats["mean"].values, "o-",
            color="#2563eb", ms=6.5, lw=2.0,
            markerfacecolor="#dbeafe", markeredgecolor="#1d4ed8", markeredgewidth=1.3,
            label="Média", zorder=4
        )

        # Curva da Mediana
        ax.plot(
            x, stats["median"].values, "s-",
            color="#dc2626", ms=6.5, lw=2.0,
            markerfacecolor="#fee2e2", markeredgecolor="#b91c1c", markeredgewidth=1.3,
            label="Mediana", zorder=4
        )

        # Faixa sutil entre média e mediana
        ax.fill_between(x, stats["median"].values, stats["mean"].values, color="#94a3b8", alpha=0.15, zorder=1)

        # Tooltip badges com o valor mediano em cada threshold
        for xv, med_v in zip(x, stats["median"].values):
            txt = f"{med_v:.3f}"
            add_tooltip_badge(
                ax, xv, med_v, txt,
                color="#b91c1c", fontsize=7.5,
                offset=(0, 6), bg_color="#ffffff", alpha=0.95
            )

        ax.set_xlim(0.965, 0.685)  # eixo invertido: mais restritivo (0,95) → menos (0,70)
        ax.set_xticks([t / 100 for t in THRESHOLD_ORDER])
        ax.set_xticklabels([THRESHOLD_LABELS[t] for t in THRESHOLD_ORDER])
        ax.set_xlabel("Threshold Exigido (SSIM)")
        ax.set_ylabel("SSIM na Validação (30 imagens)")

        min_val = min(x.min(), stats["mean"].min(), stats["median"].min())
        y_min = max(0.65, np.floor((min_val - 0.02) * 20) / 20.0)
        ax.set_ylim(y_min, 1.02)
        ax.grid(alpha=0.5, linestyle="-", color="#e2e8f0", zorder=0)

        ax.legend(loc="lower left", fontsize=9, frameon=True, fancybox=True, edgecolor="#cbd5e1", framealpha=0.95)

        fig.tight_layout()
        path = Path(outdir) / f"ssim_threshold_k{k}.pdf"
        fig.savefig(path, dpi=DPI)
        plt.close(fig)
        print(f"✔ Salvo: {path}")


# ══════════════════════════════════════════════════════════════════════
# Tempo total de execução por cenário
# ══════════════════════════════════════════════════════════════════════

K_MARKERS = {3: "o", 5: "s"}                  # forma  → k_size
PATIENCE_SIZES = {0: 100, 230: 100, 350: 100}  # tamanho → patience


def _fmt_hms(seconds: float) -> str:
    """Converte segundos em 'h:mm:ss'."""
    total = int(round(seconds))
    h, rem = divmod(total, 3600)
    m, sec = divmod(rem, 60)
    return f"{h}:{m:02d}:{sec:02d}"


def _hms_ticks(ymax: float, n_target: int = 7) -> np.ndarray:
    """Ticks em múltiplos 'redondos' de tempo (min/h) para o eixo y."""
    steps = [60, 300, 600, 900, 1800, 3600, 7200, 10800, 14400, 21600, 43200, 86400]
    step = next((s for s in steps if ymax / s <= n_target), steps[-1])
    return np.arange(0, ymax + step, step)



def plot_runtime(history, outdir, k_filter=None, opt_agg_filter=None,
                 patience_filter=None):
    """Tempo total de execução (soma de Time_s do vns_history sobre todos os
    thresholds) de cada cenário k × opt_agg × patience.

    Codificação visual:
      cor     → opt_agg
      forma   → k_size (círculo = 3, quadrado = 5)
      tamanho → patience (e agrupamento no eixo x)
    """
    apply_theme()
    if history.empty or "time_s" not in history.columns:
        print("✖ Sem histórico (time_s) para o gráfico de tempo."); return

    sub = _apply_filters(history, k_filter, opt_agg_filter, patience_filter)
    if sub.empty:
        print("✖ Sem dados para o gráfico de tempo."); return

    tot = (sub.groupby(["k_size", "opt_agg", "patience"])["time_s"]
              .sum().reset_index(name="total_s"))

    pats = [p for p in PATIENCE_VALUES if p in tot["patience"].unique()]
    ks = [k for k in K_SIZES if k in tot["k_size"].unique()]
    aggs = [a for a in OPT_AGG_ORDER if a in tot["opt_agg"].unique()]

    # posição x: grupo por patience, deslocamento por (k, opt_agg) dentro do grupo
    combos = [(k, a) for k in ks for a in aggs]
    spacing = 0.13
    offsets = {c: (i - (len(combos) - 1) / 2) * spacing for i, c in enumerate(combos)}

    fig, ax = plt.subplots(figsize=(11.5, 6.8))

    for gi, pat in enumerate(pats):
        if gi % 2 == 0:
            ax.axvspan(gi - 0.5, gi + 0.5, color="#f8fafc", zorder=0)

    ymax = tot["total_s"].max()
    for _, r in tot.iterrows():
        pat, k, ag, val = int(r["patience"]), int(r["k_size"]), r["opt_agg"], r["total_s"]
        x = pats.index(pat) + offsets[(k, ag)]
        # Stem
        ax.vlines(x, 0, val, color=OPT_AGG_EDGES[ag], lw=1.6, alpha=0.7, zorder=2)
        # Ponto
        ax.scatter(
            x, val, marker=K_MARKERS[k], s=PATIENCE_SIZES[pat],
            color=OPT_AGG_FILLS[ag], edgecolor=OPT_AGG_EDGES[ag],
            linewidth=1.4, zorder=3
        )
        # Badge com o tempo
        ax.annotate(
            _fmt_hms(val),
            (x, val),
            xytext=(0, 8),
            textcoords="offset points",
            rotation=90,
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
            color="#0f172a",
            bbox=dict(
                boxstyle="round,pad=0.22,rounding_size=0.3",
                facecolor="#ffffff",
                edgecolor=OPT_AGG_EDGES[ag],
                linewidth=0.75,
                alpha=0.95,
            ),
            zorder=5,
        )

    ticks = _hms_ticks(ymax)
    ax.set_yticks(ticks)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: _fmt_hms(v)))
    ax.set_ylim(0, ymax * 1.25)
    ax.set_xlim(-0.5, len(pats) - 0.5)
    ax.set_xticks(range(len(pats)))
    ax.set_xticklabels([f"Paciência = {p}" for p in pats])
    ax.set_xlabel("Paciência")
    ax.set_ylabel("Tempo Total de Execução (h:mm:ss)")
    ax.grid(axis="y", alpha=0.5, linestyle="-", color="#e2e8f0", zorder=1)
    ax.grid(axis="x", visible=False)

    h_agg = [Patch(facecolor=OPT_AGG_FILLS[a], edgecolor=OPT_AGG_EDGES[a],
                   linewidth=1.2, label=OPT_AGG_LABELS[a]) for a in aggs]
    h_k = [Line2D([], [], marker=K_MARKERS[k], ls="", color="#334155",
                  markerfacecolor="#f1f5f9", markeredgecolor="#334155",
                  markeredgewidth=1.3, ms=7.5, label=f"Kernel {k}×{k}") for k in ks]

    # legendas no nível da figura, acima do gráfico, estilizadas
    fig.legend(
        handles=h_agg, title="Agregação", loc="upper right",
        bbox_to_anchor=(0.49, 0.995), ncol=len(h_agg),
        fontsize=8.5, labelcolor="black",title_fontsize=9, frameon=True, fancybox=True,
        edgecolor="#cbd5e1", framealpha=0.95
    )
    fig.legend(
        handles=h_k, title="Tamanho do kernel", loc="upper left",
        bbox_to_anchor=(0.51, 0.995), ncol=len(h_k),
        fontsize=9.5, labelcolor="black", title_fontsize=10, frameon=True, fancybox=True,
        edgecolor="#cbd5e1", framealpha=0.95
    )

    fig.tight_layout(rect=(0, 0, 1, 0.91))
    suffix = f"_k{k_filter}" if k_filter is not None else ""
    path = Path(outdir) / f"runtime{suffix}.pdf"
    fig.savefig(path, dpi=DPI)
    plt.close(fig)
    print(f"✔ Salvo: {path}")


# ══════════════════════════════════════════════════════════════════════
# Comparação visual das imagens filtradas (95 a 70) de uma solução
# ══════════════════════════════════════════════════════════════════════

class _SlotDispatcher:
    """Aplica uma lista de multiplicadores em ordem row-major sobre os taps do kernel."""
    def __init__(self, fns):
        self.fns = fns
        self.calls = 0

    def __call__(self, a, b):
        fn = self.fns[self.calls % len(self.fns)]
        self.calls += 1
        return fn(a, b)


def plot_comparison(
    solution_dir=None,
    image_path=None,
    outdir="graficos",
    k_filter=None,
    opt_agg_filter=None,
    patience_filter=None,
    root="output",
    sigma=1.0,
):
    """Gera o plot de comparison visual das configurações de threshold (95 a 70).

    Aplica as configurações da solução VNS especificada aos taps do filtro
    Gaussiano sobre uma imagem do dataset, comparando a imagem original,
    a referência exata (multExato) e as imagens com thresholds 95 a 70.
    A legenda de cada foto exibe o SSIM obtido e o threshold (T).
    """
    apply_theme()

    # 1. Resolver diretório da solução
    sol_path = None
    if solution_dir:
        p = Path(solution_dir)
        if p.exists() and p.is_dir():
            sol_path = p
        elif (Path(root) / solution_dir).exists() and (Path(root) / solution_dir).is_dir():
            sol_path = Path(root) / solution_dir

    if sol_path is None:
        k = k_filter or 3
        oa = opt_agg_filter or "media"
        pat = patience_filter if patience_filter is not None else 0
        cand = Path(root) / dir_name(k, oa, pat)
        if cand.exists() and cand.is_dir():
            sol_path = cand
        else:
            dirs = sorted([d for d in Path(root).iterdir() if d.is_dir() and d.name.startswith("vns")])
            if dirs:
                sol_path = dirs[0]

    if sol_path is None or not sol_path.exists():
        print(f"✖ Pasta de solução não encontrada: {solution_dir or '(automática)'}")
        return

    # 2. Resolver caminho da imagem
    img_path = None
    if image_path:
        p = Path(image_path)
        if p.exists() and p.is_file():
            img_path = p
        else:
            for cand in (
                Path("image_dataset/512x512") / image_path,
                Path("image_dataset/512x512") / f"{image_path}.ppm",
                Path("image_dataset/512x512") / f"{image_path}.png",
            ):
                if cand.exists() and cand.is_file():
                    img_path = cand
                    break

    if img_path is None:
        def_img = Path("image_dataset/512x512/71.ppm")
        if def_img.exists():
            img_path = def_img
        else:
            ppms = sorted(Path("image_dataset/512x512").glob("*.ppm"))
            if ppms:
                img_path = ppms[0]

    if img_path is None or not img_path.exists():
        print(f"✖ Imagem não encontrada: {image_path or '(automática)'}")
        return

    from PIL import Image
    from multipliers import get_multiplier
    from gaussian_filter import apply_gaussian_filter, get_gaussian_kernel
    from metrics import calc_ssim

    print(f"── Plot de Comparação ──")
    print(f"   Solução: {sol_path}")
    print(f"   Imagem:  {img_path}")

    # Carregar imagem em escala de cinza
    pil_img = Image.open(img_path).convert("L")
    img_gray = np.array(pil_img, dtype=np.uint8)

    # 3. Ler configurações de threshold de 95 a 70
    threshold_data = []
    k_size = k_filter

    for thr in THRESHOLD_ORDER:
        csv_file = sol_path / f"vns_solution_T{thr}.csv"
        if not csv_file.exists():
            csv_file = sol_path / f"vns_solution_{thr}.csv"
        if not csv_file.exists():
            print(f"   ⚠ Solução para T={thr} não encontrada em {sol_path}, pulando.")
            continue

        with open(csv_file, newline="") as f:
            reader = csv.DictReader(f)
            names = [row["Multiplicador"].strip() for row in reader]

        if k_size is None and names:
            k_size = int(round(np.sqrt(len(names))))

        threshold_data.append((thr, names))

    if not threshold_data:
        print(f"✖ Nenhuma configuração vns_solution_T*.csv encontrada em {sol_path}.")
        return

    if k_size is None:
        k_size = 3

    # 4. Gerar kernel e referência exata
    kernel, norm_factor = get_gaussian_kernel(size=k_size, sigma=sigma)
    exact_fn = get_multiplier("multExato")
    exact_filtered = apply_gaussian_filter(img_gray, exact_fn, kernel=kernel, norm_factor=norm_factor)

    # 5. Filtrar imagem para cada threshold e calcular SSIM
    results = []
    for thr, names in threshold_data:
        disp = _SlotDispatcher([get_multiplier(n) for n in names])
        filt = apply_gaussian_filter(img_gray, disp, kernel=kernel, norm_factor=norm_factor)
        ssim_val = float(calc_ssim(exact_filtered, filt))
        results.append({
            "threshold": thr,
            "names": names,
            "image": filt,
            "ssim": ssim_val,
        })
        print(f"   T={thr:02d} -> SSIM: {ssim_val:.4f}")

    # 6. Montar o grid de comparação (2 linhas x 4 colunas)
    # Dimensões e espaçamento vertical amplo para evitar qualquer sobreposição de títulos entre linhas
    fig, axes = plt.subplots(2, 4, figsize=(16, 9.6))
    fig.subplots_adjust(left=0.04, right=0.96, top=0.93, bottom=0.03, hspace=0.36, wspace=0.14)

    grid_items = [
        {"title": "Imagem Original", "img": img_gray, "badge": "Original (Dataset)", "border": "#64748b"},
        {"title": "Filtro Exato (multExato)", "img": exact_filtered, "badge": "SSIM: 1,0000 (Ref.)", "border": "#059669"},
    ]

    for item in results:
        t = item["threshold"]
        s = item["ssim"]
        t_lbl = THRESHOLD_LABELS.get(t, f"0,{t}")
        met = s >= (t / 100.0)
        border_col = "#059669" if met else "#ef4444"
        grid_items.append({
            "title": f"Threshold {t_lbl}",
            "img": item["image"],
            "badge": f"T = {t_lbl}  |  SSIM: {s:.4f}",
            "border": border_col,
        })

    for idx, cell in enumerate(grid_items):
        if idx >= 8:
            break
        r, c = divmod(idx, 4)
        ax = axes[r, c]
        ax.imshow(cell["img"], cmap="gray")
        ax.axis("off")
        ax.set_title(cell["title"], fontsize=10.5, fontweight="bold", color="#0f172a", pad=8)

        # Badge moderno de legenda sobreposto na base da foto com T e SSIM
        ax.annotate(
            cell["badge"],
            xy=(0.5, 0.04),
            xycoords="axes fraction",
            ha="center",
            va="bottom",
            fontsize=8.5,
            fontweight="bold",
            color="#0f172a",
            bbox=dict(
                boxstyle="round,pad=0.3,rounding_size=0.3",
                facecolor="#ffffff",
                edgecolor=cell["border"],
                linewidth=1.1,
                alpha=0.94,
            ),
            zorder=10,
        )

    for idx in range(len(grid_items), 8):
        r, c = divmod(idx, 4)
        axes[r, c].set_visible(False)

    sol_label = sol_path.name
    img_name = img_path.name

    safe_sol = sol_path.name
    safe_img = img_path.stem
    path_pdf = Path(outdir) / f"comparison_{safe_sol}_{safe_img}.pdf"
    # path_png = Path(outdir) / f"comparison_{safe_sol}_{safe_img}.png"
    main_pdf = Path(outdir) / "comparison.pdf"

    fig.savefig(path_pdf, dpi=DPI)
    # fig.savefig(path_png, dpi=DPI)
    fig.savefig(main_pdf, dpi=DPI)
    plt.close(fig)
    print(f"✔ Salvo: {path_pdf}")
    # print(f"✔ Salvo: {path_png}")
    print(f"✔ Salvo: {main_pdf}")

    # Plot adicional: Mapas de Erro Absoluto (|Exato - Aproximado|)
    if results:
        fig_diff, axes_diff = plt.subplots(2, len(results), figsize=(3.3 * len(results), 7.2), squeeze=False)
        fig_diff.subplots_adjust(left=0.03, right=0.97, top=0.88, bottom=0.04, hspace=0.35, wspace=0.15)
        for j, item in enumerate(results):
            t = item["threshold"]
            s = item["ssim"]
            t_lbl = THRESHOLD_LABELS.get(t, f"0,{t}")
            filt = item["image"]
            diff = np.abs(exact_filtered.astype(np.int32) - filt.astype(np.int32))

            ax_top = axes_diff[0, j]
            ax_top.imshow(filt, cmap="gray")
            ax_top.axis("off")
            ax_top.set_title(f"T = {t_lbl}\nSSIM: {s:.4f}", fontsize=9, fontweight="bold", pad=6)

            ax_bot = axes_diff[1, j]
            ax_bot.imshow(diff, cmap="inferno", vmin=0, vmax=max(int(diff.max()), 1))
            ax_bot.axis("off")
            mae = float(np.mean(diff))
            max_err = int(np.max(diff))
            ax_bot.set_title(f"Erro Absoluto\nMAE: {mae:.2f} | Max: {max_err}", fontsize=8, pad=6)

        fig_diff.suptitle(
            f"Mapas de Erro Absoluto (|Exato − Aproximado|) — {sol_label}  |  {img_name}",
            fontsize=11.5,
            fontweight="bold",
            color="#0f172a",
            y=0.98,
        )
        path_diff_pdf = Path(outdir) / f"comparison_diff_{safe_sol}_{safe_img}.pdf"
        fig_diff.savefig(path_diff_pdf, dpi=DPI)
        plt.close(fig_diff)
        print(f"✔ Salvo: {path_diff_pdf}")


# ══════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════

MODES = {
    "main":               "Principais gráficos do TCC (3.1, 3.3, 3.4, 3.5, 3.6)",
    "stacked":            "Barras empilhadas LUT+FF+DSP por threshold",
    "panels":             "Três subplots (LUT, FF, DSP) lado a lado",
    "normalized":         "% de redução vs baseline por threshold",
    "boxplot":            "Boxplots de SSIM por threshold × opt_agg (3.1)",
    "boxplot_psnr":       "Boxplots de PSNR (ignorado por padrão devido a ruído)",
    "tradeoff":           "Trade-off qualidade × área (3.3)",
    "savings":            "Economia de recursos vs threshold (3.4)",
    "patience_quality":   "Efeito da patience na qualidade (3.5)",
    "patience_resources": "Efeito da patience nos recursos (3.6)",
    "compliance":         "Taxa de cumprimento do threshold",
    "gap":                "Gap treino × validação",
    "k_comparison":       "Comparação k=3 vs k=5",
    "convergence":        "Convergência do VNS",
    "heatmaps":           "Heatmaps de resumo",
    "ssim_threshold":     "SSIM médio/mediano × threshold, um gráfico por k",
    "runtime":            "Tempo total de execução por cenário",
    "comparison":         "Comparação visual das imagens filtradas (95 a 70) de uma solução",
    "all":                "Gerar todos os gráficos (exceto PSNR)",
}

# modos que só precisam do CSV de hardware
HW_MODES = {"stacked", "panels", "normalized"}

# modos que precisam de dados de validação / histórico
VAL_MODES = {"main", "boxplot", "boxplot_psnr", "tradeoff", "savings",
             "patience_quality", "patience_resources", "compliance",
             "gap", "k_comparison", "heatmaps", "convergence",
             "ssim_threshold", "runtime"}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Gera gráficos de recursos FPGA e qualidade (TCC — VNS + truncados)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Modos:\n" + "\n".join(f"  {k:22s} {v}" for k, v in MODES.items()),
    )
    parser.add_argument("mode", choices=MODES.keys(), help="Tipo de gráfico")
    parser.add_argument("--csv", default="configs_encontradas.csv",
                        help="Caminho do CSV de configs (default: configs_encontradas.csv)")
    parser.add_argument("--root", default="output",
                        help="Pasta-raiz das execuções do VNS (default: output)")
    parser.add_argument("--outdir", default="graficos",
                        help="Pasta de saída dos gráficos (default: graficos)")
    parser.add_argument("--k", type=int, default=None, dest="k_filter",
                        choices=[3, 5], help="Filtrar por k_size (3 ou 5)")
    parser.add_argument("--opt-agg", default=None, dest="opt_agg_filter",
                        choices=["media", "geomean", "mediana"],
                        help="Filtrar por opt_agg")
    parser.add_argument("--patience", type=int, default=None, dest="patience_filter",
                        choices=[0, 230, 350], help="Filtrar por patience")
    parser.add_argument("--solution", "--sol", default=None, dest="solution_dir",
                        help="Pasta da solução do VNS em output/ (ex: output/vns3Media0 ou vns3Media0)")
    parser.add_argument("--image", "-i", default=None, dest="image_path",
                        help="Caminho ou nome da imagem do dataset (ex: image_dataset/512x512/71.ppm ou 71.ppm)")
    parser.add_argument("--sigma", type=float, default=1.0,
                        help="Sigma do filtro gaussiano (default: 1.0)")
    return parser.parse_args()


def main():
    args = parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    configs, baselines = None, None
    if args.mode != "comparison":
        configs, baselines = load_configs(args.csv)

    need_val = (args.mode in VAL_MODES or args.mode in ("all", "main")) and args.mode != "comparison"
    long_val = pd.DataFrame()
    history = pd.DataFrame()
    trace = pd.DataFrame()
    agg = pd.DataFrame()

    if need_val:
        print("── Carregando validações ──")
        long_val = build_long_validation(args.root)
        history = build_long_history(args.root)
        trace = build_long_trace(args.root)
        print(f"   {len(long_val)} linhas de validação carregadas.")
        if not history.empty:
            print(f"   {len(history)} linhas de histórico carregadas.")
        if not trace.empty:
            print(f"   {len(trace)} linhas de trace carregadas.")

        print("\n── Verificações ──")
        run_checks(long_val, configs, args.root)

        print("\n── Montando tabela agregada ──")
        agg = build_aggregated(long_val, configs, baselines, history)
        print(f"   {len(agg)} configs agregadas.")

    print(f"\n── Gerando gráfico(s): {args.mode} ──\n")

    k = args.k_filter
    oa = args.opt_agg_filter
    pat = args.patience_filter

    if args.mode in ("stacked", "all"):
        plot_stacked(configs, baselines, args.outdir, k, oa, pat)
    if args.mode in ("panels", "all"):
        plot_panels(configs, baselines, args.outdir, k, oa, pat)
    if args.mode in ("normalized", "all"):
        plot_normalized(configs, baselines, args.outdir, k, oa, pat)
    if args.mode in ("boxplot", "main", "all"):
        plot_boxplot_ssim(agg, long_val, history, args.outdir, k, pat)
    if args.mode == ("boxplot_psnr", "all"):
        plot_boxplot_psnr(agg, long_val, args.outdir, k, pat)
    if args.mode in ("tradeoff", "all"):
        plot_tradeoff(agg, baselines, args.outdir, k)
    if args.mode in ("savings", "main", "all"):
        plot_savings(agg, baselines, args.outdir, k)
    if args.mode in ("patience_quality", "main", "all"):
        plot_patience_quality(agg, args.outdir, k)
    if args.mode in ("patience_resources", "main", "all"):
        plot_patience_resources(agg, baselines, args.outdir, k)
    if args.mode in ("compliance", "all"):
        plot_compliance(agg, args.outdir, k)
    if args.mode in ("gap", "all"):
        plot_gap(agg, args.outdir, k)
    if args.mode in ("k_comparison", "all"):
        plot_k_comparison(agg, args.outdir)
    if args.mode in ("convergence", "all"):
        plot_convergence(history, trace, args.outdir, k)
    if args.mode in ("heatmaps", "all"):
        plot_heatmaps(agg, args.outdir, k)
    if args.mode in ("ssim_threshold", "main", "all"):
        plot_ssim_threshold(long_val, args.outdir, k)
    if args.mode in ("runtime", "main", "all"):
        plot_runtime(history, args.outdir, k, oa, pat)
    if args.mode in ("comparison", "all"):
        plot_comparison(
            solution_dir=args.solution_dir,
            image_path=args.image_path,
            outdir=args.outdir,
            k_filter=k,
            opt_agg_filter=oa,
            patience_filter=pat,
            root=args.root,
            sigma=args.sigma,
        )

    print("\n✔ Concluído.")


if __name__ == "__main__":
    main()