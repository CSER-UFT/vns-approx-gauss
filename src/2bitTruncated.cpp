#include <ap_int.h>

void _2bitTruncated(ap_uint<8> a, ap_uint<8> b, ap_uint<16> &c) {
    #pragma HLS INTERFACE ap_none port=a
    #pragma HLS INTERFACE ap_none port=b
    #pragma HLS INTERFACE ap_none port=c
    #pragma HLS INTERFACE ap_ctrl_none port=return

    ap_uint<6> a_trunc = a.range(7,2);
    ap_uint<6> b_trunc = b.range(7,2);

    ap_uint<12> produto_trunc = a_trunc * b_trunc;
    c = (ap_uint<16>)produto_trunc << 4;
}