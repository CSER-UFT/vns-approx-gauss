"""
Hardware-Accurate Gaussian Filter Implementation.
Simulates FPGA / ASIC image processing pipelines using custom 8-bit multipliers.
"""

from typing import Callable, Optional, Tuple, Union
import numpy as np


def get_gaussian_kernel(size: int = 3, sigma: float = 1.0, scale_to_sum: Optional[int] = 256) -> Tuple[np.ndarray, int]:
    """Generates an integer-quantized Gaussian kernel suitable for hardware implementations.
    
    Args:
        size: Kernel dimension (odd integer, typically 3 or 5).
        sigma: Standard deviation of Gaussian function.
        scale_to_sum: Target sum of kernel weights (e.g., 16, 256 for power-of-2 hardware shift).
                      If None, uses standard integer approximations.
                      
    Returns:
        kernel (np.ndarray of uint8): 2D array of kernel weights in [0, 255].
        norm_factor (int): Normalization factor (sum of kernel weights).
    """
    if size == 3 and (scale_to_sum == 16 or scale_to_sum is None):
        # Canonical 3x3 integer kernel (sum = 16, exact >> 4 shift in FPGA)
        kernel = np.array([
            [1, 2, 1],
            [2, 4, 2],
            [1, 2, 1]
        ], dtype=np.uint8)
        return kernel, 16

    if size == 5 and (scale_to_sum == 256 or scale_to_sum is None):
        # Canonical 5x5 integer kernel (sum = 256, exact >> 8 shift in FPGA)
        kernel = np.array([
            [1,  4,  6,  4, 1],
            [4, 16, 24, 16, 4],
            [6, 24, 36, 24, 6],
            [4, 16, 24, 16, 4],
            [1,  4,  6,  4, 1]
        ], dtype=np.uint8)
        return kernel, 256

    # Continuous Gaussian discretization
    radius = size // 2
    y, x = np.mgrid[-radius:radius + 1, -radius:radius + 1]
    kernel_f = np.exp(-(x ** 2 + y ** 2) / (2 * sigma ** 2))
    kernel_f /= np.sum(kernel_f)

    if scale_to_sum is not None:
        kernel = np.round(kernel_f * scale_to_sum).astype(np.int32)
        # Ensure central symmetry and exact sum
        kernel = np.clip(kernel, 0, 255).astype(np.uint8)
        norm_factor = int(np.sum(kernel))
    else:
        # Scale so maximum value fits in 8-bit unsigned
        scale = 255.0 / np.max(kernel_f)
        kernel = np.round(kernel_f * scale).astype(np.uint8)
        norm_factor = int(np.sum(kernel))

    return kernel, norm_factor


def apply_gaussian_filter(
    image: np.ndarray,
    multiplier_fn: Callable[[np.ndarray, np.ndarray], np.ndarray],
    kernel: Optional[np.ndarray] = None,
    norm_factor: Optional[int] = None,
    kernel_size: int = 3,
    sigma: float = 1.0,
    hardware_shift: bool = True
) -> np.ndarray:
    """Applies a 2D Gaussian filter using the specified multiplier hardware model.
    
    Args:
        image: 2D (grayscale) or 3D (H, W, C) numpy array of uint8 [0, 255].
        multiplier_fn: Function simulating the multiplier (e.g. mult_exact, mult_1bit_truncated).
                       Must accept two uint8 / uint16 arrays and return uint16.
        kernel: Optional pre-defined 2D uint8 kernel. If None, generated via get_gaussian_kernel.
        norm_factor: Normalization divisor. If None, sum of kernel weights is used.
        kernel_size: Kernel dimension (if kernel is None).
        sigma: Gaussian sigma (if kernel is None).
        hardware_shift: If True and norm_factor is a power of 2, uses bit-shift >> log2(norm_factor).
        
    Returns:
        Filtered image as uint8 numpy array with identical dimensions.
    """
    if kernel is None:
        target_sum = 16 if kernel_size == 3 else 256
        kernel, norm_factor = get_gaussian_kernel(size=kernel_size, sigma=sigma, scale_to_sum=target_sum)
    elif norm_factor is None:
        norm_factor = int(np.sum(kernel))

    # Handle multi-channel (e.g., RGB)
    if image.ndim == 3:
        channels = []
        for c in range(image.shape[2]):
            ch_filtered = apply_gaussian_filter(
                image[:, :, c], multiplier_fn, kernel, norm_factor, kernel_size, sigma, hardware_shift
            )
            channels.append(ch_filtered)
        return np.stack(channels, axis=2)

    img_uint8 = np.clip(image, 0, 255).astype(np.uint8)
    k_h, k_w = kernel.shape
    pad_h, pad_w = k_h // 2, k_w // 2

    # Pad image boundaries with edge replication (common in hardware line buffers)
    padded = np.pad(img_uint8, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')

    h, w = img_uint8.shape
    acc = np.zeros((h, w), dtype=np.uint32)

    # Accumulate products over the kernel window
    for r in range(k_h):
        for c in range(k_w):
            weight = kernel[r, c]
            if weight == 0:
                continue
            window_slice = padded[r:r + h, c:c + w]
            # Call multiplier model (simulates hardware multiplier IP core)
            prod = multiplier_fn(window_slice, np.uint8(weight))
            acc += prod.astype(np.uint32)

    # Normalization (division or bit-shift)
    is_power_of_2 = (norm_factor > 0) and (norm_factor & (norm_factor - 1) == 0)
    if hardware_shift and is_power_of_2:
        shift = int(np.log2(norm_factor))
        # Optional rounding offset (+ (1 << (shift - 1))) for hardware rounding
        round_offset = 1 << (shift - 1) if shift > 0 else 0
        filtered = (acc + round_offset) >> shift
    else:
        filtered = np.round(acc / norm_factor)

    return np.clip(filtered, 0, 255).astype(np.uint8)
