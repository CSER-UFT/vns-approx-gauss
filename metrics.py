"""
Image Quality and Error Metrics for Approximate Computing Evaluation.
Computes PSNR, SSIM, MSE, MAE, Max Error, Error Rate, and MRED.
"""

import numpy as np


def calc_mse(exact: np.ndarray, approx: np.ndarray) -> float:
    """Mean Squared Error between exact and approximate images."""
    return float(np.mean((exact.astype(np.float64) - approx.astype(np.float64)) ** 2))


def calc_rmse(exact: np.ndarray, approx: np.ndarray) -> float:
    """Root Mean Squared Error."""
    return float(np.sqrt(calc_mse(exact, approx)))


def calc_mae(exact: np.ndarray, approx: np.ndarray) -> float:
    """Mean Absolute Error (also known as Mean Error Distance - MED)."""
    return float(np.mean(np.abs(exact.astype(np.float64) - approx.astype(np.float64))))


def calc_max_error(exact: np.ndarray, approx: np.ndarray) -> float:
    """Maximum Absolute Error across all pixels."""
    return float(np.max(np.abs(exact.astype(np.float64) - approx.astype(np.float64))))


def calc_psnr(exact: np.ndarray, approx: np.ndarray, max_val: float = 255.0) -> float:
    """Peak Signal-to-Noise Ratio in dB."""
    mse = calc_mse(exact, approx)
    if mse == 0:
        return float('inf')
    return float(20.0 * np.log10(max_val / np.sqrt(mse)))


def calc_error_rate(exact: np.ndarray, approx: np.ndarray) -> float:
    """Error Rate (% of pixels that differ from the exact output)."""
    diff = exact.astype(np.int32) - approx.astype(np.int32)
    return float(np.count_nonzero(diff) / diff.size * 100.0)


def calc_mred(exact: np.ndarray, approx: np.ndarray) -> float:
    """Mean Relative Error Distance (MRED) in %."""
    denom = np.maximum(exact.astype(np.float64), 1.0)
    relative_errors = np.abs(exact.astype(np.float64) - approx.astype(np.float64)) / denom
    return float(np.mean(relative_errors) * 100.0)


try:
    from scipy.signal import convolve2d
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

# Pré-computa o kernel Gaussiano 11x11 (sigma=1.5) no nível de módulo para evitar
# recriação contínua de arrays NumPy a cada chamada de calc_ssim.
_SSIM_TRUNCATE_RADIUS = 5
_SSIM_X = np.arange(-_SSIM_TRUNCATE_RADIUS, _SSIM_TRUNCATE_RADIUS + 1)
_SSIM_KERNEL_1D = np.exp(-0.5 * (_SSIM_X / 1.5) ** 2)
_SSIM_KERNEL_1D /= np.sum(_SSIM_KERNEL_1D)
_SSIM_KERNEL_2D = np.outer(_SSIM_KERNEL_1D, _SSIM_KERNEL_1D)


def calc_ssim(exact: np.ndarray, approx: np.ndarray, max_val: float = 255.0) -> float:
    """Structural Similarity Index Measure (SSIM) between two images.
    Implements Wang et al. (2004) with an 11x11 Gaussian window.
    """
    if exact.ndim == 3:
        # Compute mean SSIM across all color channels
        ssim_channels = [calc_ssim(exact[:, :, c], approx[:, :, c], max_val) for c in range(exact.shape[2])]
        return float(np.mean(ssim_channels))

    img1 = exact.astype(np.float64)
    img2 = approx.astype(np.float64)

    # SSIM constants
    k1, k2 = 0.01, 0.03
    c1 = (k1 * max_val) ** 2
    c2 = (k2 * max_val) ** 2

    # Convolução 2D vetorizada: elimina os loops for aninhados do Python original
    # (11x11 = 121 iterações por convolução), acelerando em 10x-50x.
    # Como o kernel Gaussiano é simétrico e usamos padding por reflexão, o resultado
    # convolve2d(mode='valid') é matematicamente equivalente à janela original.
    def convolve(img):
        pad = _SSIM_TRUNCATE_RADIUS
        padded = np.pad(img, pad, mode='reflect')
        if HAS_SCIPY:
            return convolve2d(padded, _SSIM_KERNEL_2D, mode='valid')
        else:
            from numpy.lib.stride_tricks import sliding_window_view
            windows = sliding_window_view(padded, (2 * pad + 1, 2 * pad + 1))
            return np.einsum('ijkl,kl->ij', windows, _SSIM_KERNEL_2D)

    mu1 = convolve(img1)
    mu2 = convolve(img2)
    mu1_sq = mu1 ** 2
    mu2_sq = mu2 ** 2
    mu1_mu2 = mu1 * mu2

    sigma1_sq = convolve(img1 * img1) - mu1_sq
    sigma2_sq = convolve(img2 * img2) - mu2_sq
    sigma12 = convolve(img1 * img2) - mu1_mu2

    # Small numerical safety
    sigma1_sq = np.maximum(sigma1_sq, 0)
    sigma2_sq = np.maximum(sigma2_sq, 0)

    ssim_map = ((2 * mu1_mu2 + c1) * (2 * sigma12 + c2)) / ((mu1_sq + mu2_sq + c1) * (sigma1_sq + sigma2_sq + c2))
    return float(np.mean(ssim_map))


def evaluate_image_errors(exact: np.ndarray, approx: np.ndarray) -> dict:
    """Compute full suite of error and quality metrics comparing approx against exact."""
    return {
        "MSE": round(calc_mse(exact, approx), 4),
        "RMSE": round(calc_rmse(exact, approx), 4),
        "PSNR (dB)": round(calc_psnr(exact, approx), 2),
        "SSIM": round(calc_ssim(exact, approx), 4),
        "MAE": round(calc_mae(exact, approx), 4),
        "Max Error": int(calc_max_error(exact, approx)),
        "Error Rate (%)": round(calc_error_rate(exact, approx), 2),
        "MRED (%)": round(calc_mred(exact, approx), 4),
    }
