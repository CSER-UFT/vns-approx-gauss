/*
 * AUTO-GENERATED FILE - DO NOT EDIT MANUALLY
 * Generated from: output/vnsSingleSweep/vns_solution_T95.csv
 * Target: 5x5 VNS-Optimized Gaussian Filter (25 taps)
 * Predicted Cost: LUT=423, FF=0, DSP=0
 */

#ifndef VNS_MAPPING_5X5_H_
#define VNS_MAPPING_5X5_H_

#include <ap_int.h>

// Selected approximate multiplier headers
#include "src/1bitTruncated.h"
#include "src/3bitTruncated.h"
#include "src/4bitTruncated.h"
#include "src/bit2Truncated.h"
#include "src/bit3Truncated.h"
#include "src/bit4Truncated.h"
#include "src/bitEspecifico.h"

// Exact 16-bit adders for balanced adder tree
inline ap_int<16> add16se_add1(ap_int<16> a, ap_int<16> b) { return a + b; }
inline ap_int<16> add16se_add2(ap_int<16> a, ap_int<16> b) { return a + b; }
inline ap_int<16> add16se_add3(ap_int<16> a, ap_int<16> b) { return a + b; }
inline ap_int<16> add16se_add4(ap_int<16> a, ap_int<16> b) { return a + b; }

// 5x5 Gaussian Kernel Weights (Sum = 256)
constexpr unsigned char K_TAP_0_0 = 1;
constexpr unsigned char K_TAP_0_1 = 4;
constexpr unsigned char K_TAP_0_2 = 6;
constexpr unsigned char K_TAP_0_3 = 4;
constexpr unsigned char K_TAP_0_4 = 1;
constexpr unsigned char K_TAP_1_0 = 4;
constexpr unsigned char K_TAP_1_1 = 16;
constexpr unsigned char K_TAP_1_2 = 24;
constexpr unsigned char K_TAP_1_3 = 16;
constexpr unsigned char K_TAP_1_4 = 4;
constexpr unsigned char K_TAP_2_0 = 6;
constexpr unsigned char K_TAP_2_1 = 24;
constexpr unsigned char K_TAP_2_2 = 36;
constexpr unsigned char K_TAP_2_3 = 24;
constexpr unsigned char K_TAP_2_4 = 6;
constexpr unsigned char K_TAP_3_0 = 4;
constexpr unsigned char K_TAP_3_1 = 16;
constexpr unsigned char K_TAP_3_2 = 24;
constexpr unsigned char K_TAP_3_3 = 16;
constexpr unsigned char K_TAP_3_4 = 4;
constexpr unsigned char K_TAP_4_0 = 1;
constexpr unsigned char K_TAP_4_1 = 4;
constexpr unsigned char K_TAP_4_2 = 6;
constexpr unsigned char K_TAP_4_3 = 4;
constexpr unsigned char K_TAP_4_4 = 1;

// Per-slot multiplier wrapper functions
// Slot 0: tap(0,0) w=1 -> bit3Truncated (bit3Truncated)
inline ap_int<16> mul_slot_0(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    bit3Truncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 1: tap(0,1) w=4 -> bit4Truncated (bit4Truncated)
inline ap_int<16> mul_slot_1(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    bit4Truncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 2: tap(0,2) w=6 -> bit4Truncated (bit4Truncated)
inline ap_int<16> mul_slot_2(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    bit4Truncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 3: tap(0,3) w=4 -> bit4Truncated (bit4Truncated)
inline ap_int<16> mul_slot_3(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    bit4Truncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 4: tap(0,4) w=1 -> p_4bitTruncated (_4bitTruncated)
inline ap_int<16> mul_slot_4(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    _4bitTruncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 5: tap(1,0) w=4 -> bit2Truncated (bit2Truncated)
inline ap_int<16> mul_slot_5(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    bit2Truncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 6: tap(1,1) w=16 -> p_4bitTruncated (_4bitTruncated)
inline ap_int<16> mul_slot_6(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    _4bitTruncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 7: tap(1,2) w=24 -> p_4bitTruncated (_4bitTruncated)
inline ap_int<16> mul_slot_7(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    _4bitTruncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 8: tap(1,3) w=16 -> p_3bitTruncated (_3bitTruncated)
inline ap_int<16> mul_slot_8(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    _3bitTruncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 9: tap(1,4) w=4 -> bit4Truncated (bit4Truncated)
inline ap_int<16> mul_slot_9(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    bit4Truncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 10: tap(2,0) w=6 -> bitEspecifico (bitEspecifico)
inline ap_int<16> mul_slot_10(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    bitEspecifico(a, b, res);
    return (ap_int<16>)res;
}

// Slot 11: tap(2,1) w=24 -> p_1bitTruncated (_1bitTruncated)
inline ap_int<16> mul_slot_11(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    _1bitTruncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 12: tap(2,2) w=36 -> p_4bitTruncated (_4bitTruncated)
inline ap_int<16> mul_slot_12(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    _4bitTruncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 13: tap(2,3) w=24 -> bit3Truncated (bit3Truncated)
inline ap_int<16> mul_slot_13(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    bit3Truncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 14: tap(2,4) w=6 -> bit4Truncated (bit4Truncated)
inline ap_int<16> mul_slot_14(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    bit4Truncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 15: tap(3,0) w=4 -> bit4Truncated (bit4Truncated)
inline ap_int<16> mul_slot_15(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    bit4Truncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 16: tap(3,1) w=16 -> p_4bitTruncated (_4bitTruncated)
inline ap_int<16> mul_slot_16(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    _4bitTruncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 17: tap(3,2) w=24 -> bit2Truncated (bit2Truncated)
inline ap_int<16> mul_slot_17(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    bit2Truncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 18: tap(3,3) w=16 -> bitEspecifico (bitEspecifico)
inline ap_int<16> mul_slot_18(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    bitEspecifico(a, b, res);
    return (ap_int<16>)res;
}

// Slot 19: tap(3,4) w=4 -> bit4Truncated (bit4Truncated)
inline ap_int<16> mul_slot_19(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    bit4Truncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 20: tap(4,0) w=1 -> bit4Truncated (bit4Truncated)
inline ap_int<16> mul_slot_20(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    bit4Truncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 21: tap(4,1) w=4 -> p_4bitTruncated (_4bitTruncated)
inline ap_int<16> mul_slot_21(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    _4bitTruncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 22: tap(4,2) w=6 -> bit4Truncated (bit4Truncated)
inline ap_int<16> mul_slot_22(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    bit4Truncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 23: tap(4,3) w=4 -> p_4bitTruncated (_4bitTruncated)
inline ap_int<16> mul_slot_23(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    _4bitTruncated(a, b, res);
    return (ap_int<16>)res;
}

// Slot 24: tap(4,4) w=1 -> p_4bitTruncated (_4bitTruncated)
inline ap_int<16> mul_slot_24(ap_uint<8> a, ap_uint<8> b) {
    ap_uint<16> res;
    _4bitTruncated(a, b, res);
    return (ap_int<16>)res;
}

#endif // VNS_MAPPING_5X5_H_
