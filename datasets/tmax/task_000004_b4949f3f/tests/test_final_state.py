# test_final_state.py

import os
import numpy as np
from scipy.io import wavfile
import pandas as pd
import pytest

def compute_mse(original_path, reconstructed_path):
    sr1, y1 = wavfile.read(original_path)
    sr2, y2 = wavfile.read(reconstructed_path)

    if sr1 != sr2:
        return float('inf')

    y1 = y1.astype(np.float64)
    y2 = y2.astype(np.float64)

    # Normalize
    if np.max(np.abs(y1)) > 0:
        y1 = y1 / np.max(np.abs(y1))
    if np.max(np.abs(y2)) > 0:
        y2 = y2 / np.max(np.abs(y2))

    min_len = min(len(y1), len(y2))
    y1 = y1[:min_len]
    y2 = y2[:min_len]

    mse = np.mean((y1 - y2) ** 2)
    return mse

def test_posteriors_plot_exists():
    path = "/home/user/posteriors.png"
    assert os.path.exists(path), f"Expected plot file not found at {path}"
    assert os.path.getsize(path) > 0, f"Plot file at {path} is empty"

def test_parameters_csv():
    path = "/home/user/parameters.csv"
    assert os.path.exists(path), f"Expected parameter log not found at {path}"

    df = pd.read_csv(path)
    expected_columns = {"component", "amplitude", "decay", "frequency", "phase"}
    assert expected_columns.issubset(set(df.columns)), f"CSV at {path} is missing required columns. Found: {df.columns}"
    assert len(df) == 3, f"Expected 3 components in the CSV, found {len(df)}"

def test_reconstructed_audio_mse():
    original_path = "/app/chime_recording.wav"
    reconstructed_path = "/home/user/reconstructed.wav"

    assert os.path.exists(reconstructed_path), f"Expected reconstructed audio not found at {reconstructed_path}"

    mse = compute_mse(original_path, reconstructed_path)

    assert mse <= 0.02, f"Reconstruction failed: MSE={mse:.5f} > 0.02"