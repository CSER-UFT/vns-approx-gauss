#include <iostream>
#include "2bitTruncated.h"

int main() {
    ap_uint<8> a = 255;
    ap_uint<8> b = 255;
    ap_uint<16> c;

    _2bitTruncated(a, b, c);

    std::cout << "OK! Resultado = " << (int)c << std::endl;
    return 0;
}