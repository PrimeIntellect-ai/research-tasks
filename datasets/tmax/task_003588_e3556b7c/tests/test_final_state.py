# test_final_state.py
import os
import pandas as pd
import numpy as np
import pytest

def test_peak_confidence_results():
    csv_path = "/home/user/peak_confidence.csv"
    assert os.path.exists(csv_path), f"Expected output file not found at {csv_path}"

    # Read the CSV
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        pytest.fail(f"Failed to read {csv_path} as a CSV file: {e}")

    # Check headers
    expected_columns = ['peak_id', 'center_mean', 'ci_lower', 'ci_upper']
    assert list(df.columns) == expected_columns, (
        f"CSV headers do not match the expected format.\n"
        f"Expected: {expected_columns}\n"
        f"Found: {list(df.columns)}"
    )

    # Check peak_id values
    df = df.sort_values('peak_id')
    assert list(df['peak_id'].values) == [1, 2, 3], "peak_id column must contain exactly [1, 2, 3]."

    # Compute MAE
    true_centers = np.array([450.0, 520.5, 600.2])
    estimated_centers = df['center_mean'].values
    mae = np.mean(np.abs(estimated_centers - true_centers))

    threshold = 0.05
    assert mae < threshold, (
        f"MAE of estimated peak centers is too high.\n"
        f"Measured MAE: {mae:.4f}\n"
        f"Threshold: < {threshold}\n"
        f"Estimated centers: {estimated_centers}\n"
        f"True centers: {true_centers}"
    )