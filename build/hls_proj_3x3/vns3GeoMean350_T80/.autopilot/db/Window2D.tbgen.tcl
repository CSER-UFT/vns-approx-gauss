set moduleName Window2D
set isTopModule 0
set isCombinational 0
set isDatapathOnly 0
set isPipelined 0
set pipeline_type none
set FunctionProtocol ap_ctrl_hs
set isOneStateSeq 0
set ProfileFlag 0
set StallSigGenFlag 0
set isEnableWaveformDebug 1
set hasInterrupt 0
set C_modelName {Window2D}
set C_modelType { void 0 }
set C_modelArgList {
	{ width int 16 regular {fifo 0}  }
	{ height int 16 regular {fifo 0}  }
	{ pixel_stream3 int 8 regular {fifo 0 volatile }  }
	{ window_stream int 72 regular {fifo 1 volatile }  }
	{ height_c11 int 16 regular {fifo 1}  }
	{ width_c13 int 16 regular {fifo 1}  }
}
set C_modelArgMapList {[ 
	{ "Name" : "width", "interface" : "fifo", "bitwidth" : 16, "direction" : "READONLY"} , 
 	{ "Name" : "height", "interface" : "fifo", "bitwidth" : 16, "direction" : "READONLY"} , 
 	{ "Name" : "pixel_stream3", "interface" : "fifo", "bitwidth" : 8, "direction" : "READONLY"} , 
 	{ "Name" : "window_stream", "interface" : "fifo", "bitwidth" : 72, "direction" : "WRITEONLY"} , 
 	{ "Name" : "height_c11", "interface" : "fifo", "bitwidth" : 16, "direction" : "WRITEONLY"} , 
 	{ "Name" : "width_c13", "interface" : "fifo", "bitwidth" : 16, "direction" : "WRITEONLY"} ]}
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
	{ pixel_stream3_dout sc_in sc_lv 8 signal 2 } 
	{ pixel_stream3_num_data_valid sc_in sc_lv 2 signal 2 } 
	{ pixel_stream3_fifo_cap sc_in sc_lv 2 signal 2 } 
	{ pixel_stream3_empty_n sc_in sc_logic 1 signal 2 } 
	{ pixel_stream3_read sc_out sc_logic 1 signal 2 } 
	{ window_stream_din sc_out sc_lv 72 signal 3 } 
	{ window_stream_num_data_valid sc_in sc_lv 2 signal 3 } 
	{ window_stream_fifo_cap sc_in sc_lv 2 signal 3 } 
	{ window_stream_full_n sc_in sc_logic 1 signal 3 } 
	{ window_stream_write sc_out sc_logic 1 signal 3 } 
	{ height_c11_din sc_out sc_lv 16 signal 4 } 
	{ height_c11_num_data_valid sc_in sc_lv 2 signal 4 } 
	{ height_c11_fifo_cap sc_in sc_lv 2 signal 4 } 
	{ height_c11_full_n sc_in sc_logic 1 signal 4 } 
	{ height_c11_write sc_out sc_logic 1 signal 4 } 
	{ width_c13_din sc_out sc_lv 16 signal 5 } 
	{ width_c13_num_data_valid sc_in sc_lv 2 signal 5 } 
	{ width_c13_fifo_cap sc_in sc_lv 2 signal 5 } 
	{ width_c13_full_n sc_in sc_logic 1 signal 5 } 
	{ width_c13_write sc_out sc_logic 1 signal 5 } 
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
 	{ "name": "pixel_stream3_dout", "direction": "in", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "pixel_stream3", "role": "dout" }} , 
 	{ "name": "pixel_stream3_num_data_valid", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "pixel_stream3", "role": "num_data_valid" }} , 
 	{ "name": "pixel_stream3_fifo_cap", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "pixel_stream3", "role": "fifo_cap" }} , 
 	{ "name": "pixel_stream3_empty_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "pixel_stream3", "role": "empty_n" }} , 
 	{ "name": "pixel_stream3_read", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "pixel_stream3", "role": "read" }} , 
 	{ "name": "window_stream_din", "direction": "out", "datatype": "sc_lv", "bitwidth":72, "type": "signal", "bundle":{"name": "window_stream", "role": "din" }} , 
 	{ "name": "window_stream_num_data_valid", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "window_stream", "role": "num_data_valid" }} , 
 	{ "name": "window_stream_fifo_cap", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "window_stream", "role": "fifo_cap" }} , 
 	{ "name": "window_stream_full_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "window_stream", "role": "full_n" }} , 
 	{ "name": "window_stream_write", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "window_stream", "role": "write" }} , 
 	{ "name": "height_c11_din", "direction": "out", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "height_c11", "role": "din" }} , 
 	{ "name": "height_c11_num_data_valid", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "height_c11", "role": "num_data_valid" }} , 
 	{ "name": "height_c11_fifo_cap", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "height_c11", "role": "fifo_cap" }} , 
 	{ "name": "height_c11_full_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "height_c11", "role": "full_n" }} , 
 	{ "name": "height_c11_write", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "height_c11", "role": "write" }} , 
 	{ "name": "width_c13_din", "direction": "out", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "width_c13", "role": "din" }} , 
 	{ "name": "width_c13_num_data_valid", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "width_c13", "role": "num_data_valid" }} , 
 	{ "name": "width_c13_fifo_cap", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "width_c13", "role": "fifo_cap" }} , 
 	{ "name": "width_c13_full_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "width_c13", "role": "full_n" }} , 
 	{ "name": "width_c13_write", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "width_c13", "role": "write" }}  ]}

set RtlHierarchyInfo {[
	{"ID" : "0", "Level" : "0", "Path" : "`AUTOTB_DUT_INST", "Parent" : "", "Child" : ["1", "2", "3", "5"],
		"CDFG" : "Window2D",
		"Protocol" : "ap_ctrl_hs",
		"ControlExist" : "1", "ap_start" : "1", "ap_ready" : "1", "ap_done" : "1", "ap_continue" : "1", "ap_idle" : "1", "real_start" : "1",
		"Pipeline" : "None", "UnalignedPipeline" : "0", "RewindPipeline" : "0", "ProcessNetwork" : "0",
		"II" : "0",
		"VariableLatency" : "1", "ExactLatency" : "-1", "EstimateLatencyMin" : "8", "EstimateLatencyMax" : "262665",
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
			{"Name" : "pixel_stream3", "Type" : "Fifo", "Direction" : "I", "DependentProc" : ["0"], "DependentChan" : "0", "DependentChanDepth" : "2", "DependentChanType" : "0",
				"SubConnect" : [
					{"ID" : "3", "SubInstance" : "grp_Window2D_Pipeline_update_window_fu_82", "Port" : "pixel_stream3", "Inst_start_state" : "4", "Inst_end_state" : "5"}]},
			{"Name" : "window_stream", "Type" : "Fifo", "Direction" : "O", "DependentProc" : ["0"], "DependentChan" : "0", "DependentChanDepth" : "2", "DependentChanType" : "0",
				"SubConnect" : [
					{"ID" : "3", "SubInstance" : "grp_Window2D_Pipeline_update_window_fu_82", "Port" : "window_stream", "Inst_start_state" : "4", "Inst_end_state" : "5"}]},
			{"Name" : "height_c11", "Type" : "Fifo", "Direction" : "O", "DependentProc" : ["0"], "DependentChan" : "0", "DependentChanDepth" : "2", "DependentChanType" : "2",
				"BlockSignal" : [
					{"Name" : "height_c11_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "width_c13", "Type" : "Fifo", "Direction" : "O", "DependentProc" : ["0"], "DependentChan" : "0", "DependentChanDepth" : "2", "DependentChanType" : "2",
				"BlockSignal" : [
					{"Name" : "width_c13_blk_n", "Type" : "RtlSignal"}]}]},
	{"ID" : "1", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.LineBuffer_U", "Parent" : "0"},
	{"ID" : "2", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.LineBuffer_1_U", "Parent" : "0"},
	{"ID" : "3", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.grp_Window2D_Pipeline_update_window_fu_82", "Parent" : "0", "Child" : ["4"],
		"CDFG" : "Window2D_Pipeline_update_window",
		"Protocol" : "ap_ctrl_hs",
		"ControlExist" : "1", "ap_start" : "1", "ap_ready" : "1", "ap_done" : "1", "ap_continue" : "0", "ap_idle" : "1", "real_start" : "0",
		"Pipeline" : "None", "UnalignedPipeline" : "0", "RewindPipeline" : "0", "ProcessNetwork" : "0",
		"II" : "0",
		"VariableLatency" : "1", "ExactLatency" : "-1", "EstimateLatencyMin" : "4", "EstimateLatencyMax" : "262661",
		"Combinational" : "0",
		"Datapath" : "0",
		"ClockEnable" : "0",
		"HasSubDataflow" : "0",
		"InDataflowNetwork" : "0",
		"HasNonBlockingOperation" : "0",
		"IsBlackBox" : "0",
		"DependenceCheck" : [
			{"FromInitialState" : "ap_enable_state2_pp0_iter1_stage0", "FromInitialIteration" : "ap_enable_reg_pp0_iter1", "FromInitialOperation" : "ap_enable_operation_38", "FromInitialSV" : "1", "FromFinalState" : "ap_enable_state3_pp0_iter2_stage0", "FromFinalIteration" : "ap_enable_reg_pp0_iter2", "FromFinalOperation" : "ap_enable_operation_49", "FromFinalSV" : "2", "FromAddress" : "LineBuffer_1_address1", "FromType" : "R", "ToInitialState" : "ap_enable_state4_pp0_iter3_stage0", "ToInitialIteration" : "ap_enable_reg_pp0_iter3", "ToInitialNextIteration" : "null", "ToInitialOperation" : "ap_enable_operation_56", "ToInitialSV" : "3", "ToFinalState" : "ap_enable_state4_pp0_iter3_stage0", "ToFinalIteration" : "ap_enable_reg_pp0_iter3", "ToFinalOperation" : "ap_enable_operation_56", "ToFinalSV" : "3", "ToAddress" : "LineBuffer_1_address0", "ToType" : "W", "PipelineBlock" : "ap_block_pp0", "AddressWidth" : "9", "II" : "1", "Pragma" : "(../gaussian_vns_3x3.cpp:95:9)", "Type" : "WAR"},
			{"FromInitialState" : "ap_enable_state3_pp0_iter2_stage0", "FromInitialIteration" : "ap_enable_reg_pp0_iter2", "FromInitialOperation" : "ap_enable_operation_50", "FromInitialSV" : "2", "FromFinalState" : "ap_enable_state3_pp0_iter2_stage0", "FromFinalIteration" : "ap_enable_reg_pp0_iter2", "FromFinalOperation" : "ap_enable_operation_50", "FromFinalSV" : "2", "FromAddress" : "LineBuffer_address0", "FromType" : "W", "ToInitialState" : "ap_enable_state3_pp0_iter2_stage0", "ToInitialIteration" : "ap_enable_reg_pp0_iter2", "ToInitialNextIteration" : "ap_enable_reg_pp0_iter3", "ToInitialOperation" : "ap_enable_operation_48", "ToInitialSV" : "2", "ToFinalState" : "ap_enable_state4_pp0_iter3_stage0", "ToFinalIteration" : "ap_enable_reg_pp0_iter3", "ToFinalOperation" : "ap_enable_operation_55", "ToFinalSV" : "3", "ToAddress" : "LineBuffer_address0", "ToType" : "R", "PipelineBlock" : "ap_block_pp0", "AddressWidth" : "9", "II" : "1", "Pragma" : "(../gaussian_vns_3x3.cpp:95:9)", "Type" : "RAW"},
			{"FromInitialState" : "ap_enable_state3_pp0_iter2_stage0", "FromInitialIteration" : "ap_enable_reg_pp0_iter2", "FromInitialOperation" : "ap_enable_operation_48", "FromInitialSV" : "2", "FromFinalState" : "ap_enable_state4_pp0_iter3_stage0", "FromFinalIteration" : "ap_enable_reg_pp0_iter3", "FromFinalOperation" : "ap_enable_operation_55", "FromFinalSV" : "3", "FromAddress" : "LineBuffer_address0", "FromType" : "R", "ToInitialState" : "ap_enable_state3_pp0_iter2_stage0", "ToInitialIteration" : "ap_enable_reg_pp0_iter2", "ToInitialNextIteration" : "ap_enable_reg_pp0_iter3", "ToInitialOperation" : "ap_enable_operation_50", "ToInitialSV" : "2", "ToFinalState" : "ap_enable_state3_pp0_iter2_stage0", "ToFinalIteration" : "ap_enable_reg_pp0_iter2", "ToFinalOperation" : "ap_enable_operation_50", "ToFinalSV" : "2", "ToAddress" : "LineBuffer_address0", "ToType" : "W", "PipelineBlock" : "ap_block_pp0", "AddressWidth" : "9", "II" : "1", "Pragma" : "(../gaussian_vns_3x3.cpp:95:9)", "Type" : "WAR", "StateEnableSignalListForFifoShift" : ["ap_enable_state3_pp0_iter2_stage0", "ap_enable_state4_pp0_iter3_stage0"]},
			{"FromInitialState" : "ap_enable_state4_pp0_iter3_stage0", "FromInitialIteration" : "ap_enable_reg_pp0_iter3", "FromInitialOperation" : "ap_enable_operation_56", "FromInitialSV" : "3", "FromFinalState" : "ap_enable_state4_pp0_iter3_stage0", "FromFinalIteration" : "ap_enable_reg_pp0_iter3", "FromFinalOperation" : "ap_enable_operation_56", "FromFinalSV" : "3", "FromAddress" : "LineBuffer_1_address0", "FromType" : "W", "ToInitialState" : "ap_enable_state2_pp0_iter1_stage0", "ToInitialIteration" : "ap_enable_reg_pp0_iter1", "ToInitialNextIteration" : "ap_enable_reg_pp0_iter2", "ToInitialOperation" : "ap_enable_operation_38", "ToInitialSV" : "1", "ToFinalState" : "ap_enable_state3_pp0_iter2_stage0", "ToFinalIteration" : "ap_enable_reg_pp0_iter2", "ToFinalOperation" : "ap_enable_operation_49", "ToFinalSV" : "2", "ToAddress" : "LineBuffer_1_address1", "ToType" : "R", "PipelineBlock" : "ap_block_pp0", "AddressWidth" : "9", "II" : "1", "Pragma" : "(../gaussian_vns_3x3.cpp:95:9)", "Type" : "RAW", "StateEnableSignalListForFifoShift" : ["ap_enable_state2_pp0_iter1_stage0", "ap_enable_state3_pp0_iter2_stage0", "ap_enable_state4_pp0_iter3_stage0"]}],
		"Port" : [
			{"Name" : "num_iterations", "Type" : "None", "Direction" : "I"},
			{"Name" : "LineBuffer", "Type" : "Memory", "Direction" : "IO"},
			{"Name" : "LineBuffer_1", "Type" : "Memory", "Direction" : "IO"},
			{"Name" : "sext_ln107", "Type" : "None", "Direction" : "I"},
			{"Name" : "zext_ln101_2", "Type" : "None", "Direction" : "I"},
			{"Name" : "num_pixels", "Type" : "None", "Direction" : "I"},
			{"Name" : "pixel_stream3", "Type" : "Fifo", "Direction" : "I",
				"BlockSignal" : [
					{"Name" : "pixel_stream3_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "window_stream", "Type" : "Fifo", "Direction" : "O",
				"BlockSignal" : [
					{"Name" : "window_stream_blk_n", "Type" : "RtlSignal"}]}],
		"Loop" : [
			{"Name" : "update_window", "PipelineType" : "UPC",
				"LoopDec" : {"FSMBitwidth" : "1", "FirstState" : "ap_ST_fsm_pp0_stage0", "FirstStateIter" : "ap_enable_reg_pp0_iter1", "FirstStateBlock" : "ap_block_pp0_stage0_subdone", "LastState" : "ap_ST_fsm_pp0_stage0", "LastStateIter" : "ap_enable_reg_pp0_iter3", "LastStateBlock" : "ap_block_pp0_stage0_subdone", "QuitState" : "ap_ST_fsm_pp0_stage0", "QuitStateIter" : "ap_enable_reg_pp0_iter3", "QuitStateBlock" : "ap_block_pp0_stage0_subdone", "OneDepthLoop" : "0", "has_ap_ctrl" : "1", "has_continue" : "0"}}]},
	{"ID" : "4", "Level" : "2", "Path" : "`AUTOTB_DUT_INST.grp_Window2D_Pipeline_update_window_fu_82.flow_control_loop_pipe_sequential_init_U", "Parent" : "3"},
	{"ID" : "5", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.mul_mul_16ns_16ns_32_4_1_U22", "Parent" : "0"}]}


set ArgLastReadFirstWriteLatency {
	Window2D {
		width {Type I LastRead 0 FirstWrite -1}
		height {Type I LastRead 0 FirstWrite -1}
		pixel_stream3 {Type I LastRead 2 FirstWrite -1}
		window_stream {Type O LastRead -1 FirstWrite 3}
		height_c11 {Type O LastRead -1 FirstWrite 0}
		width_c13 {Type O LastRead -1 FirstWrite 0}}
	Window2D_Pipeline_update_window {
		num_iterations {Type I LastRead 0 FirstWrite -1}
		LineBuffer {Type IO LastRead 2 FirstWrite 2}
		LineBuffer_1 {Type IO LastRead 1 FirstWrite 3}
		sext_ln107 {Type I LastRead 0 FirstWrite -1}
		zext_ln101_2 {Type I LastRead 0 FirstWrite -1}
		num_pixels {Type I LastRead 0 FirstWrite -1}
		pixel_stream3 {Type I LastRead 2 FirstWrite -1}
		window_stream {Type O LastRead -1 FirstWrite 3}}}

set hasDtUnsupportedChannel 0

set PerformanceInfo {[
	{"Name" : "Latency", "Min" : "8", "Max" : "262665"}
	, {"Name" : "Interval", "Min" : "8", "Max" : "262665"}
]}

set PipelineEnableSignalInfo {[
]}

set Spec2ImplPortList { 
	width { ap_fifo {  { width_dout fifo_port_we 0 16 }  { width_num_data_valid fifo_status_num_data_valid 0 2 }  { width_fifo_cap fifo_update 0 2 }  { width_empty_n fifo_status 0 1 }  { width_read fifo_data 1 1 } } }
	height { ap_fifo {  { height_dout fifo_port_we 0 16 }  { height_num_data_valid fifo_status_num_data_valid 0 2 }  { height_fifo_cap fifo_update 0 2 }  { height_empty_n fifo_status 0 1 }  { height_read fifo_data 1 1 } } }
	pixel_stream3 { ap_fifo {  { pixel_stream3_dout fifo_port_we 0 8 }  { pixel_stream3_num_data_valid fifo_status_num_data_valid 0 2 }  { pixel_stream3_fifo_cap fifo_update 0 2 }  { pixel_stream3_empty_n fifo_status 0 1 }  { pixel_stream3_read fifo_data 1 1 } } }
	window_stream { ap_fifo {  { window_stream_din fifo_port_we 1 72 }  { window_stream_num_data_valid fifo_status_num_data_valid 0 2 }  { window_stream_fifo_cap fifo_update 0 2 }  { window_stream_full_n fifo_status 0 1 }  { window_stream_write fifo_data 1 1 } } }
	height_c11 { ap_fifo {  { height_c11_din fifo_port_we 1 16 }  { height_c11_num_data_valid fifo_status_num_data_valid 0 2 }  { height_c11_fifo_cap fifo_update 0 2 }  { height_c11_full_n fifo_status 0 1 }  { height_c11_write fifo_data 1 1 } } }
	width_c13 { ap_fifo {  { width_c13_din fifo_port_we 1 16 }  { width_c13_num_data_valid fifo_status_num_data_valid 0 2 }  { width_c13_fifo_cap fifo_update 0 2 }  { width_c13_full_n fifo_status 0 1 }  { width_c13_write fifo_data 1 1 } } }
}
