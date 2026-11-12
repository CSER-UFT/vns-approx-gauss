set moduleName gaussian
set isTopModule 1
set isCombinational 0
set isDatapathOnly 0
set isPipelined 1
set pipeline_type dataflow
set FunctionProtocol ap_ctrl_hs
set isOneStateSeq 0
set ProfileFlag 0
set StallSigGenFlag 0
set isEnableWaveformDebug 1
set hasInterrupt 0
set C_modelName {gaussian}
set C_modelType { void 0 }
set C_modelArgList {
	{ src int 8 regular {array 262144 { 1 3 } 1 1 }  }
	{ dst int 8 regular {array 262144 { 0 3 } 0 1 }  }
	{ height uint 16 regular  }
	{ width uint 16 regular  }
}
set C_modelArgMapList {[ 
	{ "Name" : "src", "interface" : "memory", "bitwidth" : 8, "direction" : "READONLY"} , 
 	{ "Name" : "dst", "interface" : "memory", "bitwidth" : 8, "direction" : "WRITEONLY"} , 
 	{ "Name" : "height", "interface" : "wire", "bitwidth" : 16, "direction" : "READONLY"} , 
 	{ "Name" : "width", "interface" : "wire", "bitwidth" : 16, "direction" : "READONLY"} ]}
# RTL Port declarations: 
set portNum 28
set portList { 
	{ src_address0 sc_out sc_lv 18 signal 0 } 
	{ src_ce0 sc_out sc_logic 1 signal 0 } 
	{ src_d0 sc_out sc_lv 8 signal 0 } 
	{ src_q0 sc_in sc_lv 8 signal 0 } 
	{ src_we0 sc_out sc_logic 1 signal 0 } 
	{ src_address1 sc_out sc_lv 18 signal 0 } 
	{ src_ce1 sc_out sc_logic 1 signal 0 } 
	{ src_d1 sc_out sc_lv 8 signal 0 } 
	{ src_q1 sc_in sc_lv 8 signal 0 } 
	{ src_we1 sc_out sc_logic 1 signal 0 } 
	{ dst_address0 sc_out sc_lv 18 signal 1 } 
	{ dst_ce0 sc_out sc_logic 1 signal 1 } 
	{ dst_d0 sc_out sc_lv 8 signal 1 } 
	{ dst_q0 sc_in sc_lv 8 signal 1 } 
	{ dst_we0 sc_out sc_logic 1 signal 1 } 
	{ dst_address1 sc_out sc_lv 18 signal 1 } 
	{ dst_ce1 sc_out sc_logic 1 signal 1 } 
	{ dst_d1 sc_out sc_lv 8 signal 1 } 
	{ dst_q1 sc_in sc_lv 8 signal 1 } 
	{ dst_we1 sc_out sc_logic 1 signal 1 } 
	{ height sc_in sc_lv 16 signal 2 } 
	{ width sc_in sc_lv 16 signal 3 } 
	{ ap_clk sc_in sc_logic 1 clock -1 } 
	{ ap_rst sc_in sc_logic 1 reset -1 active_high_sync } 
	{ ap_start sc_in sc_logic 1 start -1 } 
	{ ap_done sc_out sc_logic 1 predone -1 } 
	{ ap_ready sc_out sc_logic 1 ready -1 } 
	{ ap_idle sc_out sc_logic 1 done -1 } 
}
set NewPortList {[ 
	{ "name": "src_address0", "direction": "out", "datatype": "sc_lv", "bitwidth":18, "type": "signal", "bundle":{"name": "src", "role": "address0" }} , 
 	{ "name": "src_ce0", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "src", "role": "ce0" }} , 
 	{ "name": "src_d0", "direction": "out", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "src", "role": "d0" }} , 
 	{ "name": "src_q0", "direction": "in", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "src", "role": "q0" }} , 
 	{ "name": "src_we0", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "src", "role": "we0" }} , 
 	{ "name": "src_address1", "direction": "out", "datatype": "sc_lv", "bitwidth":18, "type": "signal", "bundle":{"name": "src", "role": "address1" }} , 
 	{ "name": "src_ce1", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "src", "role": "ce1" }} , 
 	{ "name": "src_d1", "direction": "out", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "src", "role": "d1" }} , 
 	{ "name": "src_q1", "direction": "in", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "src", "role": "q1" }} , 
 	{ "name": "src_we1", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "src", "role": "we1" }} , 
 	{ "name": "dst_address0", "direction": "out", "datatype": "sc_lv", "bitwidth":18, "type": "signal", "bundle":{"name": "dst", "role": "address0" }} , 
 	{ "name": "dst_ce0", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "dst", "role": "ce0" }} , 
 	{ "name": "dst_d0", "direction": "out", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "dst", "role": "d0" }} , 
 	{ "name": "dst_q0", "direction": "in", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "dst", "role": "q0" }} , 
 	{ "name": "dst_we0", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "dst", "role": "we0" }} , 
 	{ "name": "dst_address1", "direction": "out", "datatype": "sc_lv", "bitwidth":18, "type": "signal", "bundle":{"name": "dst", "role": "address1" }} , 
 	{ "name": "dst_ce1", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "dst", "role": "ce1" }} , 
 	{ "name": "dst_d1", "direction": "out", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "dst", "role": "d1" }} , 
 	{ "name": "dst_q1", "direction": "in", "datatype": "sc_lv", "bitwidth":8, "type": "signal", "bundle":{"name": "dst", "role": "q1" }} , 
 	{ "name": "dst_we1", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "signal", "bundle":{"name": "dst", "role": "we1" }} , 
 	{ "name": "height", "direction": "in", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "height", "role": "default" }} , 
 	{ "name": "width", "direction": "in", "datatype": "sc_lv", "bitwidth":16, "type": "signal", "bundle":{"name": "width", "role": "default" }} , 
 	{ "name": "ap_clk", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "clock", "bundle":{"name": "ap_clk", "role": "default" }} , 
 	{ "name": "ap_rst", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "reset", "bundle":{"name": "ap_rst", "role": "default" }} , 
 	{ "name": "ap_start", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "start", "bundle":{"name": "ap_start", "role": "default" }} , 
 	{ "name": "ap_done", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "predone", "bundle":{"name": "ap_done", "role": "default" }} , 
 	{ "name": "ap_ready", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "ready", "bundle":{"name": "ap_ready", "role": "default" }} , 
 	{ "name": "ap_idle", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "done", "bundle":{"name": "ap_idle", "role": "default" }}  ]}

set RtlHierarchyInfo {[
	{"ID" : "0", "Level" : "0", "Path" : "`AUTOTB_DUT_INST", "Parent" : "", "Child" : ["1", "5", "11", "17", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32"],
		"CDFG" : "gaussian",
		"Protocol" : "ap_ctrl_hs",
		"ControlExist" : "1", "ap_start" : "1", "ap_ready" : "1", "ap_done" : "1", "ap_continue" : "0", "ap_idle" : "1", "real_start" : "0",
		"Pipeline" : "Dataflow", "UnalignedPipeline" : "0", "RewindPipeline" : "0", "ProcessNetwork" : "1",
		"II" : "0",
		"VariableLatency" : "1", "ExactLatency" : "-1", "EstimateLatencyMin" : "-1", "EstimateLatencyMax" : "-1",
		"Combinational" : "0",
		"Datapath" : "0",
		"ClockEnable" : "0",
		"HasSubDataflow" : "1",
		"InDataflowNetwork" : "0",
		"HasNonBlockingOperation" : "0",
		"IsBlackBox" : "0",
		"InputProcess" : [
			{"ID" : "1", "Name" : "ReadFromMem_U0"}],
		"OutputProcess" : [
			{"ID" : "17", "Name" : "WriteToMem_U0"}],
		"Port" : [
			{"Name" : "src", "Type" : "Memory", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "ReadFromMem_U0", "Port" : "src"}]},
			{"Name" : "dst", "Type" : "Memory", "Direction" : "O",
				"SubConnect" : [
					{"ID" : "17", "SubInstance" : "WriteToMem_U0", "Port" : "dst"}]},
			{"Name" : "height", "Type" : "None", "Direction" : "I"},
			{"Name" : "width", "Type" : "None", "Direction" : "I"}]},
	{"ID" : "1", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.ReadFromMem_U0", "Parent" : "0", "Child" : ["2", "4"],
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
					{"ID" : "2", "SubInstance" : "grp_ReadFromMem_Pipeline_read_image_fu_82", "Port" : "src", "Inst_start_state" : "4", "Inst_end_state" : "5"}]},
			{"Name" : "pixel_stream3", "Type" : "Fifo", "Direction" : "O", "DependentProc" : ["5"], "DependentChan" : "21", "DependentChanDepth" : "2", "DependentChanType" : "0",
				"SubConnect" : [
					{"ID" : "2", "SubInstance" : "grp_ReadFromMem_Pipeline_read_image_fu_82", "Port" : "pixel_stream3", "Inst_start_state" : "4", "Inst_end_state" : "5"}]},
			{"Name" : "height_c12", "Type" : "Fifo", "Direction" : "O", "DependentProc" : ["5"], "DependentChan" : "22", "DependentChanDepth" : "2", "DependentChanType" : "2",
				"BlockSignal" : [
					{"Name" : "height_c12_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "width_c14", "Type" : "Fifo", "Direction" : "O", "DependentProc" : ["5"], "DependentChan" : "23", "DependentChanDepth" : "2", "DependentChanType" : "2",
				"BlockSignal" : [
					{"Name" : "width_c14_blk_n", "Type" : "RtlSignal"}]}]},
	{"ID" : "2", "Level" : "2", "Path" : "`AUTOTB_DUT_INST.ReadFromMem_U0.grp_ReadFromMem_Pipeline_read_image_fu_82", "Parent" : "1", "Child" : ["3"],
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
	{"ID" : "3", "Level" : "3", "Path" : "`AUTOTB_DUT_INST.ReadFromMem_U0.grp_ReadFromMem_Pipeline_read_image_fu_82.flow_control_loop_pipe_sequential_init_U", "Parent" : "2"},
	{"ID" : "4", "Level" : "2", "Path" : "`AUTOTB_DUT_INST.ReadFromMem_U0.mul_mul_16ns_16ns_32_4_1_U6", "Parent" : "1"},
	{"ID" : "5", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.Window2D_U0", "Parent" : "0", "Child" : ["6", "7", "8", "10"],
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
		"StartSource" : "1",
		"StartFifo" : "start_for_Window2D_U0_U",
		"Port" : [
			{"Name" : "width", "Type" : "Fifo", "Direction" : "I", "DependentProc" : ["1"], "DependentChan" : "23", "DependentChanDepth" : "2", "DependentChanType" : "2",
				"BlockSignal" : [
					{"Name" : "width_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "height", "Type" : "Fifo", "Direction" : "I", "DependentProc" : ["1"], "DependentChan" : "22", "DependentChanDepth" : "2", "DependentChanType" : "2",
				"BlockSignal" : [
					{"Name" : "height_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "pixel_stream3", "Type" : "Fifo", "Direction" : "I", "DependentProc" : ["1"], "DependentChan" : "21", "DependentChanDepth" : "2", "DependentChanType" : "0",
				"SubConnect" : [
					{"ID" : "8", "SubInstance" : "grp_Window2D_Pipeline_update_window_fu_82", "Port" : "pixel_stream3", "Inst_start_state" : "4", "Inst_end_state" : "5"}]},
			{"Name" : "window_stream", "Type" : "Fifo", "Direction" : "O", "DependentProc" : ["11"], "DependentChan" : "24", "DependentChanDepth" : "2", "DependentChanType" : "0",
				"SubConnect" : [
					{"ID" : "8", "SubInstance" : "grp_Window2D_Pipeline_update_window_fu_82", "Port" : "window_stream", "Inst_start_state" : "4", "Inst_end_state" : "5"}]},
			{"Name" : "height_c11", "Type" : "Fifo", "Direction" : "O", "DependentProc" : ["11"], "DependentChan" : "25", "DependentChanDepth" : "2", "DependentChanType" : "2",
				"BlockSignal" : [
					{"Name" : "height_c11_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "width_c13", "Type" : "Fifo", "Direction" : "O", "DependentProc" : ["11"], "DependentChan" : "26", "DependentChanDepth" : "2", "DependentChanType" : "2",
				"BlockSignal" : [
					{"Name" : "width_c13_blk_n", "Type" : "RtlSignal"}]}]},
	{"ID" : "6", "Level" : "2", "Path" : "`AUTOTB_DUT_INST.Window2D_U0.LineBuffer_U", "Parent" : "5"},
	{"ID" : "7", "Level" : "2", "Path" : "`AUTOTB_DUT_INST.Window2D_U0.LineBuffer_1_U", "Parent" : "5"},
	{"ID" : "8", "Level" : "2", "Path" : "`AUTOTB_DUT_INST.Window2D_U0.grp_Window2D_Pipeline_update_window_fu_82", "Parent" : "5", "Child" : ["9"],
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
	{"ID" : "9", "Level" : "3", "Path" : "`AUTOTB_DUT_INST.Window2D_U0.grp_Window2D_Pipeline_update_window_fu_82.flow_control_loop_pipe_sequential_init_U", "Parent" : "8"},
	{"ID" : "10", "Level" : "2", "Path" : "`AUTOTB_DUT_INST.Window2D_U0.mul_mul_16ns_16ns_32_4_1_U22", "Parent" : "5"},
	{"ID" : "11", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.Filter2D_U0", "Parent" : "0", "Child" : ["12", "16"],
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
		"StartSource" : "5",
		"StartFifo" : "start_for_Filter2D_U0_U",
		"Port" : [
			{"Name" : "width", "Type" : "Fifo", "Direction" : "I", "DependentProc" : ["5"], "DependentChan" : "26", "DependentChanDepth" : "2", "DependentChanType" : "2",
				"BlockSignal" : [
					{"Name" : "width_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "height", "Type" : "Fifo", "Direction" : "I", "DependentProc" : ["5"], "DependentChan" : "25", "DependentChanDepth" : "2", "DependentChanType" : "2",
				"BlockSignal" : [
					{"Name" : "height_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "window_stream", "Type" : "Fifo", "Direction" : "I", "DependentProc" : ["5"], "DependentChan" : "24", "DependentChanDepth" : "2", "DependentChanType" : "0",
				"SubConnect" : [
					{"ID" : "12", "SubInstance" : "grp_Filter2D_Pipeline_apply_filter_VITIS_LOOP_204_1_fu_72", "Port" : "window_stream", "Inst_start_state" : "5", "Inst_end_state" : "6"}]},
			{"Name" : "output_stream4", "Type" : "Fifo", "Direction" : "O", "DependentProc" : ["17"], "DependentChan" : "27", "DependentChanDepth" : "2", "DependentChanType" : "0",
				"SubConnect" : [
					{"ID" : "12", "SubInstance" : "grp_Filter2D_Pipeline_apply_filter_VITIS_LOOP_204_1_fu_72", "Port" : "output_stream4", "Inst_start_state" : "5", "Inst_end_state" : "6"}]},
			{"Name" : "height_c", "Type" : "Fifo", "Direction" : "O", "DependentProc" : ["17"], "DependentChan" : "28", "DependentChanDepth" : "2", "DependentChanType" : "2",
				"BlockSignal" : [
					{"Name" : "height_c_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "width_c", "Type" : "Fifo", "Direction" : "O", "DependentProc" : ["17"], "DependentChan" : "29", "DependentChanDepth" : "2", "DependentChanType" : "2",
				"BlockSignal" : [
					{"Name" : "width_c_blk_n", "Type" : "RtlSignal"}]}]},
	{"ID" : "12", "Level" : "2", "Path" : "`AUTOTB_DUT_INST.Filter2D_U0.grp_Filter2D_Pipeline_apply_filter_VITIS_LOOP_204_1_fu_72", "Parent" : "11", "Child" : ["13", "14", "15"],
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
	{"ID" : "13", "Level" : "3", "Path" : "`AUTOTB_DUT_INST.Filter2D_U0.grp_Filter2D_Pipeline_apply_filter_VITIS_LOOP_204_1_fu_72.mul_8ns_7ns_14_1_1_U31", "Parent" : "12"},
	{"ID" : "14", "Level" : "3", "Path" : "`AUTOTB_DUT_INST.Filter2D_U0.grp_Filter2D_Pipeline_apply_filter_VITIS_LOOP_204_1_fu_72.ama_addmuladd_9ns_9ns_5ns_14ns_15_4_1_U32", "Parent" : "12"},
	{"ID" : "15", "Level" : "3", "Path" : "`AUTOTB_DUT_INST.Filter2D_U0.grp_Filter2D_Pipeline_apply_filter_VITIS_LOOP_204_1_fu_72.flow_control_loop_pipe_sequential_init_U", "Parent" : "12"},
	{"ID" : "16", "Level" : "2", "Path" : "`AUTOTB_DUT_INST.Filter2D_U0.mul_mul_16ns_16ns_32_4_1_U41", "Parent" : "11"},
	{"ID" : "17", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.WriteToMem_U0", "Parent" : "0", "Child" : ["18", "20"],
		"CDFG" : "WriteToMem",
		"Protocol" : "ap_ctrl_hs",
		"ControlExist" : "1", "ap_start" : "1", "ap_ready" : "1", "ap_done" : "1", "ap_continue" : "1", "ap_idle" : "1", "real_start" : "0",
		"Pipeline" : "None", "UnalignedPipeline" : "0", "RewindPipeline" : "0", "ProcessNetwork" : "0",
		"II" : "0",
		"VariableLatency" : "1", "ExactLatency" : "-1", "EstimateLatencyMin" : "6", "EstimateLatencyMax" : "523783",
		"Combinational" : "0",
		"Datapath" : "0",
		"ClockEnable" : "0",
		"HasSubDataflow" : "0",
		"InDataflowNetwork" : "1",
		"HasNonBlockingOperation" : "0",
		"IsBlackBox" : "0",
		"StartSource" : "11",
		"StartFifo" : "start_for_WriteToMem_U0_U",
		"Port" : [
			{"Name" : "width", "Type" : "Fifo", "Direction" : "I", "DependentProc" : ["11"], "DependentChan" : "29", "DependentChanDepth" : "2", "DependentChanType" : "2",
				"BlockSignal" : [
					{"Name" : "width_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "height", "Type" : "Fifo", "Direction" : "I", "DependentProc" : ["11"], "DependentChan" : "28", "DependentChanDepth" : "2", "DependentChanType" : "2",
				"BlockSignal" : [
					{"Name" : "height_blk_n", "Type" : "RtlSignal"}]},
			{"Name" : "output_stream4", "Type" : "Fifo", "Direction" : "I", "DependentProc" : ["11"], "DependentChan" : "27", "DependentChanDepth" : "2", "DependentChanType" : "0",
				"SubConnect" : [
					{"ID" : "18", "SubInstance" : "grp_WriteToMem_Pipeline_write_image_fu_60", "Port" : "output_stream4", "Inst_start_state" : "4", "Inst_end_state" : "5"}]},
			{"Name" : "dst", "Type" : "Memory", "Direction" : "O",
				"SubConnect" : [
					{"ID" : "18", "SubInstance" : "grp_WriteToMem_Pipeline_write_image_fu_60", "Port" : "dst", "Inst_start_state" : "4", "Inst_end_state" : "5"}]}]},
	{"ID" : "18", "Level" : "2", "Path" : "`AUTOTB_DUT_INST.WriteToMem_U0.grp_WriteToMem_Pipeline_write_image_fu_60", "Parent" : "17", "Child" : ["19"],
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
			{"Name" : "mul_ln74", "Type" : "None", "Direction" : "I"},
			{"Name" : "dst", "Type" : "Memory", "Direction" : "O"},
			{"Name" : "sext_ln74", "Type" : "None", "Direction" : "I"},
			{"Name" : "conv11", "Type" : "None", "Direction" : "I"},
			{"Name" : "output_stream4", "Type" : "Fifo", "Direction" : "I",
				"BlockSignal" : [
					{"Name" : "output_stream4_blk_n", "Type" : "RtlSignal"}]}],
		"Loop" : [
			{"Name" : "write_image", "PipelineType" : "UPC",
				"LoopDec" : {"FSMBitwidth" : "1", "FirstState" : "ap_ST_fsm_pp0_stage0", "FirstStateIter" : "ap_enable_reg_pp0_iter1", "FirstStateBlock" : "ap_block_pp0_stage0_subdone", "LastState" : "ap_ST_fsm_pp0_stage0", "LastStateIter" : "ap_enable_reg_pp0_iter3", "LastStateBlock" : "ap_block_pp0_stage0_subdone", "QuitState" : "ap_ST_fsm_pp0_stage0", "QuitStateIter" : "ap_enable_reg_pp0_iter3", "QuitStateBlock" : "ap_block_pp0_stage0_subdone", "OneDepthLoop" : "0", "has_ap_ctrl" : "1", "has_continue" : "0"}}]},
	{"ID" : "19", "Level" : "3", "Path" : "`AUTOTB_DUT_INST.WriteToMem_U0.grp_WriteToMem_Pipeline_write_image_fu_60.flow_control_loop_pipe_sequential_init_U", "Parent" : "18"},
	{"ID" : "20", "Level" : "2", "Path" : "`AUTOTB_DUT_INST.WriteToMem_U0.mul_mul_16ns_10ns_19_4_1_U53", "Parent" : "17"},
	{"ID" : "21", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.pixel_stream_U", "Parent" : "0"},
	{"ID" : "22", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.height_c12_U", "Parent" : "0"},
	{"ID" : "23", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.width_c14_U", "Parent" : "0"},
	{"ID" : "24", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.window_stream_U", "Parent" : "0"},
	{"ID" : "25", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.height_c11_U", "Parent" : "0"},
	{"ID" : "26", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.width_c13_U", "Parent" : "0"},
	{"ID" : "27", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.output_stream_U", "Parent" : "0"},
	{"ID" : "28", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.height_c_U", "Parent" : "0"},
	{"ID" : "29", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.width_c_U", "Parent" : "0"},
	{"ID" : "30", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.start_for_Window2D_U0_U", "Parent" : "0"},
	{"ID" : "31", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.start_for_Filter2D_U0_U", "Parent" : "0"},
	{"ID" : "32", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.start_for_WriteToMem_U0_U", "Parent" : "0"}]}


set ArgLastReadFirstWriteLatency {
	gaussian {
		src {Type I LastRead 1 FirstWrite -1}
		dst {Type O LastRead -1 FirstWrite 3}
		height {Type I LastRead 0 FirstWrite -1}
		width {Type I LastRead 0 FirstWrite -1}}
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
		pixel_stream3 {Type O LastRead -1 FirstWrite 2}}
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
		window_stream {Type O LastRead -1 FirstWrite 3}}
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
		output_stream4 {Type O LastRead -1 FirstWrite 7}}
	WriteToMem {
		width {Type I LastRead 0 FirstWrite -1}
		height {Type I LastRead 0 FirstWrite -1}
		output_stream4 {Type I LastRead 2 FirstWrite -1}
		dst {Type O LastRead -1 FirstWrite 3}}
	WriteToMem_Pipeline_write_image {
		mul_ln74 {Type I LastRead 0 FirstWrite -1}
		dst {Type O LastRead -1 FirstWrite 3}
		sext_ln74 {Type I LastRead 0 FirstWrite -1}
		conv11 {Type I LastRead 0 FirstWrite -1}
		output_stream4 {Type I LastRead 2 FirstWrite -1}}}

set hasDtUnsupportedChannel 0

set PerformanceInfo {[
	{"Name" : "Latency", "Min" : "-1", "Max" : "-1"}
	, {"Name" : "Interval", "Min" : "-1", "Max" : "-1"}
]}

set PipelineEnableSignalInfo {[
]}

set Spec2ImplPortList { 
	src { ap_memory {  { src_address0 mem_address 1 18 }  { src_ce0 mem_ce 1 1 }  { src_d0 mem_din 1 8 }  { src_q0 mem_dout 0 8 }  { src_we0 mem_we 1 1 }  { src_address1 mem_address 1 18 }  { src_ce1 mem_ce 1 1 }  { src_d1 mem_din 1 8 }  { src_q1 mem_dout 0 8 }  { src_we1 mem_we 1 1 } } }
	dst { ap_memory {  { dst_address0 mem_address 1 18 }  { dst_ce0 mem_ce 1 1 }  { dst_d0 mem_din 1 8 }  { dst_q0 mem_dout 0 8 }  { dst_we0 mem_we 1 1 }  { dst_address1 mem_address 1 18 }  { dst_ce1 mem_ce 1 1 }  { dst_d1 mem_din 1 8 }  { dst_q1 mem_dout 0 8 }  { dst_we1 mem_we 1 1 } } }
	height { ap_none {  { height in_data 0 16 } } }
	width { ap_none {  { width in_data 0 16 } } }
}

set maxi_interface_dict [dict create]

# RTL port scheduling information:
set fifoSchedulingInfoList { 
}

# RTL bus port read request latency information:
set busReadReqLatencyList { 
}

# RTL bus port write response latency information:
set busWriteResLatencyList { 
}

# RTL array port load latency information:
set memoryLoadLatencyList { 
}
