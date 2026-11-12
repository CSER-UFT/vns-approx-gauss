set moduleName Window2D_Pipeline_update_window
set isTopModule 0
set isCombinational 0
set isDatapathOnly 0
set isPipelined 1
set pipeline_type none
set FunctionProtocol ap_ctrl_hs
set isOneStateSeq 0
set ProfileFlag 0
set StallSigGenFlag 0
set isEnableWaveformDebug 1
set hasInterrupt 0
set C_modelName {Window2D_Pipeline_update_window}
set C_modelType { void 0 }
set C_modelArgList {
	{ num_iterations int 32 regular  }
	{ LineBuffer int 8 regular {array 512 { 2 3 } 1 1 }  }
	{ LineBuffer_1 int 8 regular {array 512 { 0 1 } 1 1 }  }
	{ sext_ln107 int 17 regular  }
	{ zext_ln101_2 int 17 regular  }
	{ num_pixels int 32 regular  }
	{ pixel_stream3 int 8 regular {fifo 0 volatile }  }
	{ window_stream int 72 regular {fifo 1 volatile }  }
}
set C_modelArgMapList {[ 
	{ "Name" : "num_iterations", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "LineBuffer", "interface" : "memory", "bitwidth" : 8, "direction" : "READWRITE"} , 
 	{ "Name" : "LineBuffer_1", "interface" : "memory", "bitwidth" : 8, "direction" : "READWRITE"} , 
 	{ "Name" : "sext_ln107", "interface" : "wire", "bitwidth" : 17, "direction" : "READONLY"} , 
 	{ "Name" : "zext_ln101_2", "interface" : "wire", "bitwidth" : 17, "direction" : "READONLY"} , 
 	{ "Name" : "num_pixels", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "pixel_stream3", "interface" : "fifo", "bitwidth" : 8, "direction" : "READONLY"} , 
 	{ "Name" : "window_stream", "interface" : "fifo", "bitwidth" : 72, "direction" : "WRITEONLY"} ]}
# RTL Port declarations: 
set portNum 32
set portList { 
	{ ap_clk sc_in sc_logic 1 clock -1 } 
	{ ap_rst sc_in sc_logic 1 reset -1 active_high_sync } 
	{ ap_start sc_in sc_logic 1 start -1 } 
	{ ap_done sc_out sc_logic 1 predone -1 } 
	{ ap_idle sc_out sc_logic 1 done -1 } 
	{ ap_ready sc_out sc_logic 1 ready -1 } 
	{ pixel_stream3_dout sc_in sc_lv 8 signal 6 } 
	{ pixel_stream3_num_data_valid sc_in sc_lv 2 signal 6 } 
	{ pixel_stream3_fifo_cap sc_in sc_lv 2 signal 6 } 
	{ pixel_stream3_empty_n sc_in sc_logic 1 signal 6 } 
	{ pixel_stream3_read sc_out sc_logic 1 signal 6 } 
	{ window_stream_din sc_out sc_lv 72 signal 7 } 
	{ window_stream_num_data_valid sc_in sc_lv 2 signal 7 } 
	{ window_stream_fifo_cap sc_in sc_lv 2 signal 7 } 
	{ window_stream_full_n sc_in sc_logic 1 signal 7 } 
	{ window_stream_write sc_out sc_logic 1 signal 7 } 
	{ num_iterations sc_in sc_lv 32 signal 0 } 
	{ LineBuffer_address0 sc_out sc_lv 9 signal 1 } 
	{ LineBuffer_ce0 sc_out sc_logic 1 signal 1 } 
	{ LineBuffer_we0 sc_out sc_logic 1 signal 1 } 
	{ LineBuffer_d0 sc_out sc_lv 8 signal 1 } 
	{ LineBuffer_q0 sc_in sc_lv 8 signal 1 } 
	{ LineBuffer_1_address0 sc_out sc_lv 9 signal 2 } 
	{ LineBuffer_1_ce0 sc_out sc_logic 1 signal 2 } 
	{ LineBuffer_1_we0 sc_out sc_logic 1 signal 2 } 
	{ LineBuffer_1_d0 sc_out sc_lv 8 signal 2 } 
	{ LineBuffer_1_address1 sc_out sc_lv 9 signal 2 } 
	{ LineBuffer_1_ce1 sc_out sc_logic 1 signal 2 } 
	{ LineBuffer_1_q1 sc_in sc_lv 8 signal 2 } 
	{ sext_ln107 sc_in sc_lv 17 signal 3 } 
	{ zext_ln101_2 sc_in sc_lv 17 signal 4 } 
	{ num_pixels sc_in sc_lv 32 signal 5 } 
}
set NewPortList {[ 
	{ "name": "ap_clk", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "clock", "bundle":{"name": "ap_clk", "role": "default" }} , 
 	{ "name": "ap_rst", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "reset", "bundle":{"name": "ap_rst", "role": "default" }} , 
 	{ "name": "ap_start", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "start", "bundle":{"name": "ap_start", "role": "default" }} , 
 	{ "name": "ap_done", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "predone", "bundle":{"name": "ap_done", "role": "default" }} , 
 	{ "name": "ap_idle", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "done", "bundle":{"name": "ap_idle", "role": "default" }} , 
 	{ "name": "ap_ready", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "ready", "bundle":{"name": "ap_ready", "role": "default" }} , 
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
 	{ "name": "num_iterations", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "num_iterations", "role": "default" }} , 
 	{ "name": "LineBuffer_address0", "direction": "out", "datatype": "sc_lv", "bitwidth":9, "type": "signal", "bundle":{"name": "LineBuffer", "role": "address0" }} , 
 	{ "name": "LineBuffer_ce0", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "LineBuffer", "role": "ce0" }} , 
 	{ "name": "LineBuffer_we0", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "LineBuffer", "role": "we0" }} , 
 	{ "name": "LineBuffer_d0", "direction": "out", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "LineBuffer", "role": "d0" }} , 
 	{ "name": "LineBuffer_q0", "direction": "in", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "LineBuffer", "role": "q0" }} , 
 	{ "name": "LineBuffer_1_address0", "direction": "out", "datatype": "sc_lv", "bitwidth":9, "type": "signal", "bundle":{"name": "LineBuffer_1", "role": "address0" }} , 
 	{ "name": "LineBuffer_1_ce0", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "LineBuffer_1", "role": "ce0" }} , 
 	{ "name": "LineBuffer_1_we0", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "LineBuffer_1", "role": "we0" }} , 
 	{ "name": "LineBuffer_1_d0", "direction": "out", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "LineBuffer_1", "role": "d0" }} , 
 	{ "name": "LineBuffer_1_address1", "direction": "out", "datatype": "sc_lv", "bitwidth":9, "type": "signal", "bundle":{"name": "LineBuffer_1", "role": "address1" }} , 
 	{ "name": "LineBuffer_1_ce1", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "LineBuffer_1", "role": "ce1" }} , 
 	{ "name": "LineBuffer_1_q1", "direction": "in", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "LineBuffer_1", "role": "q1" }} , 
 	{ "name": "sext_ln107", "direction": "in", "datatype": "sc_lv", "bitwidth":17, "type": "signal", "bundle":{"name": "sext_ln107", "role": "default" }} , 
 	{ "name": "zext_ln101_2", "direction": "in", "datatype": "sc_lv", "bitwidth":17, "type": "signal", "bundle":{"name": "zext_ln101_2", "role": "default" }} , 
 	{ "name": "num_pixels", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "num_pixels", "role": "default" }}  ]}

set RtlHierarchyInfo {[
	{"ID" : "0", "Level" : "0", "Path" : "`AUTOTB_DUT_INST", "Parent" : "", "Child" : ["1"],
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
	{"ID" : "1", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.flow_control_loop_pipe_sequential_init_U", "Parent" : "0"}]}


set ArgLastReadFirstWriteLatency {
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
	{"Name" : "Latency", "Min" : "4", "Max" : "262661"}
	, {"Name" : "Interval", "Min" : "4", "Max" : "262661"}
]}

set PipelineEnableSignalInfo {[
	{"Pipeline" : "0", "EnableSignal" : "ap_enable_pp0"}
]}

set Spec2ImplPortList { 
	num_iterations { ap_none {  { num_iterations in_data 0 32 } } }
	LineBuffer { ap_memory {  { LineBuffer_address0 mem_address 1 9 }  { LineBuffer_ce0 mem_ce 1 1 }  { LineBuffer_we0 mem_we 1 1 }  { LineBuffer_d0 mem_din 1 8 }  { LineBuffer_q0 in_data 0 8 } } }
	LineBuffer_1 { ap_memory {  { LineBuffer_1_address0 mem_address 1 9 }  { LineBuffer_1_ce0 mem_ce 1 1 }  { LineBuffer_1_we0 mem_we 1 1 }  { LineBuffer_1_d0 mem_din 1 8 }  { LineBuffer_1_address1 MemPortADDR2 1 9 }  { LineBuffer_1_ce1 MemPortCE2 1 1 }  { LineBuffer_1_q1 in_data 0 8 } } }
	sext_ln107 { ap_none {  { sext_ln107 in_data 0 17 } } }
	zext_ln101_2 { ap_none {  { zext_ln101_2 in_data 0 17 } } }
	num_pixels { ap_none {  { num_pixels in_data 0 32 } } }
	pixel_stream3 { ap_fifo {  { pixel_stream3_dout fifo_port_we 0 8 }  { pixel_stream3_num_data_valid fifo_status_num_data_valid 0 2 }  { pixel_stream3_fifo_cap fifo_update 0 2 }  { pixel_stream3_empty_n fifo_status 0 1 }  { pixel_stream3_read fifo_data 1 1 } } }
	window_stream { ap_fifo {  { window_stream_din fifo_port_we 1 72 }  { window_stream_num_data_valid fifo_status_num_data_valid 0 2 }  { window_stream_fifo_cap fifo_update 0 2 }  { window_stream_full_n fifo_status 0 1 }  { window_stream_write fifo_data 1 1 } } }
}
