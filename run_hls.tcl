# ==============================================================================
# run_hls.tcl - Vitis HLS Synthesis Script for 5x5 VNS-Optimized Gaussian Filter
# ==============================================================================
# Target: xc7s50csga324-1, 10 ns clock (100 MHz)
# Top-level: gaussian
#
# Usage:
#   vitis_hls -f run_hls.tcl [path_to_vns_solution.csv]
#
# Examples:
#   vitis_hls -f run_hls.tcl output/vnsSingleSweep/vns_solution_T95.csv
#   vitis_hls -f run_hls.tcl output/vnsSingleSweep/vns_solution_T90.csv
#   export VNS_CSV=output/vnsSingleSweep/vns_solution_T85.csv && vitis_hls -f run_hls.tcl
# ==============================================================================

# 1. Determine input CSV path
set vns_csv "output/vnsSingleSweep/vns_solution_T95.csv"

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

puts "============================================================"
puts "Using VNS Solution CSV: $vns_csv"
puts "============================================================"

# 2. Generate C++ mapping and selected multipliers TCL snippet
if {[catch {exec python3 generate_vns_mapping.py --csv $vns_csv --header-out vns_mapping_5x5.h --tcl-out selected_multipliers.tcl} gen_msg]} {
    puts "Error running generate_vns_mapping.py: $gen_msg"
    exit 1
}
puts $gen_msg

# 3. Create and configure Vitis HLS project
file mkdir build
cd build
open_project hls_proj

set_top gaussian

# Add top-level kernel and mapping header
add_files ../gaussian_vns_5x5.cpp -cflags "-I.. -I../src"
add_files ../vns_mapping_5x5.h

# Add ONLY the multiplier source files selected by VNS
source ../selected_multipliers.tcl

# Add testbench for csim and cosim
if {[file exists ../tb/tb_gaussian.cpp]} {
    add_files -tb ../tb/tb_gaussian.cpp -cflags "-I.. -I../src"
}

set sol_name [file rootname [file tail $vns_csv]]

open_solution -reset $sol_name
set_part xc7s50csga324-1
create_clock -period 10

# C Simulation
if {[file exists ../tb/tb_gaussian.cpp]} {
    csim_design
}

# HLS Synthesis
csynth_design

# C/RTL Co-simulation
# if {[file exists ../tb/tb_gaussian.cpp]} {
#     cosim_design
# }

# Export Vivado IP Catalog
export_design -format ip_catalog

exit