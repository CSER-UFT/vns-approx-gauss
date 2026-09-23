"""
Main Entry Point: Approximate Multiplier Evaluation on Gaussian Filter Application.
Links Vitis HLS hardware synthesis metrics with image processing accuracy metrics.
"""

import sys
import argparse
from evaluate import run_evaluation


def print_results_table(results):
    """Prints a formatted ASCII table linking hardware and application metrics."""
    headers = [
        "Multiplier", "LUT", "Savings", "FF", "DSP", 
        "PSNR (dB)", "SSIM", "MSE", "MAE", "MaxErr", "ErrRate"
    ]
    
    print("\n" + "=" * 105)
    print(f"{'HARDWARE SYNTHESIS METRICS':<42} | {'APPLICATION QUALITY & ERROR METRICS':<55}")
    print("=" * 105)
    
    row_fmt = "{:<16} | {:>5} | {:>7} | {:>4} | {:>4} || {:>9} | {:>6} | {:>7} | {:>6} | {:>6} | {:>8}"
    print(row_fmt.format(*headers))
    print("-" * 105)
    
    for r in results:
        savings = f"{r['LUT Savings (%)']:.1f}%" if r['LUT Savings (%)'] > 0 else "-"
        psnr_str = f"{r['PSNR (dB)']:.2f}" if r['PSNR (dB)'] != float('inf') else "inf (ref)"
        err_rate = f"{r['Error Rate (%)']:.1f}%"
        
        print(row_fmt.format(
            r['Multiplier'],
            r['LUT'],
            savings,
            r['FF'],
            r['DSP'],
            psnr_str,
            f"{r['SSIM']:.4f}",
            f"{r['MSE']:.3f}",
            f"{r['MAE']:.3f}",
            r['Max Error'],
            err_rate
        ))
    print("=" * 105 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate Approximate Multipliers from Vitis HLS on Gaussian Filter"
    )
    parser.add_argument(
        "--image", "-i", type=str, default=None,
        help="Path to input test image (PNG, JPG, etc.). If omitted, a synthetic pattern is used."
    )
    parser.add_argument(
        "--csv", "-c", type=str, default="metrics_all.csv",
        help="Path to input metrics_all.csv generated from Vitis HLS synthesis (default: metrics_all.csv)"
    )
    parser.add_argument(
        "--output", "-o", type=str, default="output",
        help="Output directory for generated images and reports (default: output)"
    )
    parser.add_argument(
        "--kernel-size", "-k", type=int, default=3, choices=[3, 5, 7],
        help="Gaussian kernel size (default: 3)"
    )
    parser.add_argument(
        "--sigma", "-s", type=float, default=1.0,
        help="Gaussian sigma parameter (default: 1.0)"
    )
    parser.add_argument(
        "--no-plots", action="store_true",
        help="Disable generating visual comparison and Pareto plots"
    )

    parser.add_argument(
        "--exploit-symmetry", action="store_true",
        help="Enable symmetry exploitation for all multipliers"
    )

    args = parser.parse_args()

    print("=========================================================================")
    print(" Approximate Multipliers & Hardware Metrics Evaluator - Gaussian Filter ")
    print("=========================================================================")
    print(f"Kernel Size: {args.kernel_size}x{args.kernel_size} | Sigma: {args.sigma}")
    print(f"Symmetry Exploitation: {'Enabled' if args.exploit_symmetry else 'Disabled'}")
    print(f"Hardware Metrics Source: {args.csv}")
    print(f"Output Directory: {args.output}/")
    print("-------------------------------------------------------------------------")

    results, exact_img, filtered_imgs = run_evaluation(
        image_path=args.image,
        csv_path=args.csv,
        output_dir=args.output,
        kernel_size=args.kernel_size,
        sigma=args.sigma,
        save_plots=not args.no_plots,
        exploit_symmetry=args.exploit_symmetry
    )

    print_results_table(results)
    print("Evaluation completed successfully!")


if __name__ == "__main__":
    main()
