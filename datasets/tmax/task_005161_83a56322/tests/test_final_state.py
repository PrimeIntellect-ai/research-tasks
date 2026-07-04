# test_final_state.py
import os
import numpy as np
from scipy.io import wavfile
import pytest

def decode_lsb(audio_data, max_len=50):
    bits = audio_data & 1
    chars = []
    for i in range(max_len):
        byte_bits = bits[i*8:(i+1)*8]
        if len(byte_bits) < 8:
            break
        val = sum([bit << j for j, bit in enumerate(byte_bits)])
        if val == 0:
            break
        chars.append(chr(val))
    return "".join(chars)

def test_payload_exists():
    path = "/home/user/payload.wav"
    assert os.path.isfile(path), f"Missing required file: {path}. The stego payload audio file was not generated."

def test_stego_payload():
    orig_path = "/app/carrier.wav"
    stego_path = "/home/user/payload.wav"

    assert os.path.isfile(orig_path), "Original carrier file is missing."
    assert os.path.isfile(stego_path), "Stego payload file is missing."

    try:
        sr1, orig = wavfile.read(orig_path)
    except Exception as e:
        pytest.fail(f"Failed to read original carrier file: {e}")

    try:
        sr2, stego = wavfile.read(stego_path)
    except Exception as e:
        pytest.fail(f"Failed to read stego payload file: {e}")

    assert len(orig) == len(stego), "The length of the stego payload does not match the original carrier file."

    expected_token = "AUTH_TOKEN_9942_EXFIL"
    token = decode_lsb(stego, max_len=len(expected_token) + 5)

    assert token == expected_token, f"Decoded token '{token}' does not match the expected '{expected_token}'."

    orig_float = orig.astype(np.float64)
    stego_float = stego.astype(np.float64)
    mse = np.mean((orig_float - stego_float) ** 2)

    if mse == 0:
        psnr = 100.0
    else:
        max_pixel = 32767.0
        psnr = 10 * np.log10((max_pixel ** 2) / mse)

    threshold = 85.0
    assert psnr >= threshold, f"PSNR of {psnr:.2f} dB is below the required threshold of {threshold:.2f} dB."