/*
 * gaussian_vns_3x3.cpp
 * 
 * VNS-Optimized 3x3 Gaussian Filter for Vitis HLS.
 * 
 * Approximate multipliers are assigned per tap position (slot 0..8, row-major order)
 * based on the VNS DSE solution. All adders remain exact.
 * 
 * Target Image: 512x512
 * DATAFLOW Pipeline:
 * ReadFromMem -> Window2D -> Filter2D -> WriteToMem
 */

#include <stdio.h>
#include <string.h>
#include <assert.h>
#include "hls_stream.h"
#include "ap_int.h"

// Per-slot multiplier bindings and constexpr kernel weights
#include "vns_mapping_3x3.h"

#define MAX_IMAGE_WIDTH     512
#define MAX_IMAGE_HEIGHT    512

#define FILTER_V_SIZE       3
#define FILTER_H_SIZE       3

#ifndef MIN
#define MIN(a,b) ((a<b)?(a):(b))
#endif

#ifndef MAX
#define MAX(a,b) ((a>b)?(a):(b))
#endif

typedef unsigned char       U8;
typedef unsigned short      U16;
typedef unsigned int        U32;

typedef signed char         I8;
typedef signed short        I16;
typedef signed int          I32;

void ReadFromMem(
        unsigned short       width,
        unsigned short       height,
        unsigned short       stride,
        const unsigned char *src,
        hls::stream<U8>     &pixel_stream)
{
    stride = (stride/64)*64; // Enables auto-widening to 512-bit AXI bus
    unsigned x = 0;
    read_image: for (int n = 0; n < height*stride; n++) {
        U8 pix = src[n];
        if (x < width) pixel_stream.write(pix);
        if (x == (stride - 1)) x = 0; else x++;
    }
}

void WriteToMem(
        unsigned short       width,
        unsigned short       height,
        unsigned short       stride,
        hls::stream<U8>     &pixel_stream,
        unsigned char       *dst)
{
    assert(stride <= MAX_IMAGE_WIDTH);
    assert(height <= MAX_IMAGE_HEIGHT);
    assert(stride%64 == 0);

    stride = (stride/64)*64; // Enables auto-widening to 512-bit AXI bus
    unsigned x = 0;
    write_image: for (int n = 0; n < height*stride; n++) {
        U8 pix = (x < width) ? pixel_stream.read() : 0;
        dst[n] = pix;
        if (x == (stride - 1)) x = 0; else x++;
    }
}

struct window {
    U8 pix[FILTER_V_SIZE][FILTER_H_SIZE];
};

void Window2D(
        unsigned short        width,
        unsigned short        height,
        hls::stream<U8>      &pixel_stream,
        hls::stream<window>  &window_stream)
{
    // Line buffers - stores 2 (FILTER_V_SIZE-1) entire pixel lines
    U8 LineBuffer[FILTER_V_SIZE-1][MAX_IMAGE_WIDTH];
#pragma HLS ARRAY_PARTITION variable=LineBuffer dim=1 complete
#pragma HLS DEPENDENCE variable=LineBuffer inter false
#pragma HLS DEPENDENCE variable=LineBuffer intra false

    // Sliding window of 3x3 pixels
    window Window;

    unsigned col_ptr = 0;
    unsigned ramp_up = width * ((FILTER_V_SIZE-1)/2) + (FILTER_H_SIZE-1)/2; // width * 1 + 1
    unsigned num_pixels = width * height;
    unsigned num_iterations = num_pixels + ramp_up;

    const unsigned max_iterations = MAX_IMAGE_WIDTH*MAX_IMAGE_HEIGHT + MAX_IMAGE_WIDTH*1 + 1;

    update_window: for (int n = 0; n < num_iterations; n++)
    {
#pragma HLS LOOP_TRIPCOUNT max=max_iterations
#pragma HLS PIPELINE II=1

        // Read pixel or 0 beyond image boundary
        U8 new_pixel = (n < num_pixels) ? pixel_stream.read() : 0;

        // Shift window horizontally and bring new column from line buffers + input
        for (int i = 0; i < FILTER_V_SIZE; i++) {
            for (int j = 0; j < FILTER_H_SIZE-1; j++) {
                Window.pix[i][j] = Window.pix[i][j+1];
            }
            Window.pix[i][FILTER_H_SIZE-1] = (i < FILTER_V_SIZE-1) ? LineBuffer[i][col_ptr] : new_pixel;
        }

        // Shift column vertically in line buffers, store new pixel at bottom line
        for (int i = 0; i < FILTER_V_SIZE-2; i++) {
            LineBuffer[i][col_ptr] = LineBuffer[i+1][col_ptr];
        }
        LineBuffer[FILTER_V_SIZE-2][col_ptr] = new_pixel;

        // Line buffer column pointer
        if (col_ptr == (width - 1)) {
            col_ptr = 0;
        } else {
            col_ptr++;
        }

        // Push window only after line buffers ramp up
        if (n >= ramp_up) {
            window_stream.write(Window);
        }
    }
}

/*
 * filter():
 * Computes the 3x3 approximate convolution.
 * - 9 multiplications using VNS-selected multipliers per tap (slot 0..8)
 * - 4-level balanced exact 16-bit adder tree
 * - Normalization: hardware rounding and >> shift ((sum + K_NORM_OFFSET) >> K_NORM_SHIFT)
 * - Saturation: clamped to [0, 255]
 */
ap_int<16> filter(const window w) {
#pragma HLS inline

    ap_int<16> x1, x2, x3, x4, x5, x6, x7, x8, x9;

    // --- Multiplier stage (9 taps in row-major order: slot 0..8) ---
    // Row 0
    x1 = mul_slot_0(w.pix[0][0], K_TAP_0_0);
    x2 = mul_slot_1(w.pix[0][1], K_TAP_0_1);
    x3 = mul_slot_2(w.pix[0][2], K_TAP_0_2);

    // Row 1
    x4 = mul_slot_3(w.pix[1][0], K_TAP_1_0);
    x5 = mul_slot_4(w.pix[1][1], K_TAP_1_1);
    x6 = mul_slot_5(w.pix[1][2], K_TAP_1_2);

    // Row 2
    x7 = mul_slot_6(w.pix[2][0], K_TAP_2_0);
    x8 = mul_slot_7(w.pix[2][1], K_TAP_2_1);
    x9 = mul_slot_8(w.pix[2][2], K_TAP_2_2);

    // --- Balanced Adder Tree (Exact 16-bit adders) ---
    // Level 1: 4 additions, 1 pass-through (x9)
    ap_int<16> x10 = add16se_add1(x1, x2);
    ap_int<16> x11 = add16se_add1(x3, x4);
    ap_int<16> x12 = add16se_add1(x5, x6);
    ap_int<16> x13 = add16se_add1(x7, x8);

    // Level 2: 2 additions, 1 pass-through (x9)
    ap_int<16> x14 = add16se_add2(x10, x11);
    ap_int<16> x15 = add16se_add2(x12, x13);

    // Level 3: 1 addition, 1 pass-through (x9)
    ap_int<16> x16 = add16se_add3(x14, x15);

    // Level 4: 1 addition (accumulator sum)
    ap_int<16> sum = add16se_add4(x16, x9);

    // Hardware rounding and normalization shift
    ap_int<16> norm_val = (sum + K_NORM_OFFSET) >> K_NORM_SHIFT;

    // Saturation to [0, 255]
    return MAX((ap_int<16>)0, MIN((ap_int<16>)255, norm_val));
}

void Filter2D(
        unsigned short       width,
        unsigned short       height,
        hls::stream<window> &window_stream,
        hls::stream<U8>     &pixel_stream)
{
    apply_filter: for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
#pragma HLS PIPELINE II=1
            // Read incoming window
            window w = window_stream.read();

            int sum = 0;
            // Border check: 1-pixel margin for 3x3 kernel (output 0 at borders)
            if ((i > 0) & (i < height - 1) & (j > 0) & (j < width - 1)) {
                sum = filter(w);
            }

            unsigned char outpix = (unsigned char)sum;
            pixel_stream.write(outpix);
        }
    }
}

extern "C" {

void gaussian(
        const unsigned char  src[MAX_IMAGE_WIDTH*MAX_IMAGE_HEIGHT],
        unsigned char        dst[MAX_IMAGE_WIDTH*MAX_IMAGE_HEIGHT], 
        unsigned short height, 
        unsigned short width)
{
#pragma HLS DATAFLOW
    hls::stream<U8>      pixel_stream;
    hls::stream<window>  window_stream;
    hls::stream<U8>      output_stream;

    // Stream pixels from global memory over AXI4
    ReadFromMem(width, height, width, src, pixel_stream);

    // Form 3x3 sliding window using line buffers
    Window2D(width, height, pixel_stream, window_stream);

    // Apply 3x3 approximate convolution
    Filter2D(width, height, window_stream, output_stream);

    // Stream pixels back to global memory over AXI4
    WriteToMem(width, height, width, output_stream, dst);
}

}
