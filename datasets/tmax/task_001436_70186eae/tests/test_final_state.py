# test_final_state.py

import os
import stat
import pandas as pd
import pytest

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist"
    assert os.path.isfile(script_path), f"{script_path} is not a file"
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable"

def test_features_csv_schema():
    features_path = "/home/user/features.csv"
    assert os.path.exists(features_path), f"Features CSV missing at {features_path}"

    try:
        df = pd.read_csv(features_path)
    except Exception as e:
        pytest.fail(f"Failed to read {features_path} as CSV: {e}")

    expected_columns = ["frame_index", "luma_avg", "delta_luma"]
    assert list(df.columns) == expected_columns, f"CSV columns do not match expected schema. Got {list(df.columns)}, expected {expected_columns}"

def test_bootstrap_result_metric():
    features_path = "/home/user/features.csv"
    result_path = "/home/user/bootstrap_result.txt"

    assert os.path.exists(features_path), f"Features CSV missing at {features_path}"
    assert os.path.exists(result_path), f"Bootstrap result missing at {result_path}"

    try:
        df = pd.read_csv(features_path)
    except Exception as e:
        pytest.fail(f"Failed to read {features_path} as CSV: {e}")

    # Check if expected columns are present to compute the metric
    if 'luma_avg' not in df.columns or 'delta_luma' not in df.columns:
        pytest.fail("CSV is missing 'luma_avg' or 'delta_luma' columns required for evaluation.")

    valid_df = df[df['luma_avg'] >= 50.0]

    assert not valid_df.empty, "No valid frames found with luma_avg >= 50.0. Check feature extraction logic."

    expected_mean = valid_df['delta_luma'].mean()

    with open(result_path, 'r') as f:
        content = f.read().strip()

    try:
        agent_val = float(content)
    except ValueError:
        pytest.fail(f"Could not parse bootstrap result as float. Got: '{content}'")

    error = abs(agent_val - expected_mean)
    threshold = 0.5

    assert error <= threshold, (
        f"Bootstrap result metric threshold exceeded.\n"
        f"Expected (true sample mean of filtered data): {expected_mean:.4f}\n"
        f"Agent bootstrap grand mean: {agent_val:.4f}\n"
        f"Absolute error: {error:.4f} > Threshold: {threshold}"
    )