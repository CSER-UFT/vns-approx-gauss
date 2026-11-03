/*
 * gaussian_vns_5x5.cpp
 * 
 * VNS-Optimized 5x5 Gaussian Filter for Vitis HLS.
 * 
 * Approximate multipliers are assigned per tap position (slot 0..24, row-major order)
 * based on the VNS DSE solution. All adders remain exact.
 * 
 * DATAFLOW Pipeline:
 * ReadFromMem -> Window2D -> Filter2D -> WriteToMem
 */

#include <stdio.h>
#include <string.h>
#include <assert.h>
#include "hls_stream.h"
#include "ap_int.h"

// Per-slot multiplier bindings and constexpr kernel weights
#include "vns_mapping_5x5.h"

#define MAX_IMAGE_WIDTH     512
#define MAX_IMAGE_HEIGHT    512

#define FILTER_V_SIZE       5
#define FILTER_H_SIZE       5

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
    // Line buffers - stores 4 (FILTER_V_SIZE-1) entire pixel lines
    U8 LineBuffer[FILTER_V_SIZE-1][MAX_IMAGE_WIDTH];
#pragma HLS ARRAY_PARTITION variable=LineBuffer dim=1 complete
#pragma HLS DEPENDENCE variable=LineBuffer inter false
#pragma HLS DEPENDENCE variable=LineBuffer intra false

    // Sliding window of 5x5 pixels
    window Window;

    unsigned col_ptr = 0;
    unsigned ramp_up = width * ((FILTER_V_SIZE-1)/2) + (FILTER_H_SIZE-1)/2; // width * 2 + 2
    unsigned num_pixels = width * height;
    unsigned num_iterations = num_pixels + ramp_up;

    const unsigned max_iterations = MAX_IMAGE_WIDTH*MAX_IMAGE_HEIGHT + MAX_IMAGE_WIDTH*2 + 2;

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
 * Computes the 5x5 approximate convolution.
 * - 25 multiplications using VNS-selected multipliers per tap (slot 0..24)
 * - 5-level balanced exact 16-bit adder tree
 * - Normalization: hardware rounding and >> 8 shift ((sum + 128) >> 8)
 * - Saturation: clamped to [0, 255]
 */
ap_int<16> filter(const window w) {
#pragma HLS inline

    ap_int<16> x1, x2, x3, x4, x5, x6, x7, x8, x9, x10,
               x11, x12, x13, x14, x15, x16, x17, x18, x19, x20,
               x21, x22, x23, x24, x25;

    // --- Multiplier stage (25 taps in row-major order) ---
    // Row 0
    x1  = mul_slot_0(w.pix[0][0], K_TAP_0_0);
    x2  = mul_slot_1(w.pix[0][1], K_TAP_0_1);
    x3  = mul_slot_2(w.pix[0][2], K_TAP_0_2);
    x4  = mul_slot_3(w.pix[0][3], K_TAP_0_3);
    x5  = mul_slot_4(w.pix[0][4], K_TAP_0_4);

    // Row 1
    x6  = mul_slot_5(w.pix[1][0], K_TAP_1_0);
    x7  = mul_slot_6(w.pix[1][1], K_TAP_1_1);
    x8  = mul_slot_7(w.pix[1][2], K_TAP_1_2);
    x9  = mul_slot_8(w.pix[1][3], K_TAP_1_3);
    x10 = mul_slot_9(w.pix[1][4], K_TAP_1_4);

    // Row 2
    x11 = mul_slot_10(w.pix[2][0], K_TAP_2_0);
    x12 = mul_slot_11(w.pix[2][1], K_TAP_2_1);
    x13 = mul_slot_12(w.pix[2][2], K_TAP_2_2);
    x14 = mul_slot_13(w.pix[2][3], K_TAP_2_3);
    x15 = mul_slot_14(w.pix[2][4], K_TAP_2_4);

    // Row 3
    x16 = mul_slot_15(w.pix[3][0], K_TAP_3_0);
    x17 = mul_slot_16(w.pix[3][1], K_TAP_3_1);
    x18 = mul_slot_17(w.pix[3][2], K_TAP_3_2);
    x19 = mul_slot_18(w.pix[3][3], K_TAP_3_3);
    x20 = mul_slot_19(w.pix[3][4], K_TAP_3_4);

    // Row 4
    x21 = mul_slot_20(w.pix[4][0], K_TAP_4_0);
    x22 = mul_slot_21(w.pix[4][1], K_TAP_4_1);
    x23 = mul_slot_22(w.pix[4][2], K_TAP_4_2);
    x24 = mul_slot_23(w.pix[4][3], K_TAP_4_3);
    x25 = mul_slot_24(w.pix[4][4], K_TAP_4_4);

    // --- Balanced Adder Tree (Exact 16-bit adders) ---
    // Level 1: 12 additions (x26..x37), 1 pass-through (x25)
    ap_int<16> x26 = add16se_add1(x1,  x2);
    ap_int<16> x27 = add16se_add1(x3,  x4);
    ap_int<16> x28 = add16se_add1(x5,  x6);
    ap_int<16> x29 = add16se_add1(x7,  x8);
    ap_int<16> x30 = add16se_add1(x9,  x10);
    ap_int<16> x31 = add16se_add1(x11, x12);
    ap_int<16> x32 = add16se_add1(x13, x14);
    ap_int<16> x33 = add16se_add1(x15, x16);
    ap_int<16> x34 = add16se_add1(x17, x18);
    ap_int<16> x35 = add16se_add1(x19, x20);
    ap_int<16> x36 = add16se_add1(x21, x22);
    ap_int<16> x37 = add16se_add1(x23, x24);

    // Level 2: 6 additions (x38..x43), 1 pass-through (x25)
    ap_int<16> x38 = add16se_add2(x26, x27);
    ap_int<16> x39 = add16se_add2(x28, x29);
    ap_int<16> x40 = add16se_add2(x30, x31);
    ap_int<16> x41 = add16se_add2(x32, x33);
    ap_int<16> x42 = add16se_add2(x34, x35);
    ap_int<16> x43 = add16se_add2(x36, x37);

    // Level 3: 3 additions (x44..x46), 1 pass-through (x25)
    ap_int<16> x44 = add16se_add3(x38, x39);
    ap_int<16> x45 = add16se_add3(x40, x41);
    ap_int<16> x46 = add16se_add3(x42, x43);

    // Level 4: 2 additions (x47..x48)
    ap_int<16> x47 = add16se_add4(x44, x45);
    ap_int<16> x48 = add16se_add4(x46, x25);

    // Level 5: 1 addition (accumulator sum)
    ap_int<16> sum = add16se_add4(x47, x48);

    // Hardware rounding (+ 128) and >> 8 shift (kernel sum = 256)
    ap_int<16> norm_val = (sum + 128) >> 8;

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
            // Border check: 2-pixel margin for 5x5 kernel (output 0 at borders)
            if ((i > 1) & (i < height - 2) & (j > 1) & (j < width - 2)) {
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

    // Form 5x5 sliding window using line buffers
    Window2D(width, height, pixel_stream, window_stream);

    // Apply 5x5 approximate convolution
    Filter2D(width, height, window_stream, output_stream);

    // Stream pixels back to global memory over AXI4
    WriteToMem(width, height, width, output_stream, dst);
}

}
