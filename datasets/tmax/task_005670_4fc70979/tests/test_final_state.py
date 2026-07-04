# test_final_state.py

import os
import pytest

def test_dataset_extracted():
    """Test that the dataset was correctly extracted to /home/user/data/."""
    file_path = "/home/user/data/dataset.csv"
    assert os.path.isfile(file_path), f"Extracted dataset not found at {file_path}"

def test_optimize_script_exists_and_executable():
    """Test that optimize.sh exists and is executable."""
    file_path = "/home/user/optimize.sh"
    assert os.path.isfile(file_path), f"Missing script: {file_path}"
    assert os.access(file_path, os.X_OK), f"Script is not executable: {file_path}"

def test_best_params_output():
    """Test that best_params.csv has the correct optimal parameters."""
    file_path = "/home/user/best_params.csv"
    assert os.path.isfile(file_path), f"Missing output file: {file_path}"

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {file_path}, got {len(lines)}"

    header = lines[0]
    assert header == "threads,reg,error", f"Incorrect header: expected 'threads,reg,error', got '{header}'"

    values = lines[1].split(",")
    assert len(values) == 3, f"Expected 3 comma-separated values in the second line, got {len(values)}"

    threads, reg, error = values
    assert threads == "2", f"Expected optimal threads to be 2, got {threads}"
    assert reg == "0.1", f"Expected optimal regularization to be 0.1, got {reg}"

    try:
        error_val = float(error)
    except ValueError:
        pytest.fail(f"Error value '{error}' is not a valid float")

    assert abs(error_val - 0.5) < 1e-5, f"Expected minimum error to be approximately 0.5000, got {error_val}"