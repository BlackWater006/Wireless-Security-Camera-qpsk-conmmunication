import numpy as np
from scipy.special import erfc


def ber(reference_bits: np.ndarray, received_bits: np.ndarray) -> float:
    if len(reference_bits) == 0:
        return 0.0
    if len(reference_bits) != len(received_bits):
        raise ValueError("Reference and received bit arrays must have equal lengths.")
    return float(np.mean(np.asarray(reference_bits) != np.asarray(received_bits)))


def qpsk_theoretical_ber(ebn0_db: float) -> float:
    ebn0 = 10.0 ** (ebn0_db / 10.0)
    return float(0.5 * erfc(np.sqrt(ebn0)))


def psnr(original: np.ndarray, reconstructed: np.ndarray) -> float:
    a = np.asarray(original, dtype=np.float64)
    b = np.asarray(reconstructed, dtype=np.float64)
    if a.shape != b.shape:
        raise ValueError("Images must have the same shape for PSNR.")
    mse = float(np.mean((a - b) ** 2))
    return float("inf") if mse == 0 else float(10.0 * np.log10(255.0**2 / mse))
