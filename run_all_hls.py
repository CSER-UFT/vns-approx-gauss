#!/usr/bin/env python3
"""run_all_hls.py

Utility script to automatically run Vitis HLS synthesis for every VNS solution CSV
found under the ``output/`` directory.

Features
--------
* Discovers all ``vns_solution_*.csv`` files (including any baseline CSVs).
* Detects the kernel size (3×3 or 5×5) from the folder name (``vns3`` → ``3``,
  ``vns5`` → ``5``).
* Skips already‑synthesised solutions by checking for the existence of the
  ``gaussian_csynth.rpt`` report under the appropriate build directory.
* Optional ``--dry‑run`` to only list the actions without invoking ``vitis_hls``.
* Optional ``--force`` to re‑run a solution even if a report already exists.
* Optional ``--k-size`` to restrict execution to a specific kernel size.
* Provides a clean, colour‑coded console summary:
  ``[✓]`` – already done, ``[▶]`` – running, ``[✔]`` – success,
  ``[✖]`` – failure.
"""

import argparse
import glob
import os
import subprocess
import sys
from typing import List

# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------

def find_solution_csvs(root: str = "output") -> List[str]:
    """Return a sorted list of all VNS solution CSV files.

    The pattern matches ``vns_solution_*.csv`` inside any sub‑directory of ``root``.
    """
    pattern = os.path.join(root, "**", "vns_solution_*.csv")
    return sorted(glob.glob(pattern, recursive=True))


def infer_kernel_size(csv_path: str) -> int:
    """Infer the kernel size (3 or 5) from the CSV path.

    The convention used throughout the project is that folders containing ``vns3``
    correspond to a 3×3 filter and ``vns5`` to a 5×5 filter.
    """
    lowered = csv_path.lower()
    if "/vns3" in lowered or "vns3" in os.path.basename(os.path.dirname(csv_path)).lower():
        return 3
    return 5


def solution_name(csv_path: str) -> str:
    """Construct the solution name used by the build directories.

    Example::
        csv_path = "output/vns3Media0/vns_solution_T95.csv"
        returns "vns3Media0_T95"
    """
    parent_dir = os.path.basename(os.path.dirname(csv_path))  # e.g. vns3Media0
    file_base = os.path.splitext(os.path.basename(csv_path))[0]  # vns_solution_T95
    # Extract the threshold tag after the ``vns_solution_`` prefix
    if file_base.startswith("vns_solution_"):
        tag = file_base[len("vns_solution_"):]
    else:
        tag = file_base
    return f"{parent_dir}_{tag}"


def report_exists(k_size: int, sol_name: str) -> bool:
    """Check whether the synthesis report already exists.

    The report lives at::
        build/hls_proj_<K>x<K>/<solution_name>/syn/report/gaussian_csynth.rpt
    """
    rpt_path = os.path.join(
        "build",
        f"hls_proj_{k_size}x{k_size}",
        sol_name,
        "syn",
        "report",
        "gaussian_csynth.rpt",
    )
    return os.path.isfile(rpt_path)


def run_vitis_hls(csv_path: str) -> int:
    """Invoke Vitis HLS for a given CSV file.

    Returns the subprocess exit code.
    """
    # ``run_hls.tcl`` auto‑detects the kernel size, so we can always call it.
    cmd = ["vitis_hls", "-f", "run_hls.tcl", csv_path]
    # ``subprocess.run`` forwards the exit code directly.
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    # Forward the command output so the user can see the HLS log.
    sys.stdout.write(result.stdout)
    return result.returncode

# -----------------------------------------------------------------------------
# Main entry point
# -----------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Run Vitis HLS on all VNS solution CSVs.")
    parser.add_argument("--dry-run", action="store_true", help="Only list actions, do not invoke Vitis HLS.")
    parser.add_argument("--force", action="store_true", help="Re‑run even if a synthesis report already exists.")
    parser.add_argument(
        "--k-size",
        type=int,
        choices=[3, 5],
        help="Limit execution to a specific kernel size (3 or 5).",
    )
    args = parser.parse_args()

    csv_files = find_solution_csvs()
    if not csv_files:
        print("[!] No solution CSV files found under 'output/'.")
        sys.exit(1)

    print(f"Found {len(csv_files)} solution CSV file(s).")
    for csv_path in csv_files:
        k_size = infer_kernel_size(csv_path)
        if args.k_size and k_size != args.k_size:
            continue
        sol_name = solution_name(csv_path)
        already_done = report_exists(k_size, sol_name)
        if already_done and not args.force:
            print(f"[✓] {sol_name:<30} (k={k_size}) – already synthesized, skipping.")
            continue
        print(f"[▶] {sol_name:<30} (k={k_size}) – running Vitis HLS ...")
        if args.dry_run:
            print("    (dry‑run) command: vitis_hls -f run_hls.tcl", csv_path)
            continue
        ret = run_vitis_hls(csv_path)
        if ret == 0:
            print(f"[✔] {sol_name} – synthesis completed successfully.")
        else:
            print(f"[✖] {sol_name} – synthesis failed (exit code {ret}).")

if __name__ == "__main__":
    main()
