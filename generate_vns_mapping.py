#!/usr/bin/env python3
"""
generate_vns_mapping.py

Generates the C++ mapping header (vns_mapping_5x5.h) and TCL file list
(selected_multipliers.tcl) for Vitis HLS synthesis from a VNS solution CSV.

Contract:
- 5x5 Gaussian kernel has 25 taps (all non-zero, sum = 256).
- Row-major slot ordering: slot 0 to 24 correspond to tap(0,0) through tap(4,4).
"""

import argparse
import csv
import os
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

KERNEL_5X5 = [
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


def parse_vns_csv(csv_path: str) -> List[Dict]:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"VNS solution CSV not found: {csv_path}")

    rows = []
    with open(csv_path, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    if len(rows) != 25:
        raise ValueError(
            f"Expected 25 rows in VNS solution CSV for 5x5 kernel, found {len(rows)}."
        )
    return rows


def generate_header(rows: List[Dict], csv_path: str, header_path: str) -> List[str]:
    unique_headers = set()
    unique_cpps = set()
    slot_info = []

    total_lut = 0
    total_ff = 0
    total_dsp = 0

    idx = 0
    for r in range(5):
        for c in range(5):
            expected_w = KERNEL_5X5[r][c]
            row = rows[idx]
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
                "weight": expected_w,
                "mult_name": mult_name,
                "fn_name": fn_name,
                "lut": lut,
                "ff": ff,
                "dsp": dsp,
            })
            idx += 1

    lines = []
    lines.append("/*")
    lines.append(" * AUTO-GENERATED FILE - DO NOT EDIT MANUALLY")
    lines.append(f" * Generated from: {csv_path}")
    lines.append(" * Target: 5x5 VNS-Optimized Gaussian Filter (25 taps)")
    lines.append(f" * Predicted Cost: LUT={total_lut}, FF={total_ff}, DSP={total_dsp}")
    lines.append(" */")
    lines.append("")
    lines.append("#ifndef VNS_MAPPING_5X5_H_")
    lines.append("#define VNS_MAPPING_5X5_H_")
    lines.append("")
    lines.append("#include <ap_int.h>")
    lines.append("")
    lines.append("// Selected approximate multiplier headers")
    for h in sorted(unique_headers):
        lines.append(f'#include "{h}"')
    lines.append("")

    lines.append("// Exact 16-bit adders for balanced adder tree")
    lines.append("inline ap_int<16> add16se_add1(ap_int<16> a, ap_int<16> b) { return a + b; }")
    lines.append("inline ap_int<16> add16se_add2(ap_int<16> a, ap_int<16> b) { return a + b; }")
    lines.append("inline ap_int<16> add16se_add3(ap_int<16> a, ap_int<16> b) { return a + b; }")
    lines.append("inline ap_int<16> add16se_add4(ap_int<16> a, ap_int<16> b) { return a + b; }")
    lines.append("")

    lines.append("// 5x5 Gaussian Kernel Weights (Sum = 256)")
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

    lines.append("#endif // VNS_MAPPING_5X5_H_")
    lines.append("")

    with open(header_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

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
    parser = argparse.ArgumentParser(description="Generate VNS 5x5 HLS mapping and TCL script.")
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
        help="Path to VNS solution CSV (25 rows).",
    )
    parser.add_argument(
        "--header-out",
        type=str,
        default="vns_mapping_5x5.h",
        help="Path for generated C++ header file.",
    )
    parser.add_argument(
        "--tcl-out",
        type=str,
        default="selected_multipliers.tcl",
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

    rows = parse_vns_csv(csv_file)
    unique_cpps = generate_header(rows, csv_file, args.header_out)
    generate_tcl_include(unique_cpps, args.tcl_out)


if __name__ == "__main__":
    main()
