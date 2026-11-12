set SynModuleInfo {
  {SRCNAME ReadFromMem_Pipeline_read_image MODELNAME ReadFromMem_Pipeline_read_image RTLNAME gaussian_ReadFromMem_Pipeline_read_image
    SUBMODULES {
      {MODELNAME gaussian_flow_control_loop_pipe_sequential_init RTLNAME gaussian_flow_control_loop_pipe_sequential_init BINDTYPE interface TYPE internal_upc_flow_control INSTNAME gaussian_flow_control_loop_pipe_sequential_init_U}
    }
  }
  {SRCNAME ReadFromMem MODELNAME ReadFromMem RTLNAME gaussian_ReadFromMem
    SUBMODULES {
      {MODELNAME gaussian_mul_mul_16ns_16ns_32_4_1 RTLNAME gaussian_mul_mul_16ns_16ns_32_4_1 BINDTYPE op TYPE all IMPL dsp48 LATENCY 3 ALLOW_PRAGMA 1}
    }
  }
  {SRCNAME Window2D_Pipeline_update_window MODELNAME Window2D_Pipeline_update_window RTLNAME gaussian_Window2D_Pipeline_update_window}
  {SRCNAME Window2D MODELNAME Window2D RTLNAME gaussian_Window2D
    SUBMODULES {
      {MODELNAME gaussian_Window2D_LineBuffer_RAM_AUTO_1R1W RTLNAME gaussian_Window2D_LineBuffer_RAM_AUTO_1R1W BINDTYPE storage TYPE ram IMPL auto LATENCY 2 ALLOW_PRAGMA 1}
      {MODELNAME gaussian_Window2D_LineBuffer_1_RAM_AUTO_1R1W RTLNAME gaussian_Window2D_LineBuffer_1_RAM_AUTO_1R1W BINDTYPE storage TYPE ram IMPL auto LATENCY 2 ALLOW_PRAGMA 1}
    }
  }
  {SRCNAME Filter2D_Pipeline_apply_filter_VITIS_LOOP_204_1 MODELNAME Filter2D_Pipeline_apply_filter_VITIS_LOOP_204_1 RTLNAME gaussian_Filter2D_Pipeline_apply_filter_VITIS_LOOP_204_1
    SUBMODULES {
      {MODELNAME gaussian_mul_8ns_7ns_14_1_1 RTLNAME gaussian_mul_8ns_7ns_14_1_1 BINDTYPE op TYPE mul IMPL auto LATENCY 0 ALLOW_PRAGMA 1}
      {MODELNAME gaussian_ama_addmuladd_9ns_9ns_5ns_14ns_15_4_1 RTLNAME gaussian_ama_addmuladd_9ns_9ns_5ns_14ns_15_4_1 BINDTYPE op TYPE all IMPL dsp48 LATENCY 3 ALLOW_PRAGMA 1}
    }
  }
  {SRCNAME Filter2D MODELNAME Filter2D RTLNAME gaussian_Filter2D}
  {SRCNAME WriteToMem_Pipeline_write_image MODELNAME WriteToMem_Pipeline_write_image RTLNAME gaussian_WriteToMem_Pipeline_write_image}
  {SRCNAME WriteToMem MODELNAME WriteToMem RTLNAME gaussian_WriteToMem
    SUBMODULES {
      {MODELNAME gaussian_mul_mul_16ns_10ns_19_4_1 RTLNAME gaussian_mul_mul_16ns_10ns_19_4_1 BINDTYPE op TYPE all IMPL dsp48 LATENCY 3 ALLOW_PRAGMA 1}
    }
  }
  {SRCNAME gaussian MODELNAME gaussian RTLNAME gaussian IS_TOP 1
    SUBMODULES {
      {MODELNAME gaussian_fifo_w8_d2_S RTLNAME gaussian_fifo_w8_d2_S BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME pixel_stream_U}
      {MODELNAME gaussian_fifo_w16_d2_S RTLNAME gaussian_fifo_w16_d2_S BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME height_c12_U}
      {MODELNAME gaussian_fifo_w16_d2_S RTLNAME gaussian_fifo_w16_d2_S BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME width_c14_U}
      {MODELNAME gaussian_fifo_w72_d2_S RTLNAME gaussian_fifo_w72_d2_S BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME window_stream_U}
      {MODELNAME gaussian_fifo_w16_d2_S RTLNAME gaussian_fifo_w16_d2_S BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME height_c11_U}
      {MODELNAME gaussian_fifo_w16_d2_S RTLNAME gaussian_fifo_w16_d2_S BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME width_c13_U}
      {MODELNAME gaussian_fifo_w8_d2_S RTLNAME gaussian_fifo_w8_d2_S BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME output_stream_U}
      {MODELNAME gaussian_fifo_w16_d2_S RTLNAME gaussian_fifo_w16_d2_S BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME height_c_U}
      {MODELNAME gaussian_fifo_w16_d2_S RTLNAME gaussian_fifo_w16_d2_S BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME width_c_U}
      {MODELNAME gaussian_start_for_Window2D_U0 RTLNAME gaussian_start_for_Window2D_U0 BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME start_for_Window2D_U0_U}
      {MODELNAME gaussian_start_for_Filter2D_U0 RTLNAME gaussian_start_for_Filter2D_U0 BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME start_for_Filter2D_U0_U}
      {MODELNAME gaussian_start_for_WriteToMem_U0 RTLNAME gaussian_start_for_WriteToMem_U0 BINDTYPE storage TYPE fifo IMPL srl ALLOW_PRAGMA 1 INSTNAME start_for_WriteToMem_U0_U}
    }
  }
}
