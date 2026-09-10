#include <iostream>
#include "3bitTruncated.h"

int main() {
    ap_uint<8> a = 255;
    ap_uint<8> b = 255;
    ap_uint<16> c;

    _3bitTruncated(a, b, c);

    std::cout << "OK! Resultado = " << (int)c << std::endl;
    return 0;
}