# Group 4 — Digital Image Transmission System using QPSK and AWGN

**Scenario:** Wireless Security Camera → Control Room

## Requirements
- Python 3.10+
- NumPy, SciPy, Matplotlib, Pillow

## Ubuntu setup
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

## Windows PowerShell setup
```powershell
py -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

## Run with a custom camera image
```bash
python main.py --image data/security_camera.jpg --ebn0 8 --attenuation 0.8
```

## Compare channel conditions
```bash
python main.py --ebn0 0 --attenuation 0.8
python main.py --ebn0 4 --attenuation 0.8
python main.py --ebn0 10 --attenuation 0.8
```

## Output files
`results/` contains BER plot/CSV, constellation diagrams, I/Q plot, FFT spectrum,
original/reconstructed grayscale images, JPEG baseline, optional reconstructed JPEG,
and image-results CSV.

## Model assumptions and limitations
- Uncoded coherent QPSK with ideal carrier and timing synchronization.
- Each QPSK symbol has unit energy; Eb = Es/2.
- Channel model: y = a*x + n. Noise power is referenced to the pre-attenuation signal,
  so attenuation lowers the effective receive SNR.
- The BER test uses random bits and is separate from the image payload experiment.
- JPEG is lossy before transmission. Channel bit errors can corrupt its syntax and
  prevent decoding; this is an important result, not a program failure.
- This is a baseband model, not a full RF simulation. It does not yet model carrier
  upconversion, pulse shaping, multipath fading, packet retransmission, or error-control coding.
