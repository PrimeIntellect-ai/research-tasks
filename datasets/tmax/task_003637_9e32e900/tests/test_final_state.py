# test_final_state.py
import os
import pytest
import numpy as np
from scipy.io import wavfile

def test_clean_audio_exists_and_mse():
    ref_path = '/app/reference_clean.wav'
    test_path = '/home/user/clean_audio.wav'

    assert os.path.exists(test_path), f"Expected output file not found at {test_path}"
    assert os.path.exists(ref_path), f"Reference file not found at {ref_path}"

    try:
        sr1, data1 = wavfile.read(ref_path)
    except Exception as e:
        pytest.fail(f"Failed to read reference file: {e}")

    try:
        sr2, data2 = wavfile.read(test_path)
    except Exception as e:
        pytest.fail(f"Failed to read test file: {e}")

    assert sr1 == sr2, f"Sample rate mismatch: expected {sr1}, got {sr2}"
    assert len(data1) == len(data2), f"Length mismatch: expected {len(data1)} samples, got {len(data2)} samples"

    mse = np.mean((data1.astype(float) - data2.astype(float))**2)
    assert mse < 0.1, f"MSE too high: {mse} >= 0.1. The audio was not correctly redacted."