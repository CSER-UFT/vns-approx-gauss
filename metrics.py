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

    # 11x11 Gaussian window with sigma=1.5
    truncate_radius = 5
    x = np.arange(-truncate_radius, truncate_radius + 1)
    kernel_1d = np.exp(-0.5 * (x / 1.5) ** 2)
    kernel_1d /= np.sum(kernel_1d)
    kernel_2d = np.outer(kernel_1d, kernel_1d)

    # 2D convolution helper
    def convolve(img):
        # Pad image with reflection
        pad = truncate_radius
        padded = np.pad(img, pad, mode='reflect')
        # Vectorized 2D window convolution using stride/sum
        h, w = img.shape
        out = np.zeros((h, w), dtype=np.float64)
        for i in range(2 * truncate_radius + 1):
            for j in range(2 * truncate_radius + 1):
                out += padded[i:i + h, j:j + w] * kernel_2d[i, j]
        return out

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
