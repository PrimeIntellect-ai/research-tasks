# test_final_state.py

import os
import csv
import pytest

def test_rust_project_exists():
    """Test that the Rust project was created in the correct directory."""
    cargo_toml_path = "/home/user/math_prep/Cargo.toml"
    assert os.path.isfile(cargo_toml_path), "Rust project 'math_prep' not found at /home/user/math_prep. Cargo.toml is missing."

def test_experiment_log_exists():
    """Test that the experiment_log.csv file was generated."""
    csv_path = "/home/user/experiment_log.csv"
    assert os.path.isfile(csv_path), "experiment_log.csv not found at /home/user/experiment_log.csv."

def test_experiment_log_content():
    """Test the structure and values in experiment_log.csv."""
    csv_path = "/home/user/experiment_log.csv"

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == 2, f"Expected exactly 2 rows (header + 1 data row) in CSV, found {len(rows)}."

    header = rows[0]
    expected_header = ["num_samples", "mse", "duration_ms"]
    assert header == expected_header, f"Incorrect CSV header. Expected {expected_header}, got {header}."

    data = rows[1]
    assert len(data) == 3, f"Expected 3 columns in data row, got {len(data)}."

    num_samples, mse_str, duration_str = data

    # Check num_samples
    assert num_samples == "10000", f"Expected num_samples to be '10000', got '{num_samples}'."

    # Check MSE
    try:
        mse = float(mse_str)
    except ValueError:
        pytest.fail(f"MSE value '{mse_str}' is not a valid float.")

    assert 0.0 < mse < 100.0, f"MSE value {mse} is out of expected bounds (0.0 < mse < 100.0)."

    # Check duration
    try:
        duration = int(duration_str)
    except ValueError:
        pytest.fail(f"Duration value '{duration_str}' is not a valid integer.")

    assert duration >= 0, f"Duration {duration} must be a non-negative integer."