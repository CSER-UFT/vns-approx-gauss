#include <ap_int.h>

void bitEspecifico(ap_uint<8> a, ap_uint<8> b, ap_uint<16> &c) {
    #pragma HLS INTERFACE ap_none port=a
    #pragma HLS INTERFACE ap_none port=b
    #pragma HLS INTERFACE ap_none port=c
    #pragma HLS INTERFACE ap_ctrl_none port=return

    const int posicao = 1; 

    ap_uint<8> mascara = (1 << posicao) - 1;

    ap_uint<7> a_trunc = (a >> (posicao + 1) << posicao) | (a & mascara);
    ap_uint<7> b_trunc = (b >> (posicao + 1) << posicao) | (b & mascara);

    ap_uint<14> produto_trunc = a_trunc * b_trunc;

    c = (ap_uint<16>)produto_trunc << 2;
}