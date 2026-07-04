# test_final_state.py

import os
import numpy as np
import scipy.io.wavfile as wav
import pandas as pd
import pytest

def test_output_energies_csv():
    output_path = "/home/user/output_energies.csv"
    audio_path = "/app/audio_data.wav"

    assert os.path.exists(output_path), f"Output file {output_path} does not exist."
    assert os.path.exists(audio_path), f"Audio file {audio_path} does not exist."

    # Read the generated CSV
    try:
        df = pd.read_csv(output_path, header=None)
        pred = df.values.flatten()
    except Exception as e:
        pytest.fail(f"Failed to read {output_path}: {e}")

    # Calculate ground truth
    try:
        sr, data = wav.read(audio_path)
    except Exception as e:
        pytest.fail(f"Failed to read {audio_path}: {e}")

    window_size = 4096
    num_windows = len(data) // window_size
    ref = np.zeros(num_windows)
    for i in range(num_windows):
        window = data[i*window_size : (i+1)*window_size].astype(np.float64)
        ref[i] = np.sum(window * window)

    assert len(pred) == len(ref), f"Expected {len(ref)} windows, but got {len(pred)}."

    mse = np.mean((pred - ref)**2)
    threshold = 0.001

    assert mse <= threshold, f"MSE is {mse}, which is greater than the threshold {threshold}. The C extension logic is likely incorrect (e.g., integer overflow)."