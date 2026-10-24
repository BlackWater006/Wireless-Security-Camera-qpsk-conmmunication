import numpy as np


def bits_to_bytes(bits: np.ndarray) -> bytes:
    bits = np.asarray(bits, dtype=np.uint8)
    usable = (len(bits) // 8) * 8
    return np.packbits(bits[:usable]).tobytes() if usable else b""


def bytes_to_bits(payload: bytes) -> np.ndarray:
    if not payload:
        return np.array([], dtype=np.uint8)
    return np.unpackbits(np.frombuffer(payload, dtype=np.uint8))


def modulate(bits: np.ndarray) -> np.ndarray:
    """Unit-energy QPSK: each pair maps to (±1 ± j)/sqrt(2)."""
    bits = np.asarray(bits, dtype=np.uint8)
    if len(bits) % 2:
        bits = np.append(bits, 0)
    pairs = bits.reshape(-1, 2)
    i = 1.0 - 2.0 * pairs[:, 0]
    q = 1.0 - 2.0 * pairs[:, 1]
    return (i + 1j * q) / np.sqrt(2.0)
