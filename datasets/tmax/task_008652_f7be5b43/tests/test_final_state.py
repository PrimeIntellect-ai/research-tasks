# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/predict.sh"

def test_script_exists():
    """Test that the predict.sh script exists."""
    assert os.path.exists(SCRIPT_PATH), f"Expected script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"Expected {SCRIPT_PATH} to be a file."

def test_script_prediction_1():
    """Test the prediction for learning_rate=0.04 and batch_size=48."""
    result = subprocess.run(
        ["bash", SCRIPT_PATH, "0.04", "48"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"
    output = result.stdout.strip()
    assert output == "0.8920", f"Expected prediction '0.8920', got '{output}'"

def test_script_prediction_2():
    """Test the prediction for learning_rate=0.08 and batch_size=256."""
    result = subprocess.run(
        ["bash", SCRIPT_PATH, "0.08", "256"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"
    output = result.stdout.strip()
    assert output == "0.7240", f"Expected prediction '0.7240', got '{output}'"