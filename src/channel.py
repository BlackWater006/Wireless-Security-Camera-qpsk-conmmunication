import numpy as np


def add_awgn(symbols: np.ndarray, ebn0_db: float, attenuation: float = 1.0,
             rng: np.random.Generator | None = None) -> np.ndarray:
    """Apply y = a*x + n. Noise is referenced to unit-energy transmitted QPSK."""
    if not 0.0 < attenuation <= 1.0:
        raise ValueError("attenuation must be in (0, 1].")
    if rng is None:
        rng = np.random.default_rng()
    ebn0 = 10.0 ** (ebn0_db / 10.0)
    # Es=1; QPSK has 2 bits/symbol, so Eb=1/2 and N0=Eb/(Eb/N0).
    n0 = 0.5 / ebn0
    noise = np.sqrt(n0 / 2.0) * (
        rng.normal(size=len(symbols)) + 1j * rng.normal(size=len(symbols))
    )
    return attenuation * symbols + noise
