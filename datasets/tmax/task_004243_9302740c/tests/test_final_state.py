# test_final_state.py

import os
import time
import json
import subprocess
import pytest
import numpy as np
import pandas as pd
from scipy import stats

def test_selected_features_exists():
    assert os.path.isfile("/home/user/selected_features.txt"), "/home/user/selected_features.txt is missing."

def test_experiment_log_exists():
    assert os.path.isfile("/home/user/experiment_log.json"), "/home/user/experiment_log.json is missing."
    with open("/home/user/experiment_log.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/home/user/experiment_log.json is not valid JSON.")

def test_predict_script_exists_and_executable():
    script_path = "/home/user/predict.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_pipeline_performance_and_accuracy():
    script_path = "/home/user/predict.sh"
    test_raw_path = "/app/data/test_raw.csv"
    test_preds_path = "/app/data/test_preds.csv"
    oracle_path = "/app/bin/legacy_oracle"

    assert os.path.isfile(test_raw_path), f"{test_raw_path} is missing. Setup issue."

    # Measure predict.sh time
    start_time = time.time()
    result = subprocess.run([script_path, test_raw_path, test_preds_path], capture_output=True, text=True)
    predict_time = time.time() - start_time

    assert result.returncode == 0, f"predict.sh failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"
    assert os.path.isfile(test_preds_path), f"predict.sh did not create {test_preds_path}."

    # Process test_raw.csv to get cleaned data and true targets
    df_raw = pd.read_csv(test_raw_path)

    # 1. Drop NaNs
    df_clean = df_raw.dropna()

    # 2. Drop outliers (z-score > 3.0)
    z_scores = np.abs(stats.zscore(df_clean))
    # stats.zscore might return nan if variance is 0, but assuming standard data
    df_clean = df_clean[(z_scores <= 3.0).all(axis=1)]

    # True oracle logic: target = sin(f0) + 0.5 * f2 + log(abs(f5) + 1.0)
    true_targets = np.sin(df_clean['f0']) + 0.5 * df_clean['f2'] + np.log(np.abs(df_clean['f5']) + 1.0)

    # Read agent predictions
    df_preds = pd.read_csv(test_preds_path)
    assert 'target' in df_preds.columns, f"{test_preds_path} must contain a 'target' column."

    # The agent's predict.sh should apply the exact same ETL, so the number of rows should match
    assert len(df_preds) == len(true_targets), f"Expected {len(true_targets)} predictions after ETL, got {len(df_preds)}."

    mse = np.mean((df_preds['target'].values - true_targets.values) ** 2)

    # Measure oracle time on the test set for speedup comparison
    # We can use theoretical time to avoid waiting too long during testing:
    # The oracle processes input row by row, with 5ms sleep per row.
    # It might process the raw or cleaned data depending on how it's called, but theoretical time per row is ~0.005s.
    # Let's measure actual oracle time on a small subset or just use theoretical time of 0.005 * len(df_raw).
    # The prompt says "measured by comparing the wall-clock time ... against the theoretical or measured time".
    theoretical_oracle_time = len(df_raw) * 0.005

    speedup = theoretical_oracle_time / predict_time if predict_time > 0 else float('inf')

    assert mse <= 0.05, f"MSE is {mse:.4f}, which is > 0.05 threshold."
    assert speedup >= 50.0, f"Speedup is {speedup:.2f}x, which is < 50.0x threshold. (Predict time: {predict_time:.4f}s, Oracle theoretical: {theoretical_oracle_time:.4f}s)"