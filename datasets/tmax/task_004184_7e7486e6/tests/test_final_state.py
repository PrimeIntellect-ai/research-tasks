# test_final_state.py

import os
import numpy as np
from scipy.io import wavfile

def test_fixed_output_mse():
    output_path = "/home/user/fixed_output.wav"
    reference_path = "/app/clean_reference.wav"

    assert os.path.exists(output_path), f"Output file not found: {output_path}"
    assert os.path.exists(reference_path), f"Reference file not found: {reference_path}"

    rate_out, data_out = wavfile.read(output_path)
    rate_ref, data_ref = wavfile.read(reference_path)

    assert rate_out == rate_ref, f"Sample rate mismatch: {rate_out} vs {rate_ref}"
    assert len(data_out) == len(data_ref), f"Length mismatch: {len(data_out)} vs {len(data_ref)}"

    # Normalize to [-1.0, 1.0] assuming 16-bit PCM WAV
    data_out_norm = data_out.astype(np.float32) / 32768.0
    data_ref_norm = data_ref.astype(np.float32) / 32768.0

    mse = np.mean((data_out_norm - data_ref_norm) ** 2)
    threshold = 0.005

    assert mse < threshold, f"MSE is {mse:.6f}, which is >= threshold {threshold}. The audio filter is still not converging correctly."