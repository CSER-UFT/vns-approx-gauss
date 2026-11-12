set moduleName WriteToMem_Pipeline_write_image
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
set C_modelName {WriteToMem_Pipeline_write_image}
set C_modelType { void 0 }
set C_modelArgList {
	{ mul_ln73 int 19 regular  }
	{ dst int 8 regular {array 262144 { 0 3 } 0 1 }  }
	{ sext_ln73 int 11 regular  }
	{ conv11 int 10 regular  }
	{ output_stream4 int 8 regular {fifo 0 volatile }  }
}
set C_modelArgMapList {[ 
	{ "Name" : "mul_ln73", "interface" : "wire", "bitwidth" : 19, "direction" : "READONLY"} , 
 	{ "Name" : "dst", "interface" : "memory", "bitwidth" : 8, "direction" : "WRITEONLY"} , 
 	{ "Name" : "sext_ln73", "interface" : "wire", "bitwidth" : 11, "direction" : "READONLY"} , 
 	{ "Name" : "conv11", "interface" : "wire", "bitwidth" : 10, "direction" : "READONLY"} , 
 	{ "Name" : "output_stream4", "interface" : "fifo", "bitwidth" : 8, "direction" : "READONLY"} ]}
# RTL Port declarations: 
set portNum 18
set portList { 
	{ ap_clk sc_in sc_logic 1 clock -1 } 
	{ ap_rst sc_in sc_logic 1 reset -1 active_high_sync } 
	{ ap_start sc_in sc_logic 1 start -1 } 
	{ ap_done sc_out sc_logic 1 predone -1 } 
	{ ap_idle sc_out sc_logic 1 done -1 } 
	{ ap_ready sc_out sc_logic 1 ready -1 } 
	{ output_stream4_dout sc_in sc_lv 8 signal 4 } 
	{ output_stream4_num_data_valid sc_in sc_lv 2 signal 4 } 
	{ output_stream4_fifo_cap sc_in sc_lv 2 signal 4 } 
	{ output_stream4_empty_n sc_in sc_logic 1 signal 4 } 
	{ output_stream4_read sc_out sc_logic 1 signal 4 } 
	{ mul_ln73 sc_in sc_lv 19 signal 0 } 
	{ dst_address0 sc_out sc_lv 18 signal 1 } 
	{ dst_ce0 sc_out sc_logic 1 signal 1 } 
	{ dst_we0 sc_out sc_logic 1 signal 1 } 
	{ dst_d0 sc_out sc_lv 8 signal 1 } 
	{ sext_ln73 sc_in sc_lv 11 signal 2 } 
	{ conv11 sc_in sc_lv 10 signal 3 } 
}
set NewPortList {[ 
	{ "name": "ap_clk", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "clock", "bundle":{"name": "ap_clk", "role": "default" }} , 
 	{ "name": "ap_rst", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "reset", "bundle":{"name": "ap_rst", "role": "default" }} , 
 	{ "name": "ap_start", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "start", "bundle":{"name": "ap_start", "role": "default" }} , 
 	{ "name": "ap_done", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "predone", "bundle":{"name": "ap_done", "role": "default" }} , 
 	{ "name": "ap_idle", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "done", "bundle":{"name": "ap_idle", "role": "default" }} , 
 	{ "name": "ap_ready", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "ready", "bundle":{"name": "ap_ready", "role": "default" }} , 
 	{ "name": "output_stream4_dout", "direction": "in", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "output_stream4", "role": "dout" }} , 
 	{ "name": "output_stream4_num_data_valid", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "output_stream4", "role": "num_data_valid" }} , 
 	{ "name": "output_stream4_fifo_cap", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "output_stream4", "role": "fifo_cap" }} , 
 	{ "name": "output_stream4_empty_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "output_stream4", "role": "empty_n" }} , 
 	{ "name": "output_stream4_read", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "output_stream4", "role": "read" }} , 
 	{ "name": "mul_ln73", "direction": "in", "datatype": "sc_lv", "bitwidth":19, "type": "signal", "bundle":{"name": "mul_ln73", "role": "default" }} , 
 	{ "name": "dst_address0", "direction": "out", "datatype": "sc_lv", "bitwidth":18, "type": "signal", "bundle":{"name": "dst", "role": "address0" }} , 
 	{ "name": "dst_ce0", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "dst", "role": "ce0" }} , 
 	{ "name": "dst_we0", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "dst", "role": "we0" }} , 
 	{ "name": "dst_d0", "direction": "out", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "dst", "role": "d0" }} , 
 	{ "name": "sext_ln73", "direction": "in", "datatype": "sc_lv", "bitwidth":11, "type": "signal", "bundle":{"name": "sext_ln73", "role": "default" }} , 
 	{ "name": "conv11", "direction": "in", "datatype": "sc_lv", "bitwidth":10, "type": "signal", "bundle":{"name": "conv11", "role": "default" }}  ]}

set RtlHierarchyInfo {[
	{"ID" : "0", "Level" : "0", "Path" : "`AUTOTB_DUT_INST", "Parent" : "", "Child" : ["1"],
		"CDFG" : "WriteToMem_Pipeline_write_image",
		"Protocol" : "ap_ctrl_hs",
		"ControlExist" : "1", "ap_start" : "1", "ap_ready" : "1", "ap_done" : "1", "ap_continue" : "0", "ap_idle" : "1", "real_start" : "0",
		"Pipeline" : "None", "UnalignedPipeline" : "0", "RewindPipeline" : "0", "ProcessNetwork" : "0",
		"II" : "0",
		"VariableLatency" : "1", "ExactLatency" : "-1", "EstimateLatencyMin" : "2", "EstimateLatencyMax" : "523779",
		"Combinational" : "0",
		"Datapath" : "0",
		"ClockEnable" : "0",
		"HasSubDataflow" : "0",
		"InDataflowNetwork" : "0",
		"HasNonBlockingOperation" : "0",
		"IsBlackBox" : "0",
		"Port" : [
			{"Name" : "mul_ln73", "Type" : "None", "Direction" : "I"},
			{"Name" : "dst", "Type" : "Memory", "Direction" : "O"},
			{"Name" : "sext_ln73", "Type" : "None", "Direction" : "I"},
			{"Name" : "conv11", "Type" : "None", "Direction" : "I"},
			{"Name" : "output_stream4", "Type" : "Fifo", "Direction" : "I",
				"BlockSignal" : [
					{"Name" : "output_stream4_blk_n", "Type" : "RtlSignal"}]}],
		"Loop" : [
			{"Name" : "write_image", "PipelineType" : "UPC",
				"LoopDec" : {"FSMBitwidth" : "1", "FirstState" : "ap_ST_fsm_pp0_stage0", "FirstStateIter" : "ap_enable_reg_pp0_iter1", "FirstStateBlock" : "ap_block_pp0_stage0_subdone", "LastState" : "ap_ST_fsm_pp0_stage0", "LastStateIter" : "ap_enable_reg_pp0_iter3", "LastStateBlock" : "ap_block_pp0_stage0_subdone", "QuitState" : "ap_ST_fsm_pp0_stage0", "QuitStateIter" : "ap_enable_reg_pp0_iter3", "QuitStateBlock" : "ap_block_pp0_stage0_subdone", "OneDepthLoop" : "0", "has_ap_ctrl" : "1", "has_continue" : "0"}}]},
	{"ID" : "1", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.flow_control_loop_pipe_sequential_init_U", "Parent" : "0"}]}


set ArgLastReadFirstWriteLatency {
	WriteToMem_Pipeline_write_image {
		mul_ln73 {Type I LastRead 0 FirstWrite -1}
		dst {Type O LastRead -1 FirstWrite 3}
		sext_ln73 {Type I LastRead 0 FirstWrite -1}
		conv11 {Type I LastRead 0 FirstWrite -1}
		output_stream4 {Type I LastRead 2 FirstWrite -1}}}

set hasDtUnsupportedChannel 0

set PerformanceInfo {[
	{"Name" : "Latency", "Min" : "2", "Max" : "523779"}
	, {"Name" : "Interval", "Min" : "2", "Max" : "523779"}
]}

set PipelineEnableSignalInfo {[
	{"Pipeline" : "0", "EnableSignal" : "ap_enable_pp0"}
]}

set Spec2ImplPortList { 
	mul_ln73 { ap_none {  { mul_ln73 in_data 0 19 } } }
	dst { ap_memory {  { dst_address0 mem_address 1 18 }  { dst_ce0 mem_ce 1 1 }  { dst_we0 mem_we 1 1 }  { dst_d0 mem_din 1 8 } } }
	sext_ln73 { ap_none {  { sext_ln73 in_data 0 11 } } }
	conv11 { ap_none {  { conv11 in_data 0 10 } } }
	output_stream4 { ap_fifo {  { output_stream4_dout fifo_port_we 0 8 }  { output_stream4_num_data_valid fifo_status_num_data_valid 0 2 }  { output_stream4_fifo_cap fifo_update 0 2 }  { output_stream4_empty_n fifo_status 0 1 }  { output_stream4_read fifo_data 1 1 } } }
}
