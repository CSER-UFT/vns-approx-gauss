#include <iostream>
#include "4bitTruncated.h"

int main() {
    ap_uint<8> a = 255;
    ap_uint<8> b = 255;
    ap_uint<16> c;

    _4bitTruncated(a, b, c);

    std::cout << "OK! Resultado = " << (int)c << std::endl;
    return 0;
}