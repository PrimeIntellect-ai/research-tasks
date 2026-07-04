# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/run_pipeline.sh"
PREDICTIONS_PATH = "/home/user/predictions.csv"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"The script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"The script {SCRIPT_PATH} is not executable. Did you forget to run 'chmod +x'?"

def test_predictions_correct():
    # Run the student's script to generate the predictions
    try:
        result = subprocess.run([SCRIPT_PATH], capture_output=True, text=True, timeout=30)
        assert result.returncode == 0, f"Script failed with return code {result.returncode}.\nStderr: {result.stderr}"
    except Exception as e:
        pytest.fail(f"Failed to execute the script: {e}")

    # Verify the output file was created
    assert os.path.isfile(PREDICTIONS_PATH), f"The predictions file {PREDICTIONS_PATH} was not created by the script."

    # Verify the content of the predictions file
    with open(PREDICTIONS_PATH, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "id,prediction",
        "101,A",
        "102,B",
        "103,A",
        "104,B"
    ]

    actual_lines = [line.strip() for line in content.split("\n") if line.strip()]

    assert actual_lines == expected_lines, (
        f"The contents of {PREDICTIONS_PATH} do not match the expected predictions.\n"
        f"Expected: {expected_lines}\n"
        f"Got: {actual_lines}"
    )