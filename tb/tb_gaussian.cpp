/*
 * tb_gaussian.cpp
 * C-testbench for 5x5 VNS-optimized Gaussian filter.
 */

#include <iostream>
#include <vector>
#include <cmath>
#include <cstdlib>

#define MAX_IMAGE_WIDTH  4096
#define MAX_IMAGE_HEIGHT 4096

extern "C" void gaussian(
    const unsigned char  src[MAX_IMAGE_WIDTH*MAX_IMAGE_HEIGHT],
    unsigned char        dst[MAX_IMAGE_WIDTH*MAX_IMAGE_HEIGHT],
    unsigned short height,
    unsigned short width);

int main() {
    const unsigned short width = 64;
    const unsigned short height = 64;

    std::vector<unsigned char> src(width * height, 128);
    std::vector<unsigned char> dst(width * height, 0);

    // Create a simple test pattern (checker / gradient)
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            src[y * width + x] = (unsigned char)((x * 4 + y * 4) % 256);
        }
    }

    std::cout << "[TB] Running gaussian filter on 64x64 test image..." << std::endl;
    gaussian(src.data(), dst.data(), height, width);

    // Verify border pixels are 0
    bool border_ok = true;
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            if ((y <= 1) || (y >= height - 2) || (x <= 1) || (x >= width - 2)) {
                if (dst[y * width + x] != 0) {
                    border_ok = false;
                }
            }
        }
    }

    if (!border_ok) {
        std::cerr << "[TB] FAILED: Border check failed." << std::endl;
        return 1;
    }

    std::cout << "[TB] Center pixel (32, 32): Input=" << (int)src[32 * width + 32]
              << ", Filtered=" << (int)dst[32 * width + 32] << std::endl;
    std::cout << "[TB] SUCCESS: Testbench passed." << std::endl;
    return 0;
}
