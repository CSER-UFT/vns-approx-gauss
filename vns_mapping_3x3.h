/*
 * AUTO-GENERATED FILE - DO NOT EDIT MANUALLY
 * Generated from: output/vns3GeoMean350/vns_solution_T95.csv
 * Target: 3x3 VNS-Optimized Gaussian Filter (9 taps)
 * Kernel Sum: 256 (Norm Shift: >> 8, Offset: + 128)
 * Predicted Cost: LUT=117, FF=0, DSP=0
 */

#ifndef VNS_MAPPING_3X3_H_
#define VNS_MAPPING_3X3_H_

#include <ap_int.h>

// Selected approximate multiplier headers
#include "src/4bitTruncated.h"

// Exact 16-bit signed adders for balanced adder tree
inline ap_int<16> add16se_add1(ap_int<16> a, ap_int<16> b) { return a + b; }
inline ap_int<16> add16se_add2(ap_int<16> a, ap_int<16> b) { return a + b; }
inline ap_int<16> add16se_add3(ap_int<16> a, ap_int<16> b) { return a + b; }
inline ap_int<16> add16se_add4(ap_int<16> a, ap_int<16> b) { return a + b; }

// Normalization parameters (Kernel Sum = 256)
constexpr int K_NORM_FACTOR = 256;
constexpr int K_NORM_SHIFT  = 8;
constexpr int K_NORM_OFFSET = 128;

// 3x3 Gaussian Kernel Weights
constexpr unsigned char K_TAP_0_0 = 19;
constexpr unsigned char K_TAP_0_1 = 32;
constexpr unsigned char K_TAP_0_2 = 19;
constexpr unsigned char K_TAP_1_0 = 32;
constexpr unsigned char K_TAP_1_1 = 52;
constexpr unsigned char K_TAP_1_2 = 32;
constexpr unsigned char K_TAP_2_0 = 19;
constexpr unsigned char K_TAP_2_1 = 32;
constexpr unsigned char K_TAP_2_2 = 19;

// Per-slot multiplier wrapper functions
// Slot 0: tap(0,0) w=19 -> p_4bitTruncated (_4bitTruncated)
inline ap_int<16> mul_slot_0(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    _4bitTruncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 1: tap(0,1) w=32 -> p_4bitTruncated (_4bitTruncated)
inline ap_int<16> mul_slot_1(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    _4bitTruncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 2: tap(0,2) w=19 -> p_4bitTruncated (_4bitTruncated)
inline ap_int<16> mul_slot_2(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    _4bitTruncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 3: tap(1,0) w=32 -> p_4bitTruncated (_4bitTruncated)
inline ap_int<16> mul_slot_3(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    _4bitTruncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 4: tap(1,1) w=52 -> p_4bitTruncated (_4bitTruncated)
inline ap_int<16> mul_slot_4(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    _4bitTruncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 5: tap(1,2) w=32 -> p_4bitTruncated (_4bitTruncated)
inline ap_int<16> mul_slot_5(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    _4bitTruncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 6: tap(2,0) w=19 -> p_4bitTruncated (_4bitTruncated)
inline ap_int<16> mul_slot_6(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    _4bitTruncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 7: tap(2,1) w=32 -> p_4bitTruncated (_4bitTruncated)
inline ap_int<16> mul_slot_7(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    _4bitTruncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 8: tap(2,2) w=19 -> p_4bitTruncated (_4bitTruncated)
inline ap_int<16> mul_slot_8(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    _4bitTruncated(a, b, res);
    return (ap_int<16>)res;
}

#endif // VNS_MAPPING_3X3_H_
