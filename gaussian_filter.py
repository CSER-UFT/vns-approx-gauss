"""
Hardware-Accurate Gaussian Filter Implementation.
Simulates FPGA / ASIC image processing pipelines using custom 8-bit multipliers.
"""

from typing import Callable, Dict, List, Optional, Tuple, Union
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


def group_kernel_by_weight(kernel: np.ndarray) -> Dict[int, List[Tuple[int, int]]]:
    """Agrupa os offsets (r, c) do kernel pelo valor do peso, explorando a
    simetria radial da Gaussiana.

    Base matemática: como a multiplicação é distributiva,
        a*w + b*w = (a + b)*w
    todos os taps do kernel que compartilham o mesmo peso `w` podem ter seus
    pixels somados primeiro (adição barata em hardware) e multiplicados uma
    única vez pelo peso comum, em vez de uma multiplicação por tap.

    Ex.: no kernel 5x5 canônico (soma=256), os 25 taps colapsam em apenas
    6 pesos únicos {1, 4, 6, 16, 24, 36} -> 6 multiplicações em vez de 25.

    Args:
        kernel: kernel 2D (uint8) gerado por get_gaussian_kernel.

    Returns:
        dict {peso: [(r0,c0), (r1,c1), ...]} com os offsets que carregam
        aquele peso. Taps de peso 0 são ignorados (não contribuem).
    """
    groups: Dict[int, List[Tuple[int, int]]] = {}
    k_h, k_w = kernel.shape
    for r in range(k_h):
        for c in range(k_w):
            weight = int(kernel[r, c])
            if weight == 0:
                continue
            groups.setdefault(weight, []).append((r, c))
    return groups


def summarize_symmetry_savings(kernel: np.ndarray) -> Dict[str, Union[int, float]]:
    """Resume o ganho de compartilhamento de multiplicador para um kernel dado.

    Compara o número de multiplicações "ingênuo" (uma por tap não-nulo) com
    o número de multiplicações após agrupar taps de mesmo peso.
    """
    groups = group_kernel_by_weight(kernel)
    naive_mults = int(np.count_nonzero(kernel))
    shared_mults = len(groups)
    reduction_pct = (
        (naive_mults - shared_mults) / naive_mults * 100.0 if naive_mults > 0 else 0.0
    )
    return {
        "unique_weights": shared_mults,
        "naive_multiplications_per_pixel": naive_mults,
        "shared_multiplications_per_pixel": shared_mults,
        "reduction_pct": round(reduction_pct, 2),
        "weights": sorted(groups.keys()),
        "group_sizes": {w: len(v) for w, v in sorted(groups.items())},
    }


def apply_gaussian_filter(
    image: np.ndarray,
    multiplier_fn: Callable[[np.ndarray, np.ndarray], np.ndarray],
    kernel: Optional[np.ndarray] = None,
    norm_factor: Optional[int] = None,
    kernel_size: int = 3,
    sigma: float = 1.0,
    hardware_shift: bool = True,
    exploit_symmetry: bool = False
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
        exploit_symmetry: If True, exploits the kernel's radial symmetry: pixels that
                       share the same kernel weight are pre-added (cheap adder tree)
                       before a single shared multiplication per unique weight,
                       instead of one multiplication per tap (see group_kernel_by_weight).
                       For the canonical 5x5 kernel this drops 25 multiplications/pixel
                       down to 6; for the canonical 3x3 kernel, 9 down to 3.
                       Mathematically identical to the naive path for the exact
                       multiplier; for approximate/truncated multiplier models the
                       result can differ slightly, since the operand fed into the
                       shared multiplier is now a (wider) pre-summed value rather
                       than a single 8-bit pixel.
        
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
                image[:, :, c], multiplier_fn, kernel, norm_factor, kernel_size, sigma,
                hardware_shift, exploit_symmetry
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

    if exploit_symmetry:
        # --- Symmetry-sharing path -----------------------------------------
        # Group taps that carry the same kernel weight. Since
        # a*w + b*w = ... + n*w = (a + b + ... + n)*w, we pre-add (cheap,
        # integer adders) the pixels belonging to the same group and issue a
        # single call to the multiplier model per unique weight, instead of
        # one call per tap. This mirrors an FPGA/ASIC design that shares one
        # multiplier IP core across all taps of equal coefficient, feeding it
        # a wider pre-summed operand from an adder tree.
        weight_groups = group_kernel_by_weight(kernel)
        for weight, offsets in weight_groups.items():
            # Pre-addition tree: sum every pixel window sharing this weight.
            # Use uint32 to avoid overflow (up to k_h*k_w taps of 255 each).
            pixel_sum = np.zeros((h, w), dtype=np.uint32)
            for (r, c) in offsets:
                pixel_sum += padded[r:r + h, c:c + w].astype(np.uint32)

            # Single shared multiplication for the whole group.
            prod = multiplier_fn(pixel_sum, np.uint8(weight))
            acc += prod.astype(np.uint32)
    else:
        # --- Naive path: one multiplication per tap -------------------------
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
