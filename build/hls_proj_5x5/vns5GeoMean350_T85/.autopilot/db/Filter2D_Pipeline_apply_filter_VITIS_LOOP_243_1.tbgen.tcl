set moduleName Filter2D_Pipeline_apply_filter_VITIS_LOOP_243_1
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
set C_modelName {Filter2D_Pipeline_apply_filter_VITIS_LOOP_243_1}
set C_modelType { void 0 }
set C_modelArgList {
	{ sub int 17 regular  }
	{ bound int 32 regular  }
	{ width_load int 16 regular  }
	{ window_stream int 200 regular {fifo 0 volatile }  }
	{ sub15 int 17 regular  }
	{ output_stream4 int 8 regular {fifo 1 volatile }  }
}
set C_modelArgMapList {[ 
	{ "Name" : "sub", "interface" : "wire", "bitwidth" : 17, "direction" : "READONLY"} , 
 	{ "Name" : "bound", "interface" : "wire", "bitwidth" : 32, "direction" : "READONLY"} , 
 	{ "Name" : "width_load", "interface" : "wire", "bitwidth" : 16, "direction" : "READONLY"} , 
 	{ "Name" : "window_stream", "interface" : "fifo", "bitwidth" : 200, "direction" : "READONLY"} , 
 	{ "Name" : "sub15", "interface" : "wire", "bitwidth" : 17, "direction" : "READONLY"} , 
 	{ "Name" : "output_stream4", "interface" : "fifo", "bitwidth" : 8, "direction" : "WRITEONLY"} ]}
# RTL Port declarations: 
set portNum 20
set portList { 
	{ ap_clk sc_in sc_logic 1 clock -1 } 
	{ ap_rst sc_in sc_logic 1 reset -1 active_high_sync } 
	{ ap_start sc_in sc_logic 1 start -1 } 
	{ ap_done sc_out sc_logic 1 predone -1 } 
	{ ap_idle sc_out sc_logic 1 done -1 } 
	{ ap_ready sc_out sc_logic 1 ready -1 } 
	{ window_stream_dout sc_in sc_lv 200 signal 3 } 
	{ window_stream_num_data_valid sc_in sc_lv 2 signal 3 } 
	{ window_stream_fifo_cap sc_in sc_lv 2 signal 3 } 
	{ window_stream_empty_n sc_in sc_logic 1 signal 3 } 
	{ window_stream_read sc_out sc_logic 1 signal 3 } 
	{ output_stream4_din sc_out sc_lv 8 signal 5 } 
	{ output_stream4_num_data_valid sc_in sc_lv 2 signal 5 } 
	{ output_stream4_fifo_cap sc_in sc_lv 2 signal 5 } 
	{ output_stream4_full_n sc_in sc_logic 1 signal 5 } 
	{ output_stream4_write sc_out sc_logic 1 signal 5 } 
	{ sub sc_in sc_lv 17 signal 0 } 
	{ bound sc_in sc_lv 32 signal 1 } 
	{ width_load sc_in sc_lv 16 signal 2 } 
	{ sub15 sc_in sc_lv 17 signal 4 } 
}
set NewPortList {[ 
	{ "name": "ap_clk", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "clock", "bundle":{"name": "ap_clk", "role": "default" }} , 
 	{ "name": "ap_rst", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "reset", "bundle":{"name": "ap_rst", "role": "default" }} , 
 	{ "name": "ap_start", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "start", "bundle":{"name": "ap_start", "role": "default" }} , 
 	{ "name": "ap_done", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "predone", "bundle":{"name": "ap_done", "role": "default" }} , 
 	{ "name": "ap_idle", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "done", "bundle":{"name": "ap_idle", "role": "default" }} , 
 	{ "name": "ap_ready", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "ready", "bundle":{"name": "ap_ready", "role": "default" }} , 
 	{ "name": "window_stream_dout", "direction": "in", "datatype": "sc_lv", "bitwidth":200, "type": "signal", "bundle":{"name": "window_stream", "role": "dout" }} , 
 	{ "name": "window_stream_num_data_valid", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "window_stream", "role": "num_data_valid" }} , 
 	{ "name": "window_stream_fifo_cap", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "window_stream", "role": "fifo_cap" }} , 
 	{ "name": "window_stream_empty_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "window_stream", "role": "empty_n" }} , 
 	{ "name": "window_stream_read", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "window_stream", "role": "read" }} , 
 	{ "name": "output_stream4_din", "direction": "out", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "output_stream4", "role": "din" }} , 
 	{ "name": "output_stream4_num_data_valid", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "output_stream4", "role": "num_data_valid" }} , 
 	{ "name": "output_stream4_fifo_cap", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "output_stream4", "role": "fifo_cap" }} , 
 	{ "name": "output_stream4_full_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "output_stream4", "role": "full_n" }} , 
 	{ "name": "output_stream4_write", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "output_stream4", "role": "write" }} , 
 	{ "name": "sub", "direction": "in", "datatype": "sc_lv", "bitwidth":17, "type": "signal", "bundle":{"name": "sub", "role": "default" }} , 
 	{ "name": "bound", "direction": "in", "datatype": "sc_lv", "bitwidth":32, "type": "signal", "bundle":{"name": "bound", "role": "default" }} , 
 	{ "name": "width_load", "direction": "in", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "width_load", "role": "default" }} , 
 	{ "name": "sub15", "direction": "in", "datatype": "sc_lv", "bitwidth":17, "type": "signal", "bundle":{"name": "sub15", "role": "default" }}  ]}

set RtlHierarchyInfo {[
	{"ID" : "0", "Level" : "0", "Path" : "`AUTOTB_DUT_INST", "Parent" : "", "Child" : ["1"],
		"CDFG" : "Filter2D_Pipeline_apply_filter_VITIS_LOOP_243_1",
		"Protocol" : "ap_ctrl_hs",
		"ControlExist" : "1", "ap_start" : "1", "ap_ready" : "1", "ap_done" : "1", "ap_continue" : "0", "ap_idle" : "1", "real_start" : "0",
		"Pipeline" : "None", "UnalignedPipeline" : "0", "RewindPipeline" : "0", "ProcessNetwork" : "0",
		"II" : "0",
		"VariableLatency" : "1", "ExactLatency" : "-1", "EstimateLatencyMin" : "2", "EstimateLatencyMax" : "4294836231",
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
			{"Name" : "apply_filter_VITIS_LOOP_243_1", "PipelineType" : "UPC",
				"LoopDec" : {"FSMBitwidth" : "1", "FirstState" : "ap_ST_fsm_pp0_stage0", "FirstStateIter" : "ap_enable_reg_pp0_iter1", "FirstStateBlock" : "ap_block_pp0_stage0_subdone", "LastState" : "ap_ST_fsm_pp0_stage0", "LastStateIter" : "ap_enable_reg_pp0_iter6", "LastStateBlock" : "ap_block_pp0_stage0_subdone", "QuitState" : "ap_ST_fsm_pp0_stage0", "QuitStateIter" : "ap_enable_reg_pp0_iter6", "QuitStateBlock" : "ap_block_pp0_stage0_subdone", "OneDepthLoop" : "0", "has_ap_ctrl" : "1", "has_continue" : "0"}}]},
	{"ID" : "1", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.flow_control_loop_pipe_sequential_init_U", "Parent" : "0"}]}


set ArgLastReadFirstWriteLatency {
	Filter2D_Pipeline_apply_filter_VITIS_LOOP_243_1 {
		sub {Type I LastRead 0 FirstWrite -1}
		bound {Type I LastRead 0 FirstWrite -1}
		width_load {Type I LastRead 0 FirstWrite -1}
		window_stream {Type I LastRead 2 FirstWrite -1}
		sub15 {Type I LastRead 0 FirstWrite -1}
		output_stream4 {Type O LastRead -1 FirstWrite 6}}}

set hasDtUnsupportedChannel 0

set PerformanceInfo {[
	{"Name" : "Latency", "Min" : "2", "Max" : "4294836231"}
	, {"Name" : "Interval", "Min" : "2", "Max" : "-131065"}
]}

set PipelineEnableSignalInfo {[
	{"Pipeline" : "0", "EnableSignal" : "ap_enable_pp0"}
]}

set Spec2ImplPortList { 
	sub { ap_none {  { sub in_data 0 17 } } }
	bound { ap_none {  { bound in_data 0 32 } } }
	width_load { ap_none {  { width_load in_data 0 16 } } }
	window_stream { ap_fifo {  { window_stream_dout fifo_port_we 0 200 }  { window_stream_num_data_valid fifo_status_num_data_valid 0 2 }  { window_stream_fifo_cap fifo_update 0 2 }  { window_stream_empty_n fifo_status 0 1 }  { window_stream_read fifo_data 1 1 } } }
	sub15 { ap_none {  { sub15 in_data 0 17 } } }
	output_stream4 { ap_fifo {  { output_stream4_din fifo_port_we 1 8 }  { output_stream4_num_data_valid fifo_status_num_data_valid 0 2 }  { output_stream4_fifo_cap fifo_update 0 2 }  { output_stream4_full_n fifo_status 0 1 }  { output_stream4_write fifo_data 1 1 } } }
}
