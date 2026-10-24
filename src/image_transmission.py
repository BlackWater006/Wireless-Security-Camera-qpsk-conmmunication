from pathlib import Path
import csv
import numpy as np
from PIL import Image
from .image_source import image_to_bytes, bytes_to_grayscale, decode_jpeg
from .qpsk import bytes_to_bits, bits_to_bytes, modulate
from .channel import add_awgn
from .receiver import demodulate
from .metrics import ber, psnr


def transmit_payload(payload: bytes, ebn0_db: float, attenuation: float, seed: int):
    bits = bytes_to_bits(payload)
    tx = modulate(bits)
    rx = add_awgn(tx, ebn0_db, attenuation, np.random.default_rng(seed))
    recovered_bits = demodulate(rx, len(bits))
    return bits_to_bytes(recovered_bits), ber(bits, recovered_bits), rx


def run_image_transmission(image: Image.Image, ebn0_db: float, attenuation: float,
                           out_dir: Path):
    image = image.convert("RGB")
    gray = image.convert("L")
    gray.save(out_dir / "original_grayscale.png")
    image.save(out_dir / "original_rgb.png")
    records = []

    # Raw grayscale bytes: pixel-by-pixel reconstruction is always possible.
    raw_payload, raw_meta = image_to_bytes(image, "grayscale")
    raw_rx, raw_ber, _ = transmit_payload(raw_payload, ebn0_db, attenuation, 101)
    gray_rx = bytes_to_grayscale(raw_rx, gray.width, gray.height)
    gray_rx.save(out_dir / "reconstructed_grayscale.png")
    raw_psnr = psnr(np.array(gray), np.array(gray_rx))
    records.append({
        "encoding": "raw_grayscale", "payload_bytes": len(raw_payload),
        "ber": raw_ber, "psnr_db": raw_psnr, "decoded": True
    })

    # JPEG is compressed and can fail to decode after channel bit errors.
    jpeg_payload, jpeg_meta = image_to_bytes(image, "jpeg")
    jpeg_baseline = decode_jpeg(jpeg_payload)
    jpeg_baseline.save(out_dir / "jpeg_baseline.png")
    jpeg_rx, jpeg_ber, _ = transmit_payload(jpeg_payload, ebn0_db, attenuation, 202)
    decoded_ok = False
    jpeg_psnr = float("nan")
    try:
        jpeg_image = decode_jpeg(jpeg_rx)
        jpeg_image.save(out_dir / "reconstructed_jpeg.png")
        jpeg_psnr = psnr(np.array(image), np.array(jpeg_image))
        decoded_ok = True
    except Exception:
        # Corrupted JPEG may be syntactically invalid. Save no misleading image.
        pass
    records.append({
        "encoding": "jpeg_quality_70", "payload_bytes": len(jpeg_payload),
        "ber": jpeg_ber, "psnr_db": jpeg_psnr, "decoded": decoded_ok
    })

    with (out_dir / "image_results.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["encoding", "payload_bytes", "ber", "psnr_db", "decoded"])
        writer.writeheader()
        writer.writerows(records)

    print("\nIMAGE TRANSMISSION")
    print(f"Dimensions: {gray.width} x {gray.height}")
    print(f"Eb/N0={ebn0_db} dB, amplitude attenuation={attenuation}")
    for row in records:
        print(row)
    print("Image outputs:", out_dir)
    return records
