import argparse
import csv
import os
import random

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

COLORS = {'LUT': '#4C72B0', 'FF': '#DD8452', 'DSP': '#55A868'}
RESOURCES = ['LUT', 'FF', 'DSP']


def load(path):
    """Lê o CSV mantendo a ordem das linhas (baseline, T95, T90, ...)."""
    with open(path, newline='') as f:
        rows = list(csv.DictReader(f))
    labels = [r['Threshold'] for r in rows]
    data = {k: [int(r[k]) for r in rows] for k in RESOURCES}
    return labels, data


def plot_stacked(labels, data, out):
    """Barras empilhadas: altura total = LUT + FF + DSP."""
    fig, ax = plt.subplots(figsize=(8, 5))
    bottom = [0] * len(labels)
    for k in RESOURCES:
        ax.bar(labels, data[k], bottom=bottom, label=k, color=COLORS[k])
        bottom = [b + v for b, v in zip(bottom, data[k])]
    for i, total in enumerate(bottom):
        ax.text(i, total, str(total), ha='center', va='bottom', fontsize=9)
    ax.set_xlabel('Threshold')
    ax.set_ylabel('Recursos (LUT + FF + DSP)')
    ax.set_title('Recursos totais por threshold')
    ax.legend()
    fig.tight_layout()
    fig.savefig(out, dpi=200)


def plot_panels(labels, data, out):
    """Um subgráfico por recurso, cada um na sua própria escala."""
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5), sharex=True)
    for ax, k in zip(axes, RESOURCES):
        bars = ax.bar(labels, data[k], color=COLORS[k])
        ax.bar_label(bars, fontsize=8, padding=2)
        ax.set_title(k)
        ax.set_xlabel('Threshold')
        ax.set_ylabel(f'{k} (unidades)')
        ax.margins(y=0.12)
    fig.suptitle('Recursos por threshold')
    fig.tight_layout()
    fig.savefig(out, dpi=200)


def plot_normalized(labels, data, out):
    """Barras agrupadas: cada recurso relativo ao baseline (baseline = 100%)."""
    n = len(RESOURCES)
    width = 0.8 / n
    fig, ax = plt.subplots(figsize=(9, 5))
    for j, k in enumerate(RESOURCES):
        base = data[k][0]
        vals = [100 * v / base for v in data[k]]
        xs = [i + (j - (n - 1) / 2) * width for i in range(len(labels))]
        bars = ax.bar(xs, vals, width, label=k, color=COLORS[k])
        ax.bar_label(bars, fmt='%.2f', fontsize=7, padding=2)
    ax.axhline(100, color='black', linestyle=':', linewidth=0.8)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_xlabel('Threshold')
    ax.set_ylabel('% em relação ao baseline')
    ax.set_title('Recursos relativos ao baseline')
    ax.set_ylim(80, 105)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out, dpi=200)


def load_validation(path):
    """Lê o CSV de validação por imagem -> {threshold: {'SSIM': [...], 'PSNR': [...]}}."""
    by_thr = {}
    with open(path, newline='') as f:
        for r in csv.DictReader(f):
            d = by_thr.setdefault(float(r['Threshold']), {'SSIM': [], 'PSNR': []})
            d['SSIM'].append(float(r['SSIM']))
            d['PSNR'].append(float(r['PSNR (dB)']))
    return by_thr


def load_history(path):
    """Lê o SSIM final do VNS (treino) por threshold -> {threshold: ssim}."""
    with open(path, newline='') as f:
        return {float(r['Threshold']): float(r['SSIM']) for r in csv.DictReader(f)}


def plot_boxplot(by_thr, hist, metric, out, all_points=False):
    """Boxplot de uma métrica ('SSIM' ou 'PSNR') por threshold.

    Por padrão mostra só os outliers (regra de 1,5 x IQR) como bolinhas; com
    all_points=True desenha também os pontos de todas as imagens.

    No gráfico de SSIM: traço vermelho = threshold exigido; losango preto =
    SSIM do VNS (treino), se o histórico estiver disponível.
    """
    ylabel = {'SSIM': 'SSIM', 'PSNR': 'PSNR (dB)'}[metric]
    thrs = sorted(by_thr, reverse=True)  # do mais restritivo ao menos restritivo
    n_img = len(by_thr[thrs[0]][metric])
    rng = random.Random(0)  # jitter reprodutível

    fig, ax = plt.subplots(figsize=(8, 5))
    data = [by_thr[t][metric] for t in thrs]
    pos = list(range(1, len(thrs) + 1))
    # com all_points=True os outliers já aparecem entre os pontos desenhados abaixo
    ax.boxplot(data, positions=pos, widths=0.5, showfliers=not all_points,
               flierprops={'marker': 'o', 'markersize': 4, 'alpha': 0.7,
                           'markerfacecolor': '#4C72B0', 'markeredgecolor': '#4C72B0'},
               patch_artist=True,
               boxprops={'facecolor': '#DCE6F2', 'edgecolor': '#4C72B0'},
               medianprops={'color': 'black', 'linewidth': 1.5},
               whiskerprops={'color': '#4C72B0'},
               capprops={'color': '#4C72B0'})
    if all_points:
        for x, vals in zip(pos, data):
            ax.scatter([x + rng.uniform(-0.15, 0.15) for _ in vals], vals,
                       s=12, alpha=0.55, color='#4C72B0', zorder=3)
    if metric == 'SSIM':
        for i, t in enumerate(thrs):
            ax.hlines(t, pos[i] - 0.32, pos[i] + 0.32, colors='red',
                      linestyles='--', linewidth=1.3, zorder=4,
                      label='Threshold exigido' if i == 0 else None)
            if hist and t in hist:
                ax.scatter(pos[i], hist[t], marker='D', color='black', zorder=5,
                           label='SSIM do VNS (treino)' if i == 0 else None)
        ax.legend(loc='lower right', fontsize=8)
    ax.set_xticks(pos)
    ax.set_xticklabels([f'{t:.2f}' for t in thrs])
    ax.set_xlabel('Threshold')
    ax.set_ylabel(ylabel)
    ax.set_title(f'{metric} por threshold (n = {n_img} imagens)')
    ax.grid(axis='y', alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=200)


MODES = {'stacked': plot_stacked, 'panels': plot_panels, 'normalized': plot_normalized}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('csv', nargs='?', default='configs_encontradas.csv')
    p.add_argument('--mode', choices=list(MODES) + ['boxplot', 'all'], default='all')
    p.add_argument('--validation', default='vns_validation_per_image.csv',
                   help='CSV de validação por imagem (usado no boxplot)')
    p.add_argument('--history', default='vns_history.csv',
                   help='CSV do histórico do VNS (opcional; marca o SSIM de treino no boxplot)')
    p.add_argument('--todos-pontos', action='store_true',
                   help='boxplot: desenha os pontos de todas as imagens (padrão: só outliers)')
    args = p.parse_args()

    os.makedirs('plots', exist_ok=True)

    # Gráficos de recursos (LUT/FF/DSP)
    if args.mode in MODES or args.mode == 'all':
        labels, data = load(args.csv)
        modes = MODES if args.mode == 'all' else {args.mode: MODES[args.mode]}
        for name, fn in modes.items():
            out = f'plots/plot_{name}.png'
            fn(labels, data, out)
            print(f'Salvo {out}')

    # Boxplot de SSIM e PSNR por threshold
    if args.mode in ('boxplot', 'all'):
        if not os.path.exists(args.validation):
            if args.mode == 'boxplot':
                p.error(f'arquivo não encontrado: {args.validation}')
            print(f'Boxplot ignorado: {args.validation} não encontrado')
        else:
            hist = load_history(args.history) if os.path.exists(args.history) else None
            by_thr = load_validation(args.validation)
            for metric in ('SSIM', 'PSNR'):
                out = f'plots/plot_boxplot_{metric.lower()}.png'
                plot_boxplot(by_thr, hist, metric, out, args.todos_pontos)
                print(f'Salvo {out}')


if __name__ == '__main__':
    main()