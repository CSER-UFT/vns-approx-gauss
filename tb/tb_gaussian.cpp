/*
 * tb_gaussian.cpp
 * C-testbench for 5x5 VNS-optimized Gaussian filter (512x512).
 */

#include <iostream>
#include <vector>
#include <cmath>
#include <cstdlib>

#define MAX_IMAGE_WIDTH  512
#define MAX_IMAGE_HEIGHT 512

extern "C" void gaussian(
    const unsigned char  src[MAX_IMAGE_WIDTH*MAX_IMAGE_HEIGHT],
    unsigned char        dst[MAX_IMAGE_WIDTH*MAX_IMAGE_HEIGHT],
    unsigned short height,
    unsigned short width);

int main() {
    const unsigned short width = 512;
    const unsigned short height = 512;

    std::vector<unsigned char> src(width * height, 128);
    std::vector<unsigned char> dst(width * height, 0);

    // Create a 512x512 test pattern (gradient pattern)
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            src[y * width + x] = (unsigned char)((x * 3 + y * 5) % 256);
        }
    }

    std::cout << "[TB 5x5] Running gaussian filter on 512x512 test image..." << std::endl;
    gaussian(src.data(), dst.data(), height, width);

    // Verify border pixels are 0 (5x5 filter has 2-pixel border margin)
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
        std::cerr << "[TB 5x5] FAILED: Border check failed." << std::endl;
        return 1;
    }

    std::cout << "[TB 5x5] Center pixel (256, 256): Input=" << (int)src[256 * width + 256]
              << ", Filtered=" << (int)dst[256 * width + 256] << std::endl;
    std::cout << "[TB 5x5] SUCCESS: 512x512 testbench passed." << std::endl;
    return 0;
}
