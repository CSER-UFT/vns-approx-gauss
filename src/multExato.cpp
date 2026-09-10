#include <ap_int.h>

void multExato(ap_uint<8> a, ap_uint<8> b, ap_uint<16> &c) {
    #pragma HLS INTERFACE ap_none port=a
    #pragma HLS INTERFACE ap_none port=b
    #pragma HLS INTERFACE ap_none port=c
    #pragma HLS INTERFACE ap_ctrl_none port=return

    c = a * b;
}