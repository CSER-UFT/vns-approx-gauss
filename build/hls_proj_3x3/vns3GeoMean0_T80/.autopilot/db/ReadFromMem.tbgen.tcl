set moduleName ReadFromMem
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
set C_modelName {ReadFromMem}
set C_modelType { void 0 }
set C_modelArgList {
	{ width int 16 regular  }
	{ height int 16 regular  }
	{ src int 8 regular {array 262144 { 1 3 } 1 1 }  }
	{ pixel_stream3 int 8 regular {fifo 1 volatile }  }
	{ height_c12 int 16 regular {fifo 1}  }
	{ width_c14 int 16 regular {fifo 1}  }
}
set C_modelArgMapList {[ 
	{ "Name" : "width", "interface" : "wire", "bitwidth" : 16, "direction" : "READONLY"} , 
 	{ "Name" : "height", "interface" : "wire", "bitwidth" : 16, "direction" : "READONLY"} , 
 	{ "Name" : "src", "interface" : "memory", "bitwidth" : 8, "direction" : "READONLY"} , 
 	{ "Name" : "pixel_stream3", "interface" : "fifo", "bitwidth" : 8, "direction" : "WRITEONLY"} , 
 	{ "Name" : "height_c12", "interface" : "fifo", "bitwidth" : 16, "direction" : "WRITEONLY"} , 
 	{ "Name" : "width_c14", "interface" : "fifo", "bitwidth" : 16, "direction" : "WRITEONLY"} ]}
# RTL Port declarations: 
set portNum 30
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
	{ width sc_in sc_lv 16 signal 0 } 
	{ height sc_in sc_lv 16 signal 1 } 
	{ src_address0 sc_out sc_lv 18 signal 2 } 
	{ src_ce0 sc_out sc_logic 1 signal 2 } 
	{ src_q0 sc_in sc_lv 8 signal 2 } 
	{ pixel_stream3_din sc_out sc_lv 8 signal 3 } 
	{ pixel_stream3_num_data_valid sc_in sc_lv 2 signal 3 } 
	{ pixel_stream3_fifo_cap sc_in sc_lv 2 signal 3 } 
	{ pixel_stream3_full_n sc_in sc_logic 1 signal 3 } 
	{ pixel_stream3_write sc_out sc_logic 1 signal 3 } 
	{ height_c12_din sc_out sc_lv 16 signal 4 } 
	{ height_c12_num_data_valid sc_in sc_lv 2 signal 4 } 
	{ height_c12_fifo_cap sc_in sc_lv 2 signal 4 } 
	{ height_c12_full_n sc_in sc_logic 1 signal 4 } 
	{ height_c12_write sc_out sc_logic 1 signal 4 } 
	{ width_c14_din sc_out sc_lv 16 signal 5 } 
	{ width_c14_num_data_valid sc_in sc_lv 2 signal 5 } 
	{ width_c14_fifo_cap sc_in sc_lv 2 signal 5 } 
	{ width_c14_full_n sc_in sc_logic 1 signal 5 } 
	{ width_c14_write sc_out sc_logic 1 signal 5 } 
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
 	{ "name": "width", "direction": "in", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "width", "role": "default" }} , 
 	{ "name": "height", "direction": "in", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "height", "role": "default" }} , 
 	{ "name": "src_address0", "direction": "out", "datatype": "sc_lv", "bitwidth":18, "type": "signal", "bundle":{"name": "src", "role": "address0" }} , 
 	{ "name": "src_ce0", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "src", "role": "ce0" }} , 
 	{ "name": "src_q0", "direction": "in", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "src", "role": "q0" }} , 
 	{ "name": "pixel_stream3_din", "direction": "out", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "pixel_stream3", "role": "din" }} , 
 	{ "name": "pixel_stream3_num_data_valid", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "pixel_stream3", "role": "num_data_valid" }} , 
 	{ "name": "pixel_stream3_fifo_cap", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "pixel_stream3", "role": "fifo_cap" }} , 
 	{ "name": "pixel_stream3_full_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "pixel_stream3", "role": "full_n" }} , 
 	{ "name": "pixel_stream3_write", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "pixel_stream3", "role": "write" }} , 
 	{ "name": "height_c12_din", "direction": "out", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "height_c12", "role": "din" }} , 
 	{ "name": "height_c12_num_data_valid", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "height_c12", "role": "num_data_valid" }} , 
 	{ "name": "height_c12_fifo_cap", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "height_c12", "role": "fifo_cap" }} , 
 	{ "name": "height_c12_full_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "height_c12", "role": "full_n" }} , 
 	{ "name": "height_c12_write", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "height_c12", "role": "write" }} , 
 	{ "name": "width_c14_din", "direction": "out", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "width_c14", "role": "din" }} , 
 	{ "name": "width_c14_num_data_valid", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "width_c14", "role": "num_data_valid" }} , 
 	{ "name": "width_c14_fifo_cap", "direction": "in", "datatype": "sc_lv", "bitwidth":2, "type": "signal", "bundle":{"name": "width_c14", "role": "fifo_cap" }} , 
 	{ "name": "width_c14_full_n", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "width_c14", "role": "full_n" }} , 
 	{ "name": "width_c14_write", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "width_c14", "role": "write" }}  ]}

set RtlHierarchyInfo {[
	{"ID" : "0", "Level" : "0", "Path" : "`AUTOTB_DUT_INST", "Parent" : "", "Child" : ["1", "3"],
		"CDFG" : "ReadFromMem",
		"Protocol" : "ap_ctrl_hs",
		"ControlExist" : "1", "ap_start" : "1", "ap_ready" : "1", "ap_done" : "1", "ap_continue" : "1", "ap_idle" : "1", "real_start" : "1",
		"Pipeline" : "None", "UnalignedPipeline" : "0", "RewindPipeline" : "0", "ProcessNetwork" : "0",
		"II" : "0",
		"VariableLatency" : "1", "ExactLatency" : "-1", "EstimateLatencyMin" : "-1", "EstimateLatencyMax" : "-1",
		"Combinational" : "0",
		"Datapath" : "0",
		"ClockEnable" : "0",
		"HasSubDataflow" : "0",
		"InDataflowNetwork" : "1",
		"HasNonBlockingOperation" : "0",
		"IsBlackBox" : "0",
		"Port" : [
			{"Name" : "width", "Type" : "None", "Direction" : "I"},
			{"Name" : "height", "Type" : "None", "Direction" : "I"},
			{"Name" : "src", "Type" : "Memory", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "grp_ReadFromMem_Pipeline_read_image_fu_82", "Port" : "src", "Inst_start_state" : "4", "Inst_end_state" : "5"}]},
			{"Name" : "pixel_stream3", "Type" : "Fifo", "Direction" : "O", "DependentProc" : ["0"], "DependentChan" : "0", "DependentChanDepth" : "2", "DependentChanType" : "0",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "grp_ReadFromMem_Pipeline_read_image_fu_82", "Port" : "pixel_stream3", "Inst_start_state" : "4", "Inst_end_state" : "5"}]},
			{"Name" : "height_c12", "Type" : "Fifo", "Direction" : "O", "DependentProc" : ["0"], "DependentChan" : "0", "DependentChanDepth" : "2", "DependentChanType" : "2",
				"BlockSignal" : [
					{"Name" : "height_c12_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "width_c14", "Type" : "Fifo", "Direction" : "O", "DependentProc" : ["0"], "DependentChan" : "0", "DependentChanDepth" : "2", "DependentChanType" : "2",
				"BlockSignal" : [
					{"Name" : "width_c14_blk_n", "Type" : "RtlSignal"}]}]},
	{"ID" : "1", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.grp_ReadFromMem_Pipeline_read_image_fu_82", "Parent" : "0", "Child" : ["2"],
		"CDFG" : "ReadFromMem_Pipeline_read_image",
		"Protocol" : "ap_ctrl_hs",
		"ControlExist" : "1", "ap_start" : "1", "ap_ready" : "1", "ap_done" : "1", "ap_continue" : "0", "ap_idle" : "1", "real_start" : "0",
		"Pipeline" : "None", "UnalignedPipeline" : "0", "RewindPipeline" : "0", "ProcessNetwork" : "0",
		"II" : "0",
		"VariableLatency" : "1", "ExactLatency" : "-1", "EstimateLatencyMin" : "-1", "EstimateLatencyMax" : "-1",
		"Combinational" : "0",
		"Datapath" : "0",
		"ClockEnable" : "0",
		"HasSubDataflow" : "0",
		"InDataflowNetwork" : "0",
		"HasNonBlockingOperation" : "0",
		"IsBlackBox" : "0",
		"Port" : [
			{"Name" : "mul_ln54", "Type" : "None", "Direction" : "I"},
			{"Name" : "sext_ln54", "Type" : "None", "Direction" : "I"},
			{"Name" : "src", "Type" : "Memory", "Direction" : "I"},
			{"Name" : "conv5", "Type" : "None", "Direction" : "I"},
			{"Name" : "pixel_stream3", "Type" : "Fifo", "Direction" : "O",
				"BlockSignal" : [
					{"Name" : "pixel_stream3_blk_n", "Type" : "RtlSignal"}]}],
		"Loop" : [
			{"Name" : "read_image", "PipelineType" : "UPC",
				"LoopDec" : {"FSMBitwidth" : "1", "FirstState" : "ap_ST_fsm_pp0_stage0", "FirstStateIter" : "ap_enable_reg_pp0_iter1", "FirstStateBlock" : "ap_block_pp0_stage0_subdone", "LastState" : "ap_ST_fsm_pp0_stage0", "LastStateIter" : "ap_enable_reg_pp0_iter2", "LastStateBlock" : "ap_block_pp0_stage0_subdone", "QuitState" : "ap_ST_fsm_pp0_stage0", "QuitStateIter" : "ap_enable_reg_pp0_iter1", "QuitStateBlock" : "ap_block_pp0_stage0_subdone", "OneDepthLoop" : "0", "has_ap_ctrl" : "1", "has_continue" : "0"}}]},
	{"ID" : "2", "Level" : "2", "Path" : "`AUTOTB_DUT_INST.grp_ReadFromMem_Pipeline_read_image_fu_82.flow_control_loop_pipe_sequential_init_U", "Parent" : "1"},
	{"ID" : "3", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.mul_mul_16ns_16ns_32_4_1_U6", "Parent" : "0"}]}


set ArgLastReadFirstWriteLatency {
	ReadFromMem {
		width {Type I LastRead 0 FirstWrite -1}
		height {Type I LastRead 0 FirstWrite -1}
		src {Type I LastRead 1 FirstWrite -1}
		pixel_stream3 {Type O LastRead -1 FirstWrite 2}
		height_c12 {Type O LastRead -1 FirstWrite 0}
		width_c14 {Type O LastRead -1 FirstWrite 0}}
	ReadFromMem_Pipeline_read_image {
		mul_ln54 {Type I LastRead 0 FirstWrite -1}
		sext_ln54 {Type I LastRead 0 FirstWrite -1}
		src {Type I LastRead 1 FirstWrite -1}
		conv5 {Type I LastRead 0 FirstWrite -1}
		pixel_stream3 {Type O LastRead -1 FirstWrite 2}}}

set hasDtUnsupportedChannel 0

set PerformanceInfo {[
	{"Name" : "Latency", "Min" : "-1", "Max" : "-1"}
	, {"Name" : "Interval", "Min" : "-1", "Max" : "-1"}
]}

set PipelineEnableSignalInfo {[
]}

set Spec2ImplPortList { 
	width { ap_none {  { width in_data 0 16 } } }
	height { ap_none {  { height in_data 0 16 } } }
	src { ap_memory {  { src_address0 mem_address 1 18 }  { src_ce0 mem_ce 1 1 }  { src_q0 mem_dout 0 8 } } }
	pixel_stream3 { ap_fifo {  { pixel_stream3_din fifo_port_we 1 8 }  { pixel_stream3_num_data_valid fifo_status_num_data_valid 0 2 }  { pixel_stream3_fifo_cap fifo_update 0 2 }  { pixel_stream3_full_n fifo_status 0 1 }  { pixel_stream3_write fifo_data 1 1 } } }
	height_c12 { ap_fifo {  { height_c12_din fifo_port_we 1 16 }  { height_c12_num_data_valid fifo_status_num_data_valid 0 2 }  { height_c12_fifo_cap fifo_update 0 2 }  { height_c12_full_n fifo_status 0 1 }  { height_c12_write fifo_data 1 1 } } }
	width_c14 { ap_fifo {  { width_c14_din fifo_port_we 1 16 }  { width_c14_num_data_valid fifo_status_num_data_valid 0 2 }  { width_c14_fifo_cap fifo_update 0 2 }  { width_c14_full_n fifo_status 0 1 }  { width_c14_write fifo_data 1 1 } } }
}
