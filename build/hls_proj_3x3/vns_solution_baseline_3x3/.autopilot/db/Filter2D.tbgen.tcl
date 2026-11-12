set moduleName Filter2D
set isTopModule 0
set isCombinational 0
set isDatapathOnly 0
set isPipelined 0
set pipeline_type none
set FunctionProtocol ap_ctrl_none
set isOneStateSeq 0
set ProfileFlag 0
set StallSigGenFlag 0
set isEnableWaveformDebug 1
set hasInterrupt 0
set C_modelName {Filter2D}
set C_modelType { void 0 }
set C_modelArgList {
	{ width int 16 regular {fifo 0}  }
	{ height int 16 regular {fifo 0}  }
	{ window_stream int 72 regular {fifo 0 volatile }  }
	{ output_stream4 int 8 regular {fifo 1 volatile }  }
	{ height_c int 16 regular {fifo 1}  }
	{ width_c int 16 regular {fifo 1}  }
}
set C_modelArgMapList {[ 
	{ "Name" : "width", "interface" : "fifo", "bitwidth" : 16, "direction" : "READONLY"} , 
 	{ "Name" : "height", "interface" : "fifo", "bitwidth" : 16, "direction" : "READONLY"} , 
 	{ "Name" : "window_stream", "interface" : "fifo", "bitwidth" : 72, "direction" : "READONLY"} , 
 	{ "Name" : "output_stream4", "interface" : "fifo", "bitwidth" : 8, "direction" : "WRITEONLY"} , 
 	{ "Name" : "height_c", "interface" : "fifo", "bitwidth" : 16, "direction" : "WRITEONLY"} , 
 	{ "Name" : "width_c", "interface" : "fifo", "bitwidth" : 16, "direction" : "WRITEONLY"} ]}
# RTL Port declarations: 
set portNum 40
set portList { 
	{ ap_clk sc_in sc_logic 1 clock -1 } 
	{ ap_rst sc_in sc_logic 1 reset -1 active_high_sync } 
	{ ap_start sc_in sc_logic 1 start -1 } 
	{ start_full_n sc_in sc_logic 1 signal -1 } 
	{ ap_done sc_out sc_logic 1 predone -1 } 
	{ ap_continue sc_in sc_logic 1 continue -1 } 
	{ ap_idle sc_out sc_logic 1 done -1 } 
	{ ap_ready sc_out sc_logic 1 ready -1 } 
	{ start_out sc_out sc_logic 1 signal -1 } 
	{ start_write sc_out sc_logic 1 signal -1 } 
	{ width_dout sc_in sc_lv 16 signal 0 } 
	{ width_num_data_valid sc_in sc_lv 2 signal 0 } 
	{ width_fifo_cap sc_in sc_lv 2 signal 0 } 
	{ width_empty_n sc_in sc_logic 1 signal 0 } 
	{ width_read sc_out sc_logic 1 signal 0 } 
	{ height_dout sc_in sc_lv 16 signal 1 } 
	{ height_num_data_valid sc_in sc_lv 2 signal 1 } 
	{ height_fifo_cap sc_in sc_lv 2 signal 1 } 
	{ height_empty_n sc_in sc_logic 1 signal 1 } 
	{ height_read sc_out sc_logic 1 signal 1 } 
	{ window_stream_dout sc_in sc_lv 72 signal 2 } 
	{ window_stream_num_data_valid sc_in sc_lv 2 signal 2 } 
	{ window_stream_fifo_cap sc_in sc_lv 2 signal 2 } 
	{ window_stream_empty_n sc_in sc_logic 1 signal 2 } 
	{ window_stream_read sc_out sc_logic 1 signal 2 } 
	{ output_stream4_din sc_out sc_lv 8 signal 3 } 
	{ output_stream4_num_data_valid sc_in sc_lv 2 signal 3 } 
	{ output_stream4_fifo_cap sc_in sc_lv 2 signal 3 } 
	{ output_stream4_full_n sc_in sc_logic 1 signal 3 } 
	{ output_stream4_write sc_out sc_logic 1 signal 3 } 
	{ height_c_din sc_out sc_lv 16 signal 4 } 
	{ height_c_num_data_valid sc_in sc_lv 2 signal 4 } 
	{ height_c_fifo_cap sc_in sc_lv 2 signal 4 } 
	{ height_c_full_n sc_in sc_logic 1 signal 4 } 
	{ height_c_write sc_out sc_logic 1 signal 4 } 
	{ width_c_din sc_out sc_lv 16 signal 5 } 
	{ width_c_num_data_valid sc_in sc_lv 2 signal 5 } 
	{ width_c_fifo_cap sc_in sc_lv 2 signal 5 } 
	{ width_c_full_n sc_in sc_logic 1 signal 5 } 
	{ width_c_write sc_out sc_logic 1 signal 5 } 
}
set NewPortList {[ 
	{ "name": "ap_clk", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "clock", "bundle":{"name": "ap_clk", "role": "default" }} , 
 	{ "name": "ap_rst", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "reset", "bundle":{"name": "ap_rst", "role": "default" }} , 
 	{ "name": "ap_start", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "start", "bundle":{"name": "ap_start", "role": "default" }} , 
 	{ "name": "start_full_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "start_full_n", "role": "default" }} , 
 	{ "name": "ap_done", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "predone", "bundle":{"name": "ap_done", "role": "default" }} , 
 	{ "name": "ap_continue", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "continue", "bundle":{"name": "ap_continue", "role": "default" }} , 
 	{ "name": "ap_idle", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "done", "bundle":{"name": "ap_idle", "role": "default" }} , 
 	{ "name": "ap_ready", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "ready", "bundle":{"name": "ap_ready", "role": "default" }} , 
 	{ "name": "start_out", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "start_out", "role": "default" }} , 
 	{ "name": "start_write", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "start_write", "role": "default" }} , 
 	{ "name": "width_dout", "direction": "in", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "width", "role": "dout" }} , 
 	{ "name": "width_num_data_valid", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "width", "role": "num_data_valid" }} , 
 	{ "name": "width_fifo_cap", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "width", "role": "fifo_cap" }} , 
 	{ "name": "width_empty_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "width", "role": "empty_n" }} , 
 	{ "name": "width_read", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "width", "role": "read" }} , 
 	{ "name": "height_dout", "direction": "in", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "height", "role": "dout" }} , 
 	{ "name": "height_num_data_valid", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "height", "role": "num_data_valid" }} , 
 	{ "name": "height_fifo_cap", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "height", "role": "fifo_cap" }} , 
 	{ "name": "height_empty_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "height", "role": "empty_n" }} , 
 	{ "name": "height_read", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "height", "role": "read" }} , 
 	{ "name": "window_stream_dout", "direction": "in", "datatype": "sc_lv", "bitwidth":72, "type": "signal", "bundle":{"name": "window_stream", "role": "dout" }} , 
 	{ "name": "window_stream_num_data_valid", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "window_stream", "role": "num_data_valid" }} , 
 	{ "name": "window_stream_fifo_cap", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "window_stream", "role": "fifo_cap" }} , 
 	{ "name": "window_stream_empty_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "window_stream", "role": "empty_n" }} , 
 	{ "name": "window_stream_read", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "window_stream", "role": "read" }} , 
 	{ "name": "output_stream4_din", "direction": "out", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "output_stream4", "role": "din" }} , 
 	{ "name": "output_stream4_num_data_valid", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "output_stream4", "role": "num_data_valid" }} , 
 	{ "name": "output_stream4_fifo_cap", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "output_stream4", "role": "fifo_cap" }} , 
 	{ "name": "output_stream4_full_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "output_stream4", "role": "full_n" }} , 
 	{ "name": "output_stream4_write", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "output_stream4", "role": "write" }} , 
 	{ "name": "height_c_din", "direction": "out", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "height_c", "role": "din" }} , 
 	{ "name": "height_c_num_data_valid", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "height_c", "role": "num_data_valid" }} , 
 	{ "name": "height_c_fifo_cap", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "height_c", "role": "fifo_cap" }} , 
 	{ "name": "height_c_full_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "height_c", "role": "full_n" }} , 
 	{ "name": "height_c_write", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "height_c", "role": "write" }} , 
 	{ "name": "width_c_din", "direction": "out", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "width_c", "role": "din" }} , 
 	{ "name": "width_c_num_data_valid", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "width_c", "role": "num_data_valid" }} , 
 	{ "name": "width_c_fifo_cap", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "width_c", "role": "fifo_cap" }} , 
 	{ "name": "width_c_full_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "width_c", "role": "full_n" }} , 
 	{ "name": "width_c_write", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "width_c", "role": "write" }}  ]}

set RtlHierarchyInfo {[
	{"ID" : "0", "Level" : "0", "Path" : "`AUTOTB_DUT_INST", "Parent" : "", "Child" : ["1", "5"],
		"CDFG" : "Filter2D",
		"Protocol" : "ap_ctrl_none",
		"ControlExist" : "1", "ap_start" : "1", "ap_ready" : "1", "ap_done" : "1", "ap_continue" : "1", "ap_idle" : "1", "real_start" : "1",
		"Pipeline" : "None", "UnalignedPipeline" : "0", "RewindPipeline" : "0", "ProcessNetwork" : "0",
		"II" : "0",
		"VariableLatency" : "1", "ExactLatency" : "-1", "EstimateLatencyMin" : "7", "EstimateLatencyMax" : "4294836237",
		"Combinational" : "0",
		"Datapath" : "0",
		"ClockEnable" : "0",
		"HasSubDataflow" : "0",
		"InDataflowNetwork" : "1",
		"HasNonBlockingOperation" : "0",
		"IsBlackBox" : "0",
		"Port" : [
			{"Name" : "width", "Type" : "Fifo", "Direction" : "I", "DependentProc" : ["0"], "DependentChan" : "0", "DependentChanDepth" : "2", "DependentChanType" : "2",
				"BlockSignal" : [
					{"Name" : "width_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "height", "Type" : "Fifo", "Direction" : "I", "DependentProc" : ["0"], "DependentChan" : "0", "DependentChanDepth" : "2", "DependentChanType" : "2",
				"BlockSignal" : [
					{"Name" : "height_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "window_stream", "Type" : "Fifo", "Direction" : "I", "DependentProc" : ["0"], "DependentChan" : "0", "DependentChanDepth" : "2", "DependentChanType" : "0",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "grp_Filter2D_Pipeline_apply_filter_VITIS_LOOP_204_1_fu_72", "Port" : "window_stream", "Inst_start_state" : "5", "Inst_end_state" : "6"}]},
			{"Name" : "output_stream4", "Type" : "Fifo", "Direction" : "O", "DependentProc" : ["0"], "DependentChan" : "0", "DependentChanDepth" : "2", "DependentChanType" : "0",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "grp_Filter2D_Pipeline_apply_filter_VITIS_LOOP_204_1_fu_72", "Port" : "output_stream4", "Inst_start_state" : "5", "Inst_end_state" : "6"}]},
			{"Name" : "height_c", "Type" : "Fifo", "Direction" : "O", "DependentProc" : ["0"], "DependentChan" : "0", "DependentChanDepth" : "2", "DependentChanType" : "2",
				"BlockSignal" : [
					{"Name" : "height_c_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "width_c", "Type" : "Fifo", "Direction" : "O", "DependentProc" : ["0"], "DependentChan" : "0", "DependentChanDepth" : "2", "DependentChanType" : "2",
				"BlockSignal" : [
					{"Name" : "width_c_blk_n", "Type" : "RtlSignal"}]}]},
	{"ID" : "1", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.grp_Filter2D_Pipeline_apply_filter_VITIS_LOOP_204_1_fu_72", "Parent" : "0", "Child" : ["2", "3", "4"],
		"CDFG" : "Filter2D_Pipeline_apply_filter_VITIS_LOOP_204_1",
		"Protocol" : "ap_ctrl_hs",
		"ControlExist" : "1", "ap_start" : "1", "ap_ready" : "1", "ap_done" : "1", "ap_continue" : "0", "ap_idle" : "1", "real_start" : "0",
		"Pipeline" : "None", "UnalignedPipeline" : "0", "RewindPipeline" : "0", "ProcessNetwork" : "0",
		"II" : "0",
		"VariableLatency" : "1", "ExactLatency" : "-1", "EstimateLatencyMin" : "2", "EstimateLatencyMax" : "4294836232",
		"Combinational" : "0",
		"Datapath" : "0",
		"ClockEnable" : "0",
		"HasSubDataflow" : "0",
		"InDataflowNetwork" : "0",
		"HasNonBlockingOperation" : "0",
		"IsBlackBox" : "0",
		"Port" : [
			{"Name" : "sub", "Type" : "None", "Direction" : "I"},
			{"Name" : "bound", "Type" : "None", "Direction" : "I"},
			{"Name" : "width_load", "Type" : "None", "Direction" : "I"},
			{"Name" : "window_stream", "Type" : "Fifo", "Direction" : "I",
				"BlockSignal" : [
					{"Name" : "window_stream_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "sub15", "Type" : "None", "Direction" : "I"},
			{"Name" : "output_stream4", "Type" : "Fifo", "Direction" : "O",
				"BlockSignal" : [
					{"Name" : "output_stream4_blk_n", "Type" : "RtlSignal"}]}],
		"Loop" : [
			{"Name" : "apply_filter_VITIS_LOOP_204_1", "PipelineType" : "UPC",
				"LoopDec" : {"FSMBitwidth" : "1", "FirstState" : "ap_ST_fsm_pp0_stage0", "FirstStateIter" : "ap_enable_reg_pp0_iter1", "FirstStateBlock" : "ap_block_pp0_stage0_subdone", "LastState" : "ap_ST_fsm_pp0_stage0", "LastStateIter" : "ap_enable_reg_pp0_iter7", "LastStateBlock" : "ap_block_pp0_stage0_subdone", "QuitState" : "ap_ST_fsm_pp0_stage0", "QuitStateIter" : "ap_enable_reg_pp0_iter7", "QuitStateBlock" : "ap_block_pp0_stage0_subdone", "OneDepthLoop" : "0", "has_ap_ctrl" : "1", "has_continue" : "0"}}]},
	{"ID" : "2", "Level" : "2", "Path" : "`AUTOTB_DUT_INST.grp_Filter2D_Pipeline_apply_filter_VITIS_LOOP_204_1_fu_72.mul_8ns_7ns_14_1_1_U31", "Parent" : "1"},
	{"ID" : "3", "Level" : "2", "Path" : "`AUTOTB_DUT_INST.grp_Filter2D_Pipeline_apply_filter_VITIS_LOOP_204_1_fu_72.ama_addmuladd_9ns_9ns_5ns_14ns_15_4_1_U32", "Parent" : "1"},
	{"ID" : "4", "Level" : "2", "Path" : "`AUTOTB_DUT_INST.grp_Filter2D_Pipeline_apply_filter_VITIS_LOOP_204_1_fu_72.flow_control_loop_pipe_sequential_init_U", "Parent" : "1"},
	{"ID" : "5", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.mul_mul_16ns_16ns_32_4_1_U41", "Parent" : "0"}]}


set ArgLastReadFirstWriteLatency {
	Filter2D {
		width {Type I LastRead 0 FirstWrite -1}
		height {Type I LastRead 0 FirstWrite -1}
		window_stream {Type I LastRead 2 FirstWrite -1}
		output_stream4 {Type O LastRead -1 FirstWrite 7}
		height_c {Type O LastRead -1 FirstWrite 0}
		width_c {Type O LastRead -1 FirstWrite 0}}
	Filter2D_Pipeline_apply_filter_VITIS_LOOP_204_1 {
		sub {Type I LastRead 0 FirstWrite -1}
		bound {Type I LastRead 0 FirstWrite -1}
		width_load {Type I LastRead 0 FirstWrite -1}
		window_stream {Type I LastRead 2 FirstWrite -1}
		sub15 {Type I LastRead 0 FirstWrite -1}
		output_stream4 {Type O LastRead -1 FirstWrite 7}}}

set hasDtUnsupportedChannel 0

set PerformanceInfo {[
	{"Name" : "Latency", "Min" : "7", "Max" : "4294836237"}
	, {"Name" : "Interval", "Min" : "7", "Max" : "-131059"}
]}

set PipelineEnableSignalInfo {[
]}

set Spec2ImplPortList { 
	width { ap_fifo {  { width_dout fifo_port_we 0 16 }  { width_num_data_valid fifo_status_num_data_valid 0 2 }  { width_fifo_cap fifo_update 0 2 }  { width_empty_n fifo_status 0 1 }  { width_read fifo_data 1 1 } } }
	height { ap_fifo {  { height_dout fifo_port_we 0 16 }  { height_num_data_valid fifo_status_num_data_valid 0 2 }  { height_fifo_cap fifo_update 0 2 }  { height_empty_n fifo_status 0 1 }  { height_read fifo_data 1 1 } } }
	window_stream { ap_fifo {  { window_stream_dout fifo_port_we 0 72 }  { window_stream_num_data_valid fifo_status_num_data_valid 0 2 }  { window_stream_fifo_cap fifo_update 0 2 }  { window_stream_empty_n fifo_status 0 1 }  { window_stream_read fifo_data 1 1 } } }
	output_stream4 { ap_fifo {  { output_stream4_din fifo_port_we 1 8 }  { output_stream4_num_data_valid fifo_status_num_data_valid 0 2 }  { output_stream4_fifo_cap fifo_update 0 2 }  { output_stream4_full_n fifo_status 0 1 }  { output_stream4_write fifo_data 1 1 } } }
	height_c { ap_fifo {  { height_c_din fifo_port_we 1 16 }  { height_c_num_data_valid fifo_status_num_data_valid 0 2 }  { height_c_fifo_cap fifo_update 0 2 }  { height_c_full_n fifo_status 0 1 }  { height_c_write fifo_data 1 1 } } }
	width_c { ap_fifo {  { width_c_din fifo_port_we 1 16 }  { width_c_num_data_valid fifo_status_num_data_valid 0 2 }  { width_c_fifo_cap fifo_update 0 2 }  { width_c_full_n fifo_status 0 1 }  { width_c_write fifo_data 1 1 } } }
}
