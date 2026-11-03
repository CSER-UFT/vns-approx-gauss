#!/usr/bin/env python3
"""
generate_vns_mapping.py

Generates the C++ mapping header (vns_mapping_3x3.h or vns_mapping_5x5.h) and
TCL file list (selected_multipliers.tcl) for Vitis HLS synthesis from a VNS solution CSV.

Supports both:
- 3x3 Gaussian kernel (9 taps, row-major slot 0..8)
- 5x5 Gaussian kernel (25 taps, row-major slot 0..24)
"""

import argparse
import csv
import math
import os
import re
import sys
from typing import Dict, List, Tuple

# Multiplier metadata: maps name variants to (header_filename, function_name, cpp_filename)
MULTIPLIER_INFO = {
    "multExato": ("src/multExato.h", "multExato", "src/multExato.cpp"),
    "exact": ("src/multExato.h", "multExato", "src/multExato.cpp"),
    
    "p_1bitTruncated": ("src/1bitTruncated.h", "_1bitTruncated", "src/1bitTruncated.cpp"),
    "1bitTruncated": ("src/1bitTruncated.h", "_1bitTruncated", "src/1bitTruncated.cpp"),
    "_1bitTruncated": ("src/1bitTruncated.h", "_1bitTruncated", "src/1bitTruncated.cpp"),

    "p_2bitTruncated": ("src/2bitTruncated.h", "_2bitTruncated", "src/2bitTruncated.cpp"),
    "2bitTruncated": ("src/2bitTruncated.h", "_2bitTruncated", "src/2bitTruncated.cpp"),
    "_2bitTruncated": ("src/2bitTruncated.h", "_2bitTruncated", "src/2bitTruncated.cpp"),

    "p_3bitTruncated": ("src/3bitTruncated.h", "_3bitTruncated", "src/3bitTruncated.cpp"),
    "3bitTruncated": ("src/3bitTruncated.h", "_3bitTruncated", "src/3bitTruncated.cpp"),
    "_3bitTruncated": ("src/3bitTruncated.h", "_3bitTruncated", "src/3bitTruncated.cpp"),

    "p_4bitTruncated": ("src/4bitTruncated.h", "_4bitTruncated", "src/4bitTruncated.cpp"),
    "4bitTruncated": ("src/4bitTruncated.h", "_4bitTruncated", "src/4bitTruncated.cpp"),
    "_4bitTruncated": ("src/4bitTruncated.h", "_4bitTruncated", "src/4bitTruncated.cpp"),

    "bit1Truncated": ("src/bit1Truncated.h", "bit1Truncated", "src/bit1Truncated.cpp"),
    "p_bit1Truncated": ("src/bit1Truncated.h", "bit1Truncated", "src/bit1Truncated.cpp"),
    "_bit1Truncated": ("src/bit1Truncated.h", "bit1Truncated", "src/bit1Truncated.cpp"),

    "bit2Truncated": ("src/bit2Truncated.h", "bit2Truncated", "src/bit2Truncated.cpp"),
    "p_bit2Truncated": ("src/bit2Truncated.h", "bit2Truncated", "src/bit2Truncated.cpp"),
    "_bit2Truncated": ("src/bit2Truncated.h", "bit2Truncated", "src/bit2Truncated.cpp"),

    "bit3Truncated": ("src/bit3Truncated.h", "bit3Truncated", "src/bit3Truncated.cpp"),
    "p_bit3Truncated": ("src/bit3Truncated.h", "bit3Truncated", "src/bit3Truncated.cpp"),
    "_bit3Truncated": ("src/bit3Truncated.h", "bit3Truncated", "src/bit3Truncated.cpp"),

    "bit4Truncated": ("src/bit4Truncated.h", "bit4Truncated", "src/bit4Truncated.cpp"),
    "p_bit4Truncated": ("src/bit4Truncated.h", "bit4Truncated", "src/bit4Truncated.cpp"),
    "_bit4Truncated": ("src/bit4Truncated.h", "bit4Truncated", "src/bit4Truncated.cpp"),

    "bitEspecifico": ("src/bitEspecifico.h", "bitEspecifico", "src/bitEspecifico.cpp"),
    "p_bitEspecifico": ("src/bitEspecifico.h", "bitEspecifico", "src/bitEspecifico.cpp"),
    "_bitEspecifico": ("src/bitEspecifico.h", "bitEspecifico", "src/bitEspecifico.cpp"),
}

DEFAULT_KERNEL_3X3 = [
    [19, 32, 19],
    [32, 52, 32],
    [19, 32, 19],
]

DEFAULT_KERNEL_5X5 = [
    [1,  4,  6,  4, 1],
    [4, 16, 24, 16, 4],
    [6, 24, 36, 24, 6],
    [4, 16, 24, 16, 4],
    [1,  4,  6,  4, 1],
]


def resolve_multiplier(raw_name: str) -> Tuple[str, str, str]:
    name = raw_name.strip()
    if name in MULTIPLIER_INFO:
        return MULTIPLIER_INFO[name]
    clean = name.lstrip("p_").lstrip("_")
    if clean in MULTIPLIER_INFO:
        return MULTIPLIER_INFO[clean]
    raise ValueError(f"Unknown multiplier '{raw_name}'. Available: {list(MULTIPLIER_INFO.keys())}")


def parse_vns_csv(csv_path: str, expected_k: int = None) -> Tuple[List[Dict], int]:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"VNS solution CSV not found: {csv_path}")

    rows = []
    with open(csv_path, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    n_rows = len(rows)
    if expected_k is not None:
        expected_rows = expected_k * expected_k
        if n_rows != expected_rows:
            raise ValueError(
                f"Expected {expected_rows} rows for {expected_k}x{expected_k} kernel, but found {n_rows} in {csv_path}."
            )
        k_size = expected_k
    else:
        if n_rows == 9:
            k_size = 3
        elif n_rows == 25:
            k_size = 5
        else:
            raise ValueError(
                f"Unsupported row count ({n_rows}) in {csv_path}. Expected 9 (for 3x3) or 25 (for 5x5)."
            )

    return rows, k_size


def generate_header(rows: List[Dict], csv_path: str, k_size: int, header_path: str) -> List[str]:
    unique_headers = set()
    unique_cpps = set()
    slot_info = []

    total_lut = 0
    total_ff = 0
    total_dsp = 0

    default_kernel = DEFAULT_KERNEL_3X3 if k_size == 3 else DEFAULT_KERNEL_5X5

    for idx, row in enumerate(rows):
        pos_str = row.get("Posicao", "")
        # Extract row, col, and weight from Posicao, e.g. "tap(0,1) w=32"
        m_pos = re.search(r'tap\((\d+)\s*,\s*(\d+)\)', pos_str)
        m_w = re.search(r'w=(\d+)', pos_str)

        if m_pos:
            r = int(m_pos.group(1))
            c = int(m_pos.group(2))
        else:
            r = idx // k_size
            c = idx % k_size

        if m_w:
            w = int(m_w.group(1))
        else:
            w = default_kernel[r][c]

        mult_name = row["Multiplicador"]
        lut = int(row.get("LUT", 0))
        ff = int(row.get("FF", 0))
        dsp = int(row.get("DSP", 0))
        total_lut += lut
        total_ff += ff
        total_dsp += dsp

        h_file, fn_name, cpp_file = resolve_multiplier(mult_name)
        unique_headers.add(h_file)
        unique_cpps.add(cpp_file)

        slot_info.append({
            "slot": idx,
            "r": r,
            "c": c,
            "weight": w,
            "mult_name": mult_name,
            "fn_name": fn_name,
            "lut": lut,
            "ff": ff,
            "dsp": dsp,
        })

    kernel_sum = sum(s["weight"] for s in slot_info)
    # Hardware shift and rounding calculation
    is_power_of_2 = (kernel_sum > 0) and (kernel_sum & (kernel_sum - 1) == 0)
    norm_shift = int(math.log2(kernel_sum)) if is_power_of_2 else 8
    norm_offset = 1 << (norm_shift - 1) if norm_shift > 0 else 0

    lines = []
    lines.append("/*")
    lines.append(" * AUTO-GENERATED FILE - DO NOT EDIT MANUALLY")
    lines.append(f" * Generated from: {csv_path}")
    lines.append(f" * Target: {k_size}x{k_size} VNS-Optimized Gaussian Filter ({len(slot_info)} taps)")
    lines.append(f" * Kernel Sum: {kernel_sum} (Norm Shift: >> {norm_shift}, Offset: + {norm_offset})")
    lines.append(f" * Predicted Cost: LUT={total_lut}, FF={total_ff}, DSP={total_dsp}")
    lines.append(" */")
    lines.append("")
    guard_name = f"VNS_MAPPING_{k_size}X{k_size}_H_"
    lines.append(f"#ifndef {guard_name}")
    lines.append(f"#define {guard_name}")
    lines.append("")
    lines.append("#include <ap_int.h>")
    lines.append("")
    lines.append("// Selected approximate multiplier headers")
    for h in sorted(unique_headers):
        lines.append(f'#include "{h}"')
    lines.append("")

    lines.append("// Exact 16-bit signed adders for balanced adder tree")
    lines.append("inline ap_int<16> add16se_add1(ap_int<16> a, ap_int<16> b) { return a + b; }")
    lines.append("inline ap_int<16> add16se_add2(ap_int<16> a, ap_int<16> b) { return a + b; }")
    lines.append("inline ap_int<16> add16se_add3(ap_int<16> a, ap_int<16> b) { return a + b; }")
    lines.append("inline ap_int<16> add16se_add4(ap_int<16> a, ap_int<16> b) { return a + b; }")
    lines.append("")

    lines.append(f"// Normalization parameters (Kernel Sum = {kernel_sum})")
    lines.append(f"constexpr int K_NORM_FACTOR = {kernel_sum};")
    lines.append(f"constexpr int K_NORM_SHIFT  = {norm_shift};")
    lines.append(f"constexpr int K_NORM_OFFSET = {norm_offset};")
    lines.append("")

    lines.append(f"// {k_size}x{k_size} Gaussian Kernel Weights")
    for s in slot_info:
        r, c, w = s["r"], s["c"], s["weight"]
        lines.append(f"constexpr unsigned char K_TAP_{r}_{c} = {w};")
    lines.append("")

    lines.append("// Per-slot multiplier wrapper functions")
    for s in slot_info:
        slot = s["slot"]
        r = s["r"]
        c = s["c"]
        w = s["weight"]
        mult_name = s["mult_name"]
        fn_name = s["fn_name"]
        lines.append(f"// Slot {slot}: tap({r},{c}) w={w} -> {mult_name} ({fn_name})")
        lines.append(f"inline ap_int<16> mul_slot_{slot}(ap_uint<8> a, ap_uint<8> b) {{")
        lines.append(f"    ap_uint<16> res;")
        lines.append(f"    {fn_name}(a, b, res);")
        lines.append(f"    return (ap_int<16>)res;")
        lines.append(f"}}")
        lines.append("")

    lines.append(f"#endif // {guard_name}")
    lines.append("")

    with open(header_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[generate_vns_mapping] Target: {k_size}x{k_size} ({len(slot_info)} taps, sum={kernel_sum})")
    print(f"[generate_vns_mapping] Header written to: {header_path}")
    print(f"[generate_vns_mapping] Predicted HW Cost: LUT={total_lut}, FF={total_ff}, DSP={total_dsp}")
    print(f"[generate_vns_mapping] Unique multiplier IPs: {len(unique_cpps)}")
    return sorted(unique_cpps)


def generate_tcl_include(unique_cpps: List[str], tcl_path: str):
    lines = [
        "# Auto-generated list of multiplier source files selected by VNS",
        "# Sourced from run_hls.tcl inside build/ directory",
    ]
    for cpp in unique_cpps:
        lines.append(f"add_files ../{cpp}")
    lines.append("")

    with open(tcl_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[generate_vns_mapping] TCL snippet written to: {tcl_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate VNS HLS mapping and TCL script (3x3 or 5x5).")
    parser.add_argument(
        "csv_pos",
        nargs="?",
        default=None,
        help="Positional path to VNS solution CSV.",
    )
    parser.add_argument(
        "--csv",
        type=str,
        default=None,
        help="Path to VNS solution CSV (9 rows for 3x3, 25 rows for 5x5).",
    )
    parser.add_argument(
        "--kernel-size", "-k",
        type=int,
        choices=[3, 5],
        default=None,
        help="Kernel size (3 or 5). If omitted, automatically inferred from row count.",
    )
    parser.add_argument(
        "--header-out",
        type=str,
        default=None,
        help="Path for generated C++ header file (defaults to vns_mapping_<K>x<K>.h).",
    )
    parser.add_argument(
        "--tcl-out",
        type=str,
        default=None,
        help="Path for generated TCL script containing add_files for selected multipliers.",
    )

    args, unknown = parser.parse_known_args()
    
    # Resolve CSV path priority: --csv > csv_pos > unknown non-flags > default
    csv_file = args.csv or args.csv_pos
    if not csv_file and unknown:
        for u in unknown:
            if not u.startswith("-") and not u.endswith(".tcl"):
                csv_file = u
                break
    if not csv_file:
        csv_file = "output/vnsSingleSweep/vns_solution_T95.csv"

    rows, k_size = parse_vns_csv(csv_file, expected_k=args.kernel_size)

    # Determine default output filenames based on resolved k_size
    header_out = args.header_out
    if not header_out:
        header_out = f"vns_mapping_{k_size}x{k_size}.h"

    tcl_out = args.tcl_out
    if not tcl_out:
        tcl_out = f"selected_multipliers_{k_size}x{k_size}.tcl" if k_size == 3 else "selected_multipliers.tcl"

    unique_cpps = generate_header(rows, csv_file, k_size, header_out)
    generate_tcl_include(unique_cpps, tcl_out)


if __name__ == "__main__":
    main()
