from pathlib import Path
import argparse
import csv
import numpy as np

from src.image_source import create_demo_image, load_image
from src.qpsk import modulate
from src.channel import add_awgn
from src.receiver import demodulate
from src.metrics import ber, qpsk_theoretical_ber
from src.visualization import plot_ber, plot_constellations, plot_signal_and_fft
from src.image_transmission import run_image_transmission

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RESULTS = ROOT / "results"
DATA.mkdir(exist_ok=True)
RESULTS.mkdir(exist_ok=True)


def run_ber_experiment(bit_count: int, seed: int):
    rng = np.random.default_rng(seed)
    bits = rng.integers(0, 2, bit_count, dtype=np.uint8)
    ebn0_values = np.arange(-2, 13, 2)
    sim_values, theory_values = [], []
    for ebn0_db in ebn0_values:
        tx = modulate(bits)
        rx = add_awgn(tx, float(ebn0_db), 1.0, rng)
        rx_bits = demodulate(rx, len(bits))
        sim = ber(bits, rx_bits)
        theory = qpsk_theoretical_ber(float(ebn0_db))
        sim_values.append(sim)
        theory_values.append(theory)
        print(f"Eb/N0={ebn0_db:>3} dB | BER simulation={sim:.6g} | theory={theory:.6g}")

    with (RESULTS / "ber_results.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["EbN0_dB", "BER_simulation", "BER_theory"])
        writer.writerows(zip(ebn0_values, sim_values, theory_values))
    plot_ber(ebn0_values, sim_values, theory_values, RESULTS)
    return ebn0_values, sim_values, theory_values


def main():
    parser = argparse.ArgumentParser(description="Group 4 QPSK wireless security camera simulation")
    parser.add_argument("--image", type=Path, default=None, help="Optional input image (PNG/JPG)")
    parser.add_argument("--ebn0", type=float, default=8.0, help="Image link Eb/N0 in dB (default 8)")
    parser.add_argument("--attenuation", type=float, default=0.8, help="Amplitude gain in (0, 1] (default 0.8)")
    parser.add_argument("--ber-bits", type=int, default=200000, help="BER experiment bit count")
    parser.add_argument("--seed", type=int, default=7, help="Random seed")
    args = parser.parse_args()

    if args.ber_bits < 100:
        parser.error("--ber-bits must be at least 100")
    if not 0 < args.attenuation <= 1:
        parser.error("--attenuation must be in (0, 1]")

    image_path = args.image
    if image_path is None:
        image_path = DATA / "demo_security_camera.png"
        if not image_path.exists():
            create_demo_image(image_path)
    if not image_path.exists():
        parser.error(f"Image not found: {image_path}")

    print("GROUP 4: WIRELESS SECURITY CAMERA -> CONTROL ROOM")
    print("Model: coherent baseband QPSK + attenuation + AWGN")
    run_ber_experiment(args.ber_bits, args.seed)

    rng = np.random.default_rng(args.seed + 1)
    demo_bits = rng.integers(0, 2, 8000, dtype=np.uint8)
    tx = modulate(demo_bits)
    rx = add_awgn(tx, args.ebn0, args.attenuation, rng)
    plot_constellations(tx, rx, args.ebn0, RESULTS)
    plot_signal_and_fft(tx, RESULTS)

    run_image_transmission(load_image(image_path), args.ebn0, args.attenuation, RESULTS)
    print("\nAll results saved in:", RESULTS)


if __name__ == "__main__":
    main()
