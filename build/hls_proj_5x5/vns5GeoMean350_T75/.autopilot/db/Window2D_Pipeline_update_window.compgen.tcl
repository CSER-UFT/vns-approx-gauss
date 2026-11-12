# This script segment is generated automatically by AutoPilot

# clear list
if {${::AESL::PGuard_autoexp_gen}} {
    cg_default_interface_gen_dc_begin
    cg_default_interface_gen_bundle_begin
    AESL_LIB_XILADAPTER::native_axis_begin
}

# XIL_BRAM:
if {${::AESL::PGuard_autoexp_gen}} {
if {[info proc ::AESL_LIB_XILADAPTER::xil_bram_gen] == "::AESL_LIB_XILADAPTER::xil_bram_gen"} {
eval "::AESL_LIB_XILADAPTER::xil_bram_gen { \
    id 15 \
    name LineBuffer \
    reset_level 1 \
    sync_rst true \
    dir IO \
    corename LineBuffer \
    op interface \
    ports { LineBuffer_address0 { O 9 vector } LineBuffer_ce0 { O 1 bit } LineBuffer_we0 { O 1 bit } LineBuffer_d0 { O 8 vector } LineBuffer_q0 { I 8 vector } } \
} "
} else {
puts "@W \[IMPL-110\] Cannot find bus interface model in the library. Ignored generation of bus interface for 'LineBuffer'"
}
}


# XIL_BRAM:
if {${::AESL::PGuard_autoexp_gen}} {
if {[info proc ::AESL_LIB_XILADAPTER::xil_bram_gen] == "::AESL_LIB_XILADAPTER::xil_bram_gen"} {
eval "::AESL_LIB_XILADAPTER::xil_bram_gen { \
    id 16 \
    name LineBuffer_1 \
    reset_level 1 \
    sync_rst true \
    dir IO \
    corename LineBuffer_1 \
    op interface \
    ports { LineBuffer_1_address0 { O 9 vector } LineBuffer_1_ce0 { O 1 bit } LineBuffer_1_we0 { O 1 bit } LineBuffer_1_d0 { O 8 vector } LineBuffer_1_address1 { O 9 vector } LineBuffer_1_ce1 { O 1 bit } LineBuffer_1_q1 { I 8 vector } } \
} "
} else {
puts "@W \[IMPL-110\] Cannot find bus interface model in the library. Ignored generation of bus interface for 'LineBuffer_1'"
}
}


# XIL_BRAM:
if {${::AESL::PGuard_autoexp_gen}} {
if {[info proc ::AESL_LIB_XILADAPTER::xil_bram_gen] == "::AESL_LIB_XILADAPTER::xil_bram_gen"} {
eval "::AESL_LIB_XILADAPTER::xil_bram_gen { \
    id 17 \
    name LineBuffer_2 \
    reset_level 1 \
    sync_rst true \
    dir IO \
    corename LineBuffer_2 \
    op interface \
    ports { LineBuffer_2_address0 { O 9 vector } LineBuffer_2_ce0 { O 1 bit } LineBuffer_2_we0 { O 1 bit } LineBuffer_2_d0 { O 8 vector } LineBuffer_2_address1 { O 9 vector } LineBuffer_2_ce1 { O 1 bit } LineBuffer_2_q1 { I 8 vector } } \
} "
} else {
puts "@W \[IMPL-110\] Cannot find bus interface model in the library. Ignored generation of bus interface for 'LineBuffer_2'"
}
}


# XIL_BRAM:
if {${::AESL::PGuard_autoexp_gen}} {
if {[info proc ::AESL_LIB_XILADAPTER::xil_bram_gen] == "::AESL_LIB_XILADAPTER::xil_bram_gen"} {
eval "::AESL_LIB_XILADAPTER::xil_bram_gen { \
    id 18 \
    name LineBuffer_3 \
    reset_level 1 \
    sync_rst true \
    dir IO \
    corename LineBuffer_3 \
    op interface \
    ports { LineBuffer_3_address0 { O 9 vector } LineBuffer_3_ce0 { O 1 bit } LineBuffer_3_we0 { O 1 bit } LineBuffer_3_d0 { O 8 vector } LineBuffer_3_address1 { O 9 vector } LineBuffer_3_ce1 { O 1 bit } LineBuffer_3_q1 { I 8 vector } } \
} "
} else {
puts "@W \[IMPL-110\] Cannot find bus interface model in the library. Ignored generation of bus interface for 'LineBuffer_3'"
}
}


# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 14 \
    name num_iterations \
    type other \
    dir I \
    reset_level 1 \
    sync_rst true \
    corename dc_num_iterations \
    op interface \
    ports { num_iterations { I 32 vector } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 19 \
    name sext_ln106 \
    type other \
    dir I \
    reset_level 1 \
    sync_rst true \
    corename dc_sext_ln106 \
    op interface \
    ports { sext_ln106 { I 17 vector } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 20 \
    name zext_ln100_3 \
    type other \
    dir I \
    reset_level 1 \
    sync_rst true \
    corename dc_zext_ln100_3 \
    op interface \
    ports { zext_ln100_3 { I 18 vector } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 21 \
    name num_pixels \
    type other \
    dir I \
    reset_level 1 \
    sync_rst true \
    corename dc_num_pixels \
    op interface \
    ports { num_pixels { I 32 vector } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 22 \
    name pixel_stream3 \
    type fifo \
    dir I \
    reset_level 1 \
    sync_rst true \
    corename dc_pixel_stream3 \
    op interface \
    ports { pixel_stream3_dout { I 8 vector } pixel_stream3_num_data_valid { I 2 vector } pixel_stream3_fifo_cap { I 2 vector } pixel_stream3_empty_n { I 1 bit } pixel_stream3_read { O 1 bit } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id 23 \
    name window_stream \
    type fifo \
    dir O \
    reset_level 1 \
    sync_rst true \
    corename dc_window_stream \
    op interface \
    ports { window_stream_din { O 200 vector } window_stream_num_data_valid { I 2 vector } window_stream_fifo_cap { I 2 vector } window_stream_full_n { I 1 bit } window_stream_write { O 1 bit } } \
} "
}

# Direct connection:
if {${::AESL::PGuard_autoexp_gen}} {
eval "cg_default_interface_gen_dc { \
    id -1 \
    name ap_ctrl \
    type ap_ctrl \
    reset_level 1 \
    sync_rst true \
    corename ap_ctrl \
    op interface \
    ports { ap_start { I 1 bit } ap_ready { O 1 bit } ap_done { O 1 bit } ap_idle { O 1 bit } } \
} "
}


# Adapter definition:
set PortName ap_clk
set DataWd 1 
if {${::AESL::PGuard_autoexp_gen}} {
if {[info proc cg_default_interface_gen_clock] == "cg_default_interface_gen_clock"} {
eval "cg_default_interface_gen_clock { \
    id -2 \
    name ${PortName} \
    reset_level 1 \
    sync_rst true \
    corename apif_ap_clk \
    data_wd ${DataWd} \
    op interface \
}"
} else {
puts "@W \[IMPL-113\] Cannot find bus interface model in the library. Ignored generation of bus interface for '${PortName}'"
}
}


# Adapter definition:
set PortName ap_rst
set DataWd 1 
if {${::AESL::PGuard_autoexp_gen}} {
if {[info proc cg_default_interface_gen_reset] == "cg_default_interface_gen_reset"} {
eval "cg_default_interface_gen_reset { \
    id -3 \
    name ${PortName} \
    reset_level 1 \
    sync_rst true \
    corename apif_ap_rst \
    data_wd ${DataWd} \
    op interface \
}"
} else {
puts "@W \[IMPL-114\] Cannot find bus interface model in the library. Ignored generation of bus interface for '${PortName}'"
}
}



# merge
if {${::AESL::PGuard_autoexp_gen}} {
    cg_default_interface_gen_dc_end
    cg_default_interface_gen_bundle_end
    AESL_LIB_XILADAPTER::native_axis_end
}


# flow_control definition:
set InstName gaussian_flow_control_loop_pipe_sequential_init_U
set CompName gaussian_flow_control_loop_pipe_sequential_init
set name flow_control_loop_pipe_sequential_init
if {${::AESL::PGuard_autocg_gen} && ${::AESL::PGuard_autocg_ipmgen}} {
if {[info proc ::AESL_LIB_VIRTEX::xil_gen_UPC_flow_control] == "::AESL_LIB_VIRTEX::xil_gen_UPC_flow_control"} {
eval "::AESL_LIB_VIRTEX::xil_gen_UPC_flow_control { \
    name ${name} \
    prefix gaussian_ \
}"
} else {
puts "@W \[IMPL-107\] Cannot find ::AESL_LIB_VIRTEX::xil_gen_UPC_flow_control, check your platform lib"
}
}


if {${::AESL::PGuard_rtl_comp_handler}} {
	::AP::rtl_comp_handler $CompName BINDTYPE interface TYPE internal_upc_flow_control INSTNAME $InstName
}


