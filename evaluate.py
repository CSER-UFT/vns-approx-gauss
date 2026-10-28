"""
Gaussian Filter Multiplier Evaluator and Hardware-Metric Linker.
Links Vitis HLS synthesis metrics (LUT, FF, DSP) from metrics_all.csv with
Gaussian filter image quality metrics (PSNR, SSIM, MSE, MAE, Error Rate).
"""

import os
import re
import glob
import csv
from typing import Dict, List, Optional, Tuple
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from multipliers import get_multiplier, MULTIPLIER_REGISTRY
from gaussian_filter import apply_gaussian_filter, get_gaussian_kernel
from metrics import evaluate_image_errors


def create_synthetic_test_image(width: int = 256, height: int = 256) -> np.ndarray:
    """Generates a rich test pattern with edges, smooth gradients, and circles
    for benchmark testing when no external image is provided.
    """
    y, x = np.mgrid[0:height, 0:width]
    
    # Diagonal gradient
    gradient = ((x + y) / (width + height) * 180.0).astype(np.float64)
    
    # Concentric circles
    center_x, center_y = width // 2, height // 2
    dist = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
    circles = (np.sin(dist / 6.0) * 45.0 + 45.0)
    
    # Checkerboard pattern in top-left
    checker = (((x // 16) + (y // 16)) % 2) * 50.0
    checker_mask = (x < width // 2) & (y < height // 2)
    
    img = gradient + circles
    img[checker_mask] += checker[checker_mask]
    
    # Add high-frequency grid lines
    img[::32, :] = 255
    img[:, ::32] = 255
    
    return np.clip(img, 0, 255).astype(np.uint8)


def load_hardware_metrics(csv_path: str = "metrics_all.csv", build_dir: str = "build") -> List[Dict]:
    """Loads multiplier hardware metrics from metrics_all.csv and enriches with any
    additional reports found in the build directory.
    """
    entries = {}
    if os.path.exists(csv_path):
        with open(csv_path, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row['Multiplier'].strip()
                entries[name] = {
                    'Multiplier': name,
                    'LUT': int(row['LUT']),
                    'FF': int(row['FF']),
                    'DSP': int(row['DSP']),
                }

    # Also scan build directory for any csynth.rpt not yet in CSV
    rpt_files = glob.glob(os.path.join(build_dir, "**/*_csynth.rpt"), recursive=True)
    for rpt in rpt_files:
        base = os.path.basename(rpt).replace('_csynth.rpt', '')
        if base == 'csynth' or base in entries:
            continue
        try:
            with open(rpt, 'r') as f:
                content = f.read()
            match = re.search(r'\|Total\s*\|\s*\d+\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|', content)
            if match:
                entries[base] = {
                    'Multiplier': base,
                    'LUT': int(match.group(3)),
                    'FF': int(match.group(2)),
                    'DSP': int(match.group(1)),
                }
        except Exception:
            pass

    return list(entries.values())


def run_evaluation(
    image_path: Optional[str] = None,
    csv_path: str = "metrics_all.csv",
    output_dir: str = "output",
    kernel_size: int = 3,
    sigma: float = 1.0,
    save_plots: bool = True
) -> Tuple[List[Dict], np.ndarray, Dict[str, np.ndarray]]:
    """Runs complete Gaussian filter evaluation comparing all approximate multipliers
    against the exact multiplier baseline, linking hardware metrics with application errors.
    """
    os.makedirs(output_dir, exist_ok=True)

    # 1. Load or generate test image
    if image_path and os.path.exists(image_path):
        pil_img = Image.open(image_path).convert('L')
        img = np.array(pil_img, dtype=np.uint8)
        print(f"Loaded test image '{image_path}' ({img.shape[1]}x{img.shape[0]})")
    else:
        img = create_synthetic_test_image(256, 256)
        synthetic_path = os.path.join(output_dir, "input_test_image.png")
        Image.fromarray(img).save(synthetic_path)
        print(f"Generated synthetic test pattern (256x256), saved to {synthetic_path}")

    # 2. Get hardware metrics
    hw_metrics = load_hardware_metrics(csv_path)
    if not hw_metrics:
        print("Warning: No hardware metrics found. Using default registered multipliers.")
        hw_metrics = [
            {'Multiplier': 'multExato', 'LUT': 43, 'FF': 0, 'DSP': 0},
            {'Multiplier': 'p_1bitTruncated', 'LUT': 33, 'FF': 0, 'DSP': 0},
            {'Multiplier': 'p_2bitTruncated', 'LUT': 26, 'FF': 0, 'DSP': 0},
        ]

    # Find exact baseline hardware metrics
    exact_entry = next((e for e in hw_metrics if 'exato' in e['Multiplier'].lower() or 'exact' in e['Multiplier'].lower()), None)
    baseline_lut = exact_entry['LUT'] if exact_entry else 43

    # 3. Compute baseline (Exact Multiplier) Gaussian filter
    kernel, norm_factor = get_gaussian_kernel(size=kernel_size, sigma=sigma)
    exact_multiplier_fn = get_multiplier("multExato")
    exact_filtered = apply_gaussian_filter(img, exact_multiplier_fn, kernel=kernel, norm_factor=norm_factor)
    Image.fromarray(exact_filtered).save(os.path.join(output_dir, "filtered_exact.png"))

    filtered_images = {"Exact": exact_filtered}
    comparison_results = []

    # 4. Evaluate each multiplier
    for entry in hw_metrics:
        mult_name = entry['Multiplier']
        try:
            mult_fn = get_multiplier(mult_name)
        except ValueError:
            print(f"Skipping {mult_name}: no Python model found.")
            continue

        # Run Gaussian filter with this multiplier
        filtered = apply_gaussian_filter(img, mult_fn, kernel=kernel, norm_factor=norm_factor)
        filtered_images[mult_name] = filtered
        
        # Save filtered image
        safe_name = re.sub(r'[^\w\-]', '_', mult_name)
        Image.fromarray(filtered).save(os.path.join(output_dir, f"filtered_{safe_name}.png"))
        # Compute application error metrics vs exact
        app_metrics = evaluate_image_errors(exact_filtered, filtered)

        # Compute hardware savings
        lut = entry['LUT']
        lut_savings = ((baseline_lut - lut) / baseline_lut * 100.0) if baseline_lut > 0 else 0.0

        merged = {
            'Multiplier': mult_name,
            'LUT': lut,
            'LUT Savings (%)': round(lut_savings, 2),
            'FF': entry['FF'],
            'DSP': entry['DSP'],
            'PSNR (dB)': app_metrics['PSNR (dB)'],
            'SSIM': app_metrics['SSIM'],
            'MSE': app_metrics['MSE'],
            'RMSE': app_metrics['RMSE'],
            'MAE': app_metrics['MAE'],
            'Max Error': app_metrics['Max Error'],
            'Error Rate (%)': app_metrics['Error Rate (%)'],
        }
        comparison_results.append(merged)

    # 5. Export comprehensive results CSV
    results_csv_path = os.path.join(output_dir, "gaussian_multiplier_comparison.csv")
    fieldnames = list(comparison_results[0].keys())
    with open(results_csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(comparison_results)
    print(f"\nDetailed comparison results saved to: {results_csv_path}")

    # Also update root metrics comparison CSV
    with open("gaussian_multiplier_comparison.csv", 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(comparison_results)

    # 6. Generate visualizations
    if save_plots:
        generate_comparison_plots(img, exact_filtered, filtered_images, comparison_results, output_dir)

    return comparison_results, exact_filtered, filtered_images


def generate_comparison_plots(
    original: np.ndarray,
    exact_filtered: np.ndarray,
    filtered_images: Dict[str, np.ndarray],
    results: List[Dict],
    output_dir: str
):
    """Generates visual comparison figures and Pareto frontier charts."""
    # A. Visual Image & Error Map Comparison
    approx_items = [item for item in results if not ('exato' in item['Multiplier'].lower() or 'exact' in item['Multiplier'].lower())]
    n_approx = len(approx_items)
    if n_approx > 0:
        fig, axes = plt.subplots(n_approx, 4, figsize=(16, 4 * n_approx))
        if n_approx == 1:
            axes = np.expand_dims(axes, 0)

        for idx, item in enumerate(approx_items):
            name = item['Multiplier']
            approx_img = filtered_images[name]
            # Difference map (absolute error amplified by 10x for clear visual inspection)
            diff = np.abs(exact_filtered.astype(np.int32) - approx_img.astype(np.int32))
            diff_amplified = np.clip(diff * 10, 0, 255).astype(np.uint8)

            axes[idx, 0].imshow(original, cmap='gray')
            axes[idx, 0].set_title("Original Input")
            axes[idx, 0].axis('off')

            axes[idx, 1].imshow(exact_filtered, cmap='gray')
            axes[idx, 1].set_title("Exact (multExato)")
            axes[idx, 1].axis('off')

            axes[idx, 2].imshow(approx_img, cmap='gray')
            axes[idx, 2].set_title(f"{name}\nPSNR: {item['PSNR (dB)']} dB | SSIM: {item['SSIM']}")
            axes[idx, 2].axis('off')

            im_diff = axes[idx, 3].imshow(diff, cmap='inferno', vmin=0, vmax=max(np.max(diff), 1))
            axes[idx, 3].set_title(f"Absolute Error Map\nMAE: {item['MAE']} | Max Err: {item['Max Error']}")
            axes[idx, 3].axis('off')
            fig.colorbar(im_diff, ax=axes[idx, 3], fraction=0.046, pad=0.04)

        plt.tight_layout()
        comparison_plot_path = os.path.join(output_dir, "visual_comparison.png")
        plt.savefig(comparison_plot_path, dpi=200)
        plt.close()
        print(f"Visual comparison plot saved to: {comparison_plot_path}")

    # B. Pareto Trade-Off: Hardware (LUTs) vs Quality (PSNR & SSIM)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    luts = [r['LUT'] for r in results]
    psnrs = [r['PSNR (dB)'] for r in results]
    ssims = [r['SSIM'] for r in results]
    names = [r['Multiplier'] for r in results]

    # Replace inf PSNR for plotting
    finite_psnrs = [p if p != float('inf') else 80.0 for p in psnrs]

    # Subplot 1: LUT vs PSNR
    ax1.scatter(luts, finite_psnrs, color='royalblue', s=100, zorder=3)
    for i, txt in enumerate(names):
        p_label = "Exact (inf)" if psnrs[i] == float('inf') else f"{psnrs[i]:.1f} dB"
        ax1.annotate(f"{txt}\n({p_label})", (luts[i], finite_psnrs[i]),
                     textcoords="offset points", xytext=(0, 10), ha='center', fontsize=9)
    ax1.set_xlabel("Hardware Cost (LUTs)", fontweight='bold')
    ax1.set_ylabel("Application Quality - PSNR (dB)", fontweight='bold')
    ax1.set_title("Hardware vs Accuracy: LUTs vs PSNR")
    ax1.grid(True, linestyle='--', alpha=0.6)

    # Subplot 2: LUT vs SSIM
    ax2.scatter(luts, ssims, color='forestgreen', s=100, zorder=3)
    for i, txt in enumerate(names):
        ax2.annotate(f"{txt}\n(SSIM: {ssims[i]:.4f})", (luts[i], ssims[i]),
                     textcoords="offset points", xytext=(0, 10), ha='center', fontsize=9)
    ax2.set_xlabel("Hardware Cost (LUTs)", fontweight='bold')
    ax2.set_ylabel("Application Quality - SSIM", fontweight='bold')
    ax2.set_title("Hardware vs Accuracy: LUTs vs SSIM")
    ax2.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    pareto_path = os.path.join(output_dir, "pareto_tradeoff.png")
    plt.savefig(pareto_path, dpi=200)
    plt.close()
    print(f"Hardware trade-off plot saved to: {pareto_path}")