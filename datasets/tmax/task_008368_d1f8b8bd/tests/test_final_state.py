# test_final_state.py

import os
import json
import math
import pytest

def test_executable_exists():
    executable_path = "/home/user/etl_clean"
    assert os.path.exists(executable_path), f"Executable {executable_path} is missing."
    assert os.path.isfile(executable_path), f"{executable_path} is not a file."
    assert os.access(executable_path, os.X_OK), f"{executable_path} is not executable."

def test_clean_data_csv():
    file_path = "/home/user/clean_data.csv"
    assert os.path.exists(file_path), f"File {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    expected_content = """id,measurement
1,10.5
3,12.2
5,15.8
7,20.0
9,22.5"""

    with open(file_path, "r") as f:
        actual_content = f.read()

    expected_lines = [line.strip() for line in expected_content.strip().split('\n') if line.strip()]
    actual_lines = [line.strip() for line in actual_content.strip().split('\n') if line.strip()]

    assert actual_lines == expected_lines, f"Content of {file_path} does not match expected valid rows."

def test_run_metrics_json():
    file_path = "/home/user/run_metrics.json"
    assert os.path.exists(file_path), f"File {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    with open(file_path, "r") as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{file_path} is not valid JSON.")

    assert "valid_count" in metrics, "Key 'valid_count' missing in run_metrics.json"
    assert "mean" in metrics, "Key 'mean' missing in run_metrics.json"
    assert "sample_variance" in metrics, "Key 'sample_variance' missing in run_metrics.json"

    assert metrics["valid_count"] == 5, f"Expected valid_count to be 5, got {metrics['valid_count']}"
    assert math.isclose(metrics["mean"], 16.2000, abs_tol=1e-4), f"Expected mean to be ~16.2000, got {metrics['mean']}"
    assert math.isclose(metrics["sample_variance"], 25.6950, abs_tol=1e-4), f"Expected sample_variance to be ~25.6950, got {metrics['sample_variance']}"