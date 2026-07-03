# test_final_state.py

import os
import pytest

def test_preprocess_script_exists_and_executable():
    """Test that preprocess.sh exists and is executable."""
    script_path = "/home/user/preprocess.sh"
    assert os.path.isfile(script_path), f"Script not found: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_centered_data_correctness():
    """Test that centered_data.csv is correctly mean-centered and formatted to 2 decimal places."""
    dataset_path = "/home/user/dataset.csv"
    centered_path = "/home/user/centered_data.csv"

    assert os.path.isfile(dataset_path), f"Original dataset missing: {dataset_path}"
    assert os.path.isfile(centered_path), f"Centered data missing: {centered_path}"

    # Read original data to compute truth
    with open(dataset_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    data = [[float(x) for x in line.split(",")] for line in lines]
    n = len(data)

    # Compute means
    means = [sum(col) / n for col in zip(*data)]

    # Compute expected centered data
    expected_centered = []
    for row in data:
        expected_centered.append(",".join(f"{val - mean:.2f}" for val, mean in zip(row, means)))

    # Read actual centered data
    with open(centered_path, "r") as f:
        actual_centered = [line.strip() for line in f if line.strip()]

    assert actual_centered == expected_centered, "The contents of centered_data.csv do not match the expected mean-centered values."

def test_metrics_log_correctness():
    """Test that metrics.log contains the correct mean values formatted to 2 decimal places."""
    dataset_path = "/home/user/dataset.csv"
    log_path = "/home/user/metrics.log"

    assert os.path.isfile(dataset_path), f"Original dataset missing: {dataset_path}"
    assert os.path.isfile(log_path), f"Metrics log missing: {log_path}"

    # Read original data to compute truth
    with open(dataset_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    data = [[float(x) for x in line.split(",")] for line in lines]
    n = len(data)

    # Compute means
    means = [sum(col) / n for col in zip(*data)]

    expected_log_entry = f"Col1_mean={means[0]:.2f}, Col2_mean={means[1]:.2f}, Col3_mean={means[2]:.2f}"

    # Read log file
    with open(log_path, "r") as f:
        log_content = f.read()

    assert expected_log_entry in log_content, f"Expected log entry '{expected_log_entry}' not found in {log_path}."