# test_final_state.py

import os
import sys
import subprocess
import pytest
import pandas as pd
import numpy as np

def test_result_csv_exists():
    """Verify that the result CSV file was created."""
    assert os.path.exists("/home/user/result.csv"), "The output file /home/user/result.csv does not exist."
    assert os.path.isfile("/home/user/result.csv"), "/home/user/result.csv is not a file."

def test_result_csv_format_and_mse():
    """Verify the format of the result CSV and compute the MSE against the reference truth."""
    # 1. Generate reference data
    cmd = [
        "ffmpeg", "-i", "/app/sensor_video.mp4",
        "-vf", "format=gray,scale=1:1",
        "-f", "image2pipe",
        "-vcodec", "rawvideo",
        "-pix_fmt", "gray",
        "-"
    ]
    try:
        process = subprocess.run(cmd, capture_output=True, check=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to extract frames from video using ffmpeg: {e.stderr.decode()}")

    raw_bytes = process.stdout
    brightness = [float(b) for b in raw_bytes]

    assert len(brightness) > 0, "Error: No frames extracted from video."

    # 2. Resample (mean of every 3 frames)
    resampled = []
    for i in range(0, len(brightness) - len(brightness) % 3, 3):
        resampled.append(np.mean(brightness[i:i+3]))

    # 3. SMA window 4
    sma = []
    for i in range(len(resampled) - 3):
        sma.append(np.mean(resampled[i:i+4]))

    # 4. Min-Max Normalization
    sma = np.array(sma)
    sma_min = sma.min()
    sma_max = sma.max()
    normalized = (sma - sma_min) / (sma_max - sma_min)

    reference_df = pd.DataFrame({
        'idx': range(len(normalized)),
        'value': normalized
    })

    # Load agent's result
    try:
        agent_df = pd.read_csv('/home/user/result.csv')
    except Exception as e:
        pytest.fail(f"Could not read /home/user/result.csv as a CSV file: {e}")

    # Check columns
    assert list(agent_df.columns) == ['idx', 'value'], f"Expected columns ['idx', 'value'], but got {list(agent_df.columns)}"

    min_len = min(len(reference_df), len(agent_df))
    assert min_len > 0, "Agent CSV contains no data rows."

    # Check if the length is roughly correct (at least min_len)
    assert len(agent_df) == len(reference_df), f"Expected {len(reference_df)} rows, but got {len(agent_df)} rows."

    ref_vals = reference_df['value'].values[:min_len]
    agent_vals = agent_df['value'].values[:min_len]

    # Calculate MSE
    mse = np.mean((ref_vals - agent_vals) ** 2)

    # Assert threshold
    assert mse <= 0.001, f"Failure: MSE {mse:.6f} exceeds threshold of 0.001."