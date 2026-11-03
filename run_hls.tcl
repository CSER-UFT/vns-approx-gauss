# ==============================================================================
# run_hls.tcl - Vitis HLS Synthesis Script for VNS-Optimized Gaussian Filter
# Auto-detects 3x3 or 5x5 based on input CSV.
# ==============================================================================
# Target: xc7s50csga324-1, 10 ns clock (100 MHz)
# Top-level: gaussian (512x512 image)
#
# Usage:
#   vitis_hls -f run_hls.tcl [path_to_vns_solution.csv]
#
# Or use dedicated scripts:
#   vitis_hls -f run_hls3.tcl [path_to_vns_solution_3x3.csv]
#   vitis_hls -f run_hls5.tcl [path_to_vns_solution_5x5.csv]
# ==============================================================================

# 1. Determine input CSV path
set vns_csv "output/vns5GeoMean0/vns_solution_T95.csv"

if {[info exists env(VNS_CSV)] && $env(VNS_CSV) ne ""} {
    set vns_csv $env(VNS_CSV)
} else {
    # Scan argv for user-specified CSV, filtering out vitis_hls flags (-f, etc.) and tcl scripts
    foreach arg $argv {
        if {$arg ne "-f" && ![string match "*.tcl" $arg] && ![string match "-*" $arg]} {
            set vns_csv $arg
            break
        }
    }
}

# Auto-detect kernel size (3x3 vs 5x5)
set k_size 5
if {[string match "*vns3*" $vns_csv] || [string match "*3x3*" $vns_csv]} {
    set k_size 3
}

if {$k_size == 3} {
    set top_cpp "../gaussian_vns_3x3.cpp"
    set mapping_h "vns_mapping_3x3.h"
    set tcl_out "selected_multipliers_3x3.tcl"
    set tb_cpp "../tb/tb_gaussian_3x3.cpp"
} else {
    set top_cpp "../gaussian_vns_5x5.cpp"
    set mapping_h "vns_mapping_5x5.h"
    set tcl_out "selected_multipliers.tcl"
    set tb_cpp "../tb/tb_gaussian.cpp"
}

# Determine solution name based on directory pattern (e.g. vns5GeoMean0) and threshold (e.g. T95)
set file_base [file rootname [file tail $vns_csv]]
set parent_dir [file tail [file dirname [file normalize $vns_csv]]]

if {[regexp {vns_solution_(.+)$} $file_base -> tag]} {
    set threshold_tag $tag
} elseif {[regexp {_(T\d+|baseline)$} $file_base -> tag]} {
    set threshold_tag $tag
} else {
    set threshold_tag $file_base
}

if {[info exists env(SOL_NAME)] && $env(SOL_NAME) ne ""} {
    set sol_name $env(SOL_NAME)
} elseif {[string match "vns*" $parent_dir]} {
    set sol_name "${parent_dir}_${threshold_tag}"
} else {
    set sol_name $file_base
}

puts "============================================================"
puts "Target Kernel:          ${k_size}x${k_size} Gaussian Filter (512x512)"
puts "Using VNS Solution CSV: $vns_csv"
puts "HLS Solution Name:      $sol_name"
puts "============================================================"

# 2. Generate C++ mapping and selected multipliers TCL snippet
if {[catch {exec python3 generate_vns_mapping.py --kernel-size $k_size --csv $vns_csv --header-out $mapping_h --tcl-out $tcl_out} gen_msg]} {
    puts "Error running generate_vns_mapping.py: $gen_msg"
    exit 1
}
puts $gen_msg

# 3. Create and configure Vitis HLS project (separated by kernel size to avoid file collisions)
file mkdir build
cd build
set proj_name "hls_proj_${k_size}x${k_size}"
open_project $proj_name

set_top gaussian

# Add top-level kernel and mapping header
add_files $top_cpp -cflags "-I.. -I../src"
add_files ../$mapping_h

# Add ONLY the multiplier source files selected by VNS
source ../$tcl_out

# Add testbench for csim and cosim
if {[file exists $tb_cpp]} {
    add_files -tb $tb_cpp -cflags "-I.. -I../src"
}

open_solution -reset $sol_name
set_part xc7s50csga324-1
create_clock -period 10

# C Simulation
if {[file exists $tb_cpp]} {
    csim_design
}

# HLS Synthesis
csynth_design

# C/RTL Co-simulation (optional)
# if {[file exists $tb_cpp]} {
#     cosim_design
# }

# Export Vivado IP Catalog
export_design -format ip_catalog

exit
