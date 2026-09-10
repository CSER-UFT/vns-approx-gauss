#include <iostream>
#include "2bitTruncated.h"

int main() {
    ap_uint<8> a = 255;
    ap_uint<8> b = 255;
    ap_uint<16> c;

    bitEspecifico(a, b, c);

    // if (c != 30) {
    //     std::cout << "Erro!" << std::endl;
    //     return 1;
    // }

    std::cout << "OK! Resultado = " << (int)c << std::endl;
    return 0;
}