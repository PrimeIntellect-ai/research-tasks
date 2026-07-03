# test_final_state.py

import os
import numpy as np
import scipy.io.wavfile as wav
import pytest

def calculate_mse(file1, file2):
    sr1, data1 = wav.read(file1)
    sr2, data2 = wav.read(file2)

    # Ensure same length
    min_len = min(len(data1), len(data2))
    if min_len == 0:
        return float('inf')

    data1 = data1[:min_len].astype(np.float32)
    data2 = data2[:min_len].astype(np.float32)

    # Normalize to avoid scale differences
    max1 = np.max(np.abs(data1))
    max2 = np.max(np.abs(data2))

    if max1 > 0:
        data1 /= max1
    if max2 > 0:
        data2 /= max2

    mse = np.mean((data1 - data2)**2)
    return mse

def test_output_audio_exists_and_meets_mse_threshold():
    output_path = "/app/output.wav"
    reference_path = "/tmp/clean_reference.wav"

    assert os.path.isfile(output_path), f"Output audio file {output_path} does not exist. Did the server process the audio successfully?"
    assert os.path.isfile(reference_path), f"Reference audio file {reference_path} does not exist (environment issue)."

    mse = calculate_mse(output_path, reference_path)

    threshold = 0.02
    assert mse <= threshold, f"MSE {mse:.5f} exceeds threshold {threshold}. The moving average filter was either not applied correctly or the window size was wrong."

def test_c_project_compiles_cleanly():
    # Verify that the binary was built
    binary_path = "/app/audio_math_server/dsp_server"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} not found. The C project build might have failed."
    assert os.access(binary_path, os.X_OK), f"The file {binary_path} is not executable."