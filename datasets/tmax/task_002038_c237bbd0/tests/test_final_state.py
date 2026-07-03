# test_final_state.py
import os
import csv
import pytest
import numpy as np
from scipy.io import wavfile

def test_experiments_csv_exists_and_valid():
    csv_path = "/app/experiments.csv"
    assert os.path.isfile(csv_path), f"{csv_path} is missing."

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    # Assuming at least a header and 5 data rows
    assert len(rows) >= 6, f"{csv_path} must contain at least 5 different parameter combinations tested (plus header)."

def test_run_pipeline_sh_exists_and_executable():
    script_path = "/app/run_pipeline.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_test_cleaned_wav_exists():
    out_path = "/app/data/test_cleaned.wav"
    assert os.path.isfile(out_path), f"The output file {out_path} is missing."

def get_audio_data(filepath):
    rate, data = wavfile.read(filepath)
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32768.0
    return rate, data

def test_audio_mse_metric():
    truth_path = "/truth/test_clean.wav"
    pred_path = "/app/data/test_cleaned.wav"

    assert os.path.isfile(truth_path), f"Ground truth {truth_path} is missing."
    assert os.path.isfile(pred_path), f"Prediction {pred_path} is missing."

    r1, clean = get_audio_data(truth_path)
    r2, cleaned = get_audio_data(pred_path)

    assert r1 == r2, f"Sampling rates do not match: truth={r1}, pred={r2}"

    min_len = min(len(clean), len(cleaned))
    clean_trimmed = clean[:min_len]
    cleaned_trimmed = cleaned[:min_len]

    mse = np.mean((clean_trimmed - cleaned_trimmed) ** 2)
    threshold = 0.005

    assert mse <= threshold, f"MSE {mse:.6f} exceeds the threshold of {threshold}."