# test_final_state.py

import os
import subprocess
import pytest

def test_pipeline_exists_and_executable():
    """Test that pipeline.sh exists and is executable."""
    file_path = "/home/user/pipeline.sh"
    assert os.path.isfile(file_path), f"{file_path} is missing."
    assert os.access(file_path, os.X_OK), f"{file_path} is not executable."

def test_run_pipeline():
    """Test that pipeline.sh runs successfully."""
    file_path = "/home/user/pipeline.sh"
    result = subprocess.run([file_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {file_path} failed with return code {result.returncode}.\nStderr: {result.stderr}"

def test_cleaned_predictions_output():
    """Test that cleaned_predictions.csv contains the correct predictions."""
    file_path = "/home/user/cleaned_predictions.csv"
    assert os.path.isfile(file_path), f"{file_path} was not created."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 6, f"Expected 6 lines in {file_path} (header + 5 rows), got {len(lines)}."
    assert lines[0] == "user_id,predicted_LTV", f"Incorrect header in {file_path}: {lines[0]}"

    expected_predictions = {
        "U001": "523.80",
        "U002": "629.15",
        "U003": "31.25",
        "U004": ["1228.82", "1228.83"], # allow both standard rounding results
        "U005": "834.20"
    }

    for line in lines[1:]:
        parts = line.split(",")
        assert len(parts) == 2, f"Malformed line in {file_path}: {line}"
        user_id, predicted_LTV = parts
        assert user_id in expected_predictions, f"Unexpected user_id {user_id} in {file_path}"
        expected = expected_predictions[user_id]
        if isinstance(expected, list):
            assert predicted_LTV in expected, f"Incorrect prediction for {user_id}. Expected one of {expected}, got {predicted_LTV}"
        else:
            assert predicted_LTV == expected, f"Incorrect prediction for {user_id}. Expected {expected}, got {predicted_LTV}"

def test_nearest_to_U001_output():
    """Test that nearest_to_U001.txt contains the correct user_id."""
    file_path = "/home/user/nearest_to_U001.txt"
    assert os.path.isfile(file_path), f"{file_path} was not created."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == "U004", f"Incorrect content in {file_path}. Expected 'U004', got '{content}'"