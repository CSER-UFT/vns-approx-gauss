# ==============================================================================
# run_hls3.tcl - Vitis HLS Synthesis Script for 3x3 VNS-Optimized Gaussian Filter
# ==============================================================================
# Target: xc7s50csga324-1, 10 ns clock (100 MHz)
# Top-level: gaussian (3x3 kernel, 512x512 image)
#
# Usage:
#   vitis_hls -f run_hls3.tcl [path_to_vns_solution.csv]
#
# Examples:
#   vitis_hls -f run_hls3.tcl output/vns3GeoMean350/vns_solution_T95.csv
#   export VNS_CSV=output/vns3GeoMean350/vns_solution_T90.csv && vitis_hls -f run_hls3.tcl
# ==============================================================================

# 1. Determine input CSV path
set vns_csv "output/vns3GeoMean350/vns_solution_T95.csv"

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

# Determine solution name based on directory pattern (e.g. vns3GeoMean350) and threshold (e.g. T95)
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
puts "Target Kernel:          3x3 Gaussian Filter (512x512)"
puts "Using VNS Solution CSV: $vns_csv"
puts "HLS Solution Name:      $sol_name"
puts "============================================================"

# 2. Generate C++ mapping and selected multipliers TCL snippet for 3x3
if {[catch {exec python3 generate_vns_mapping.py --kernel-size 3 --csv $vns_csv --header-out vns_mapping_3x3.h --tcl-out selected_multipliers_3x3.tcl} gen_msg]} {
    puts "Error running generate_vns_mapping.py: $gen_msg"
    exit 1
}
puts $gen_msg

# 3. Create and configure Vitis HLS project
file mkdir build
cd build
open_project hls_proj_3x3

set_top gaussian

# Add top-level kernel and mapping header
add_files ../gaussian_vns_3x3.cpp -cflags "-I.. -I../src"
add_files ../vns_mapping_3x3.h

# Add ONLY the multiplier source files selected by VNS
source ../selected_multipliers_3x3.tcl

# Add testbench for csim and cosim
if {[file exists ../tb/tb_gaussian_3x3.cpp]} {
    add_files -tb ../tb/tb_gaussian_3x3.cpp -cflags "-I.. -I../src"
}

open_solution -reset $sol_name
set_part xc7s50csga324-1
create_clock -period 10

# C Simulation
if {[file exists ../tb/tb_gaussian_3x3.cpp]} {
    csim_design
}

# HLS Synthesis
csynth_design

# C/RTL Co-simulation (optional)
# if {[file exists ../tb/tb_gaussian_3x3.cpp]} {
#     cosim_design
# }

# Export Vivado IP Catalog
export_design -format ip_catalog

exit
