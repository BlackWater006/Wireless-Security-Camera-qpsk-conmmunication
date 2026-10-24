from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_ber(ebn0_values, simulated, theoretical, out_dir: Path):
    plt.figure(figsize=(8, 5))
    # A zero simulated BER cannot be drawn on a logarithmic axis; hide zero points.
    sim_plot = [v if v > 0 else np.nan for v in simulated]
    plt.semilogy(ebn0_values, sim_plot, "o-", label="Simulation")
    plt.semilogy(ebn0_values, theoretical, "--", label="Theory")
    plt.xlabel("Eb/N0 (dB)")
    plt.ylabel("BER")
    plt.title("Uncoded QPSK over AWGN")
    plt.grid(True, which="both", linestyle=":")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir / "ber_vs_ebn0.png", dpi=160)
    plt.close()


def plot_constellations(tx, rx, ebn0_db: float, out_dir: Path):
    n = min(5000, len(tx), len(rx))
    for name, symbols, title in (
        ("constellation_before.png", tx, "QPSK constellation before channel"),
        ("constellation_after.png", rx, f"After attenuation + AWGN (Eb/N0={ebn0_db} dB)")
    ):
        plt.figure(figsize=(5.5, 5.5))
        plt.scatter(symbols[:n].real, symbols[:n].imag, s=10, alpha=0.5)
        plt.xlabel("In-phase (I)")
        plt.ylabel("Quadrature (Q)")
        plt.title(title)
        plt.axis("equal")
        plt.grid(True, linestyle=":")
        plt.tight_layout()
        plt.savefig(out_dir / name, dpi=160)
        plt.close()


def plot_signal_and_fft(symbols, out_dir: Path):
    n = min(40, len(symbols))
    plt.figure(figsize=(8, 4))
    plt.plot(np.arange(n), symbols[:n].real, "o-", label="I")
    plt.plot(np.arange(n), symbols[:n].imag, "s-", label="Q")
    plt.xlabel("Symbol index")
    plt.ylabel("Amplitude")
    plt.title("QPSK baseband I/Q symbols")
    plt.grid(True, linestyle=":")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir / "qpsk_time_domain.png", dpi=160)
    plt.close()

    sample = symbols[:min(4096, len(symbols))]
    spectrum = np.fft.fftshift(np.fft.fft(sample))
    freq = np.fft.fftshift(np.fft.fftfreq(len(sample), d=1.0))
    mag = 20 * np.log10(np.maximum(np.abs(spectrum) / len(sample), 1e-12))
    plt.figure(figsize=(8, 4))
    plt.plot(freq, mag)
    plt.xlabel("Normalized frequency (cycles/symbol)")
    plt.ylabel("Magnitude (dB)")
    plt.title("FFT magnitude of QPSK symbol sequence")
    plt.grid(True, linestyle=":")
    plt.tight_layout()
    plt.savefig(out_dir / "qpsk_frequency_domain.png", dpi=160)
    plt.close()
