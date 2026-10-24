from pathlib import Path
import io
import numpy as np
from PIL import Image


def create_demo_image(path: Path, width: int = 256, height: int = 192) -> Path:
    """Create a deterministic, synthetic security-camera test image."""
    y, x = np.mgrid[0:height, 0:width]
    img = np.full((height, width, 3), 32, dtype=np.uint8)
    img[y > int(height * 0.58)] = [65, 72, 66]
    building = ((x > width * 0.08) & (x < width * 0.43) &
                (y > height * 0.16) & (y < height * 0.58))
    img[building] = [115, 122, 126]
    for wx in (40, 70, 100):
        img[48:70, wx:wx + 14] = [190, 194, 170]
        img[82:104, wx:wx + 14] = [190, 194, 170]
    img[int(height * 0.78):int(height * 0.80), :] = [190, 190, 180]
    cy, cx = int(height * 0.70), int(width * 0.67)
    img[cy:cy + 22, cx - 28:cx + 28] = [35, 45, 58]
    img[cy - 9:cy + 3, cx - 16:cx + 18] = [45, 55, 68]
    img[cy + 17:cy + 25, cx - 20:cx - 8] = [15, 15, 15]
    img[cy + 17:cy + 25, cx + 10:cx + 22] = [15, 15, 15]
    rng = np.random.default_rng(12)
    img = np.clip(img.astype(float) + rng.normal(0, 3, img.shape), 0, 255).astype(np.uint8)
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(img, "RGB").save(path)
    return path


def load_image(path: Path) -> Image.Image:
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")
    with Image.open(path) as im:
        return im.convert("RGB")


def image_to_bytes(image: Image.Image, mode: str) -> tuple[bytes, dict]:
    """Encode image as raw grayscale bytes or JPEG bytes; return payload and metadata."""
    if mode == "grayscale":
        gray = image.convert("L")
        meta = {"mode": mode, "width": gray.width, "height": gray.height,
                "format": "RAW_GRAY", "quality": None}
        return gray.tobytes(), meta
    if mode == "jpeg":
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=70)
        meta = {"mode": mode, "width": image.width, "height": image.height,
                "format": "JPEG", "quality": 70}
        return buffer.getvalue(), meta
    raise ValueError("mode must be 'grayscale' or 'jpeg'")


def bytes_to_grayscale(payload: bytes, width: int, height: int) -> Image.Image:
    expected = width * height
    raw = payload[:expected].ljust(expected, b"\x00")
    return Image.frombytes("L", (width, height), raw)


def decode_jpeg(payload: bytes) -> Image.Image:
    with Image.open(io.BytesIO(payload)) as im:
        return im.convert("RGB")
