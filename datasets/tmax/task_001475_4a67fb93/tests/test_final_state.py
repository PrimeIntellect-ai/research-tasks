# test_final_state.py

import os
import json
import numpy as np
import pandas as pd
import imageio.v3 as iio
import pytest

def test_processed_frames_parquet():
    """Verify that the Parquet file exists and has the correct structure."""
    parquet_path = "/app/processed_frames.parquet"
    assert os.path.exists(parquet_path), f"Missing Parquet file at {parquet_path}"

    try:
        df = pd.read_parquet(parquet_path)
    except Exception as e:
        pytest.fail(f"Failed to read Parquet file: {e}")

    assert "intensity" in df.columns, "Parquet file must contain an 'intensity' column"
    assert len(df.columns) == 1, "Parquet file should only contain the 'intensity' column"
    assert len(df) > 0, "Parquet file is empty"

def test_metrics_json_and_accuracy():
    """Verify the metrics.json file and check its accuracy against the true values."""
    json_path = "/app/metrics.json"
    video_path = "/app/factory_feed.mp4"

    assert os.path.exists(json_path), f"Missing JSON file at {json_path}"

    with open(json_path, 'r') as f:
        try:
            agent_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("metrics.json is not a valid JSON file")

    for key in ["mean", "ci_lower", "ci_upper"]:
        assert key in agent_data, f"Missing key '{key}' in metrics.json"

    # Read video and compute true intensities
    # Using imageio since cv2 might not be available in the test environment
    # cv2.COLOR_BGR2GRAY weights: Y = 0.299 R + 0.587 G + 0.114 B
    try:
        frames = iio.imread(video_path, plugin="pyav")
    except Exception:
        # Fallback if pyav is not available
        import imageio
        reader = imageio.get_reader(video_path)
        frames = [im for im in reader]

    intensities = []
    for frame in frames:
        # frame is RGB
        R = frame[:, :, 0]
        G = frame[:, :, 1]
        B = frame[:, :, 2]
        gray = 0.299 * R + 0.587 * G + 0.114 * B
        # cv2 rounds and converts to uint8, but np.mean on float is close enough
        # Actually cv2.cvtColor returns uint8
        gray_uint8 = np.round(gray).astype(np.uint8)
        intensities.append(np.mean(gray_uint8))

    intensities = np.array(intensities)

    # Compute true values
    true_mean = np.mean(intensities)

    np.random.seed(42)
    n_bootstraps = 10000
    bootstrap_means = np.zeros(n_bootstraps)
    for i in range(n_bootstraps):
        sample = np.random.choice(intensities, size=len(intensities), replace=True)
        bootstrap_means[i] = np.mean(sample)

    true_ci_lower = np.percentile(bootstrap_means, 2.5)
    true_ci_upper = np.percentile(bootstrap_means, 97.5)

    agent_mean = float(agent_data['mean'])
    agent_lower = float(agent_data['ci_lower'])
    agent_upper = float(agent_data['ci_upper'])

    error = max(
        abs(true_mean - agent_mean),
        abs(true_ci_lower - agent_lower),
        abs(true_ci_upper - agent_upper)
    )

    threshold = 0.1
    assert error <= threshold, (
        f"Maximum Absolute Error {error:.4f} exceeds threshold {threshold}. "
        f"True values: mean={true_mean:.4f}, ci_lower={true_ci_lower:.4f}, ci_upper={true_ci_upper:.4f}. "
        f"Agent values: mean={agent_mean:.4f}, ci_lower={agent_lower:.4f}, ci_upper={agent_upper:.4f}."
    )