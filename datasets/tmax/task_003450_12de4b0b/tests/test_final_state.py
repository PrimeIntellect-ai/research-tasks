# test_final_state.py

import os
import numpy as np
from scipy.io import wavfile

def calculate_mse(file1, file2):
    rate1, data1 = wavfile.read(file1)
    rate2, data2 = wavfile.read(file2)

    if rate1 != rate2:
        return float('inf')

    # Ensure same length for comparison
    min_len = min(len(data1), len(data2))
    d1 = data1[:min_len].astype(np.float64)
    d2 = data2[:min_len].astype(np.float64)

    # Normalize
    d1 = d1 / np.max(np.abs(d1)) if np.max(np.abs(d1)) > 0 else d1
    d2 = d2 / np.max(np.abs(d2)) if np.max(np.abs(d2)) > 0 else d2

    mse = np.mean((d1 - d2) ** 2)
    return mse

def test_reconstructed_audio_mse():
    output_path = '/home/user/output_reconstructed.wav'
    reference_path = '/app/reference_clean.wav'

    assert os.path.exists(output_path), f"Output file {output_path} does not exist. Did you run the service to generate the reconstructed audio?"
    assert os.path.exists(reference_path), f"Reference file {reference_path} is missing."

    try:
        mse = calculate_mse(output_path, reference_path)
    except Exception as e:
        assert False, f"Failed to compute MSE. Ensure {output_path} is a valid WAV file. Error: {e}"

    threshold = 0.01
    assert mse < threshold, f"Reconstructed audio MSE is {mse:.6f}, which is not less than the threshold {threshold}."