#include <iostream>
#include "bit1Truncated.h"

int main() {
    ap_uint<8> a = 2;
    ap_uint<8> b = 2;
    ap_uint<16> c;

    bit1Truncated(a, b, c);

    std::cout << "OK! Resultado = " << (int)c << std::endl;
    return 0;
}
