# test_final_state.py
import os
import subprocess
import pandas as pd
import numpy as np
import pytest

def test_processed_signal_csv_exists():
    csv_path = "/home/user/processed_signal.csv"
    assert os.path.exists(csv_path), f"Expected output file {csv_path} does not exist."
    assert os.path.isfile(csv_path), f"{csv_path} is not a file."

def test_processed_signal_accuracy():
    csv_path = "/home/user/processed_signal.csv"
    assert os.path.exists(csv_path), f"Expected output file {csv_path} does not exist."

    try:
        agent_df = pd.read_csv(csv_path)
    except Exception as e:
        pytest.fail(f"Failed to read {csv_path} as CSV: {e}")

    assert 'rolling_sma' in agent_df.columns, "CSV is missing the 'rolling_sma' column."

    cmd = "ffmpeg -i /app/data_feed.mp4 -vf 'fps=10,format=gray,signalstats' -f null - 2>&1 | grep 'Parsed_signalstats' | awk '{print $5}' | cut -d= -f2"
    try:
        output = subprocess.check_output(cmd, shell=True, text=True).strip().split('\n')
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run ffmpeg to generate ground truth: {e}")

    raw_intensities = [float(x) for x in output if x]

    kept_indices = []
    kept_intensities = []

    for i, val in enumerate(raw_intensities):
        if i == 0:
            kept_indices.append(i)
            kept_intensities.append(val)
        else:
            if abs(val - kept_intensities[-1]) > 1.0:
                kept_indices.append(i)
                kept_intensities.append(val)

    normalized = [x / 255.0 for x in kept_intensities]
    rolling_sma = []
    for i in range(len(normalized)):
        start = max(0, i - 4)
        window = normalized[start:i+1]
        rolling_sma.append(sum(window) / len(window))

    assert len(agent_df) == len(rolling_sma), f"Length mismatch: Expected {len(rolling_sma)} rows, got {len(agent_df)} rows."

    agent_sma = agent_df['rolling_sma'].values
    mse = np.mean((np.array(rolling_sma) - agent_sma)**2)

    threshold = 0.0001
    assert mse <= threshold, f"MSE of rolling_sma is {mse}, which exceeds the threshold of {threshold}."