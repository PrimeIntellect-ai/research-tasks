# test_final_state.py

import os
import json
import csv
import math
import pytest

def test_artifacts_exist():
    """Check that the expected artifact files are generated."""
    assert os.path.exists('/home/user/artifacts/cleaned_data.csv'), "The file /home/user/artifacts/cleaned_data.csv is missing."
    assert os.path.exists('/home/user/artifacts/metrics.json'), "The file /home/user/artifacts/metrics.json is missing."

def test_cleaned_data_logic():
    """Validate that the cleaned data matches the expected logical filtering."""
    raw_file = '/home/user/raw_experiment.csv'
    assert os.path.exists(raw_file), f"{raw_file} is missing."

    with open(raw_file, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        raw_data = list(reader)

    # Step A: Remove rows with missing values
    data_no_missing = [row for row in raw_data if all(val.strip() != '' for val in row)]

    # Step B: Remove outliers based on Y column Z-score
    y_vals = [float(row[3]) for row in data_no_missing]
    mu = sum(y_vals) / len(y_vals)
    std = math.sqrt(sum((y - mu)**2 for y in y_vals) / len(y_vals))

    expected_cleaned_data = []
    for row in data_no_missing:
        y = float(row[3])
        if abs(y - mu) / std <= 2.0:
            expected_cleaned_data.append(row)

    # Check generated cleaned_data.csv
    with open('/home/user/artifacts/cleaned_data.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        out_header = next(reader)
        out_data = list(reader)

    assert len(out_data) == len(expected_cleaned_data), f"Expected {len(expected_cleaned_data)} cleaned rows, but found {len(out_data)} in cleaned_data.csv."

def test_metrics_json_values():
    """Validate the contents of metrics.json against expected values."""
    json_path = '/home/user/artifacts/metrics.json'
    with open(json_path, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Could not parse {json_path} as valid JSON.")

    assert 'cleaned_row_count' in metrics, "Missing 'cleaned_row_count' in metrics.json."
    assert metrics['cleaned_row_count'] == 94, f"Expected cleaned_row_count to be 94, got {metrics['cleaned_row_count']}."

    # Check estimates with a tolerance of 0.005
    tolerance = 0.005

    assert 'beta1_estimate' in metrics, "Missing 'beta1_estimate' in metrics.json."
    beta1 = metrics['beta1_estimate']
    assert abs(beta1 - 5.4850) <= tolerance, f"beta1_estimate {beta1} is outside the acceptable tolerance of 5.4850."

    assert 'beta1_ci_lower' in metrics, "Missing 'beta1_ci_lower' in metrics.json."
    lower = metrics['beta1_ci_lower']
    assert abs(lower - 5.3780) <= tolerance, f"beta1_ci_lower {lower} is outside the acceptable tolerance of 5.3780."

    assert 'beta1_ci_upper' in metrics, "Missing 'beta1_ci_upper' in metrics.json."
    upper = metrics['beta1_ci_upper']
    assert abs(upper - 5.6020) <= tolerance, f"beta1_ci_upper {upper} is outside the acceptable tolerance of 5.6020."