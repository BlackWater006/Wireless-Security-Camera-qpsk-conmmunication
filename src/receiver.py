import numpy as np


def demodulate(symbols: np.ndarray, original_bit_count: int | None = None) -> np.ndarray:
    """Coherent hard-decision QPSK receiver with ideal carrier/timing sync."""
    bits = np.empty(2 * len(symbols), dtype=np.uint8)
    bits[0::2] = (symbols.real < 0).astype(np.uint8)
    bits[1::2] = (symbols.imag < 0).astype(np.uint8)
    return bits if original_bit_count is None else bits[:original_bit_count]
