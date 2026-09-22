"""
Approximate and Exact 8-bit Multiplier Models for Hardware Simulation.
Matches the Vitis HLS C++ implementations in `src/`.
"""

import numpy as np


def mult_exact(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Exact 8-bit unsigned multiplier: c = a * b
    Matches `src/multExato.cpp`.
    Inputs: 8-bit unsigned (0-255)
    Output: 16-bit unsigned (0-65025)
    """
    return np.uint16(a) * np.uint16(b)


def mult_1bit_truncated(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """1-bit Truncated Multiplier.
    Matches `src/1bitTruncated.cpp`:
        ap_uint<7> a_trunc = a.range(7,1); // a >> 1
        ap_uint<7> b_trunc = b.range(7,1); // b >> 1
        ap_uint<14> produto_trunc = a_trunc * b_trunc;
        c = (ap_uint<16>)produto_trunc << 2;
    """
    a_trunc = (np.uint16(a) >> 1) & 0x7F
    b_trunc = (np.uint16(b) >> 1) & 0x7F
    prod_trunc = a_trunc * b_trunc
    return np.uint16(prod_trunc << 2)


def mult_2bit_truncated(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """2-bit Truncated Multiplier.
    Matches `src/2bitTruncated.cpp`:
        ap_uint<6> a_trunc = a.range(7,2); // a >> 2
        ap_uint<6> b_trunc = b.range(7,2); // b >> 2
        ap_uint<12> produto_trunc = a_trunc * b_trunc;
        c = (ap_uint<16>)produto_trunc << 4;
    """
    a_trunc = (np.uint16(a) >> 2) & 0x3F
    b_trunc = (np.uint16(b) >> 2) & 0x3F
    prod_trunc = a_trunc * b_trunc
    return np.uint16(prod_trunc << 4)


def mult_3bit_truncated(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """3-bit Truncated Multiplier (zeros in truncated positions).
    Matches `src/3bitTruncated.cpp`:
        ap_uint<5> a_trunc = a.range(7,3); // a >> 3
        ap_uint<5> b_trunc = b.range(7,3); // b >> 3
        ap_uint<10> produto_trunc = a_trunc * b_trunc;
        c = (ap_uint<16>)produto_trunc << 6;
    """
    a_trunc = (np.uint16(a) >> 3) & 0x1F
    b_trunc = (np.uint16(b) >> 3) & 0x1F
    prod_trunc = a_trunc * b_trunc
    return np.uint16(prod_trunc << 6)


def mult_4bit_truncated(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """4-bit Truncated Multiplier (zeros in truncated positions).
    Matches `src/4bitTruncated.cpp`:
        ap_uint<4> a_trunc = a.range(7,4); // a >> 4
        ap_uint<4> b_trunc = b.range(7,4); // b >> 4
        ap_uint<8> produto_trunc = a_trunc * b_trunc;
        c = (ap_uint<16>)produto_trunc << 8;
    """
    a_trunc = (np.uint16(a) >> 4) & 0x0F
    b_trunc = (np.uint16(b) >> 4) & 0x0F
    prod_trunc = a_trunc * b_trunc
    return np.uint16(prod_trunc << 8)


def mult_k_bit_truncated(a: np.ndarray, b: np.ndarray, k: int, fill_ones: bool = False) -> np.ndarray:
    """Parametric k-bit LSB Truncated Multiplier (k in 0..7).
    Truncates k least significant bits before multiplication.
    If fill_ones is True, sets lower 2*k bits to 1 (compensation bias).
    """
    if k == 0:
        return mult_exact(a, b)
    mask = (1 << (8 - k)) - 1
    a_trunc = (np.uint16(a) >> k) & mask
    b_trunc = (np.uint16(b) >> k) & mask
    prod_trunc = a_trunc * b_trunc
    res = np.uint16(prod_trunc << (2 * k))
    if fill_ones:
        res |= np.uint16((1 << (2 * k)) - 1)
    return res


def mult_bit1_truncated(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """1-bit Truncated Multiplier with 1s in truncated positions (bias compensation).
    Matches `src/bit1Truncated.cpp`:
        ap_uint<7> a_trunc = a.range(7,1);
        ap_uint<7> b_trunc = b.range(7,1);
        ap_uint<14> produto_trunc = a_trunc * b_trunc;
        c = ((ap_uint<16>)produto_trunc << 2) | 0b11;
    """
    a_trunc = (np.uint16(a) >> 1) & 0x7F
    b_trunc = (np.uint16(b) >> 1) & 0x7F
    prod_trunc = a_trunc * b_trunc
    return np.uint16((prod_trunc << 2) | 0x03)


def mult_bit2_truncated(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """2-bit Truncated Multiplier with 1s in truncated positions (bias compensation).
    Matches `src/bit2Truncated.cpp`:
        ap_uint<6> a_trunc = a.range(7,2);
        ap_uint<6> b_trunc = b.range(7,2);
        ap_uint<12> produto_trunc = a_trunc * b_trunc;
        c = ((ap_uint<16>)produto_trunc << 4);
        c[0] = c[1] = c[2] = c[3] = 1;
    """
    a_trunc = (np.uint16(a) >> 2) & 0x3F
    b_trunc = (np.uint16(b) >> 2) & 0x3F
    prod_trunc = a_trunc * b_trunc
    return np.uint16((prod_trunc << 4) | 0x0F)


def mult_bit3_truncated(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """3-bit Truncated Multiplier with 1s in truncated positions (bias compensation).
    Matches `src/bit3Truncated.cpp`:
        ap_uint<5> a_trunc = a.range(7,3);
        ap_uint<5> b_trunc = b.range(7,3);
        ap_uint<10> produto_trunc = a_trunc * b_trunc;
        c = ((ap_uint<16>)produto_trunc << 6);
        c[0] = c[1] = c[2] = c[3] = c[4] = c[5] = 1;
    """
    a_trunc = (np.uint16(a) >> 3) & 0x1F
    b_trunc = (np.uint16(b) >> 3) & 0x1F
    prod_trunc = a_trunc * b_trunc
    return np.uint16((prod_trunc << 6) | 0x3F)


def mult_bit4_truncated(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """4-bit Truncated Multiplier with 1s in truncated positions (bias compensation).
    Matches `src/bit4Truncated.cpp`:
        ap_uint<4> a_trunc = a.range(7,4);
        ap_uint<4> b_trunc = b.range(7,4);
        ap_uint<8> produto_trunc = a_trunc * b_trunc;
        c = ((ap_uint<16>)produto_trunc << 8);
        c[0] = ... = c[7] = 1;
    """
    a_trunc = (np.uint16(a) >> 4) & 0x0F
    b_trunc = (np.uint16(b) >> 4) & 0x0F
    prod_trunc = a_trunc * b_trunc
    return np.uint16((prod_trunc << 8) | 0xFF)


def mult_bit_especifico(a: np.ndarray, b: np.ndarray, pos: int = 1) -> np.ndarray:
    """Specific bit truncated multiplier.
    Matches `src/bitEspecifico.cpp`:
    Removes bit at position `pos`, concatenating higher and lower bits.
    """
    mask = (1 << pos) - 1
    a_u = np.uint16(a)
    b_u = np.uint16(b)
    
    a_trunc = ((a_u >> (pos + 1)) << pos) | (a_u & mask)
    b_trunc = ((b_u >> (pos + 1)) << pos) | (b_u & mask)
    prod_trunc = a_trunc * b_trunc
    return np.uint16(prod_trunc << 2)


# Registry of known multipliers and aliases
MULTIPLIER_REGISTRY = {
    # Exact
    "multExato": mult_exact,
    "exact": mult_exact,
    
    # Truncated family (zeros in truncated lower bits)
    "p_1bitTruncated": mult_1bit_truncated,
    "1bitTruncated": mult_1bit_truncated,
    "_1bitTruncated": mult_1bit_truncated,
    
    "p_2bitTruncated": mult_2bit_truncated,
    "2bitTruncated": mult_2bit_truncated,
    "_2bitTruncated": mult_2bit_truncated,
    
    "p_3bitTruncated": mult_3bit_truncated,
    "3bitTruncated": mult_3bit_truncated,
    "_3bitTruncated": mult_3bit_truncated,
    
    "p_4bitTruncated": mult_4bit_truncated,
    "4bitTruncated": mult_4bit_truncated,
    "_4bitTruncated": mult_4bit_truncated,
    
    # Specific bit truncation
    "bitEspecifico": mult_bit_especifico,
    "p_bitEspecifico": mult_bit_especifico,
    "_bitEspecifico": mult_bit_especifico,
    
    # Truncated family with 1s in truncated positions (constant bias compensation)
    "bit1Truncated": mult_bit1_truncated,
    "p_bit1Truncated": mult_bit1_truncated,
    "_bit1Truncated": mult_bit1_truncated,
    
    "bit2Truncated": mult_bit2_truncated,
    "p_bit2Truncated": mult_bit2_truncated,
    "_bit2Truncated": mult_bit2_truncated,
    
    "bit3Truncated": mult_bit3_truncated,
    "p_bit3Truncated": mult_bit3_truncated,
    "_bit3Truncated": mult_bit3_truncated,
    
    "bit4Truncated": mult_bit4_truncated,
    "p_bit4Truncated": mult_bit4_truncated,
    "_bit4Truncated": mult_bit4_truncated,
}


def get_multiplier(name: str):
    """Retrieve multiplier function by name (supports variations and k-bit names)."""
    # 1. Exact lookup
    if name in MULTIPLIER_REGISTRY:
        return MULTIPLIER_REGISTRY[name]
    
    # 2. Clean name (remove leading p_ or _ or trailing spaces)
    clean = name.strip()
    if clean.startswith("p_"):
        clean = clean[2:]
    if clean.startswith("_"):
        clean = clean[1:]
        
    if clean in MULTIPLIER_REGISTRY:
        return MULTIPLIER_REGISTRY[clean]

    for key, fn in MULTIPLIER_REGISTRY.items():
        if key.lower() == clean.lower() or key.lower() == name.lower():
            return fn
            
    # 3. Check for parametric patterns:
    # "bit<k>Truncated" -> fill with ones
    import re
    match_bit_k = re.search(r'bit\s*(\d+)\s*Truncated', name, re.IGNORECASE)
    if match_bit_k:
        k = int(match_bit_k.group(1))
        return lambda a, b: mult_k_bit_truncated(a, b, k, fill_ones=True)

    # "<k>bitTruncated" or "<k>_bit" -> fill with zeros
    match_k_bit = re.search(r'(\d+)\s*bit', name, re.IGNORECASE)
    if match_k_bit:
        k = int(match_k_bit.group(1))
        return lambda a, b: mult_k_bit_truncated(a, b, k, fill_ones=False)
        
    raise ValueError(f"Multiplier '{name}' not found in registry. Available: {list(MULTIPLIER_REGISTRY.keys())}")
