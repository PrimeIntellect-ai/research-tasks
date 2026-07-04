# test_final_state.py
import os

def test_model_inputs_log_exists():
    """Verify that the output log file was created."""
    assert os.path.isfile("/home/user/model_inputs.log"), "The file /home/user/model_inputs.log does not exist."

def test_model_inputs_log_content():
    """Verify that the output log file contains the exact expected classifications."""
    expected_lines = [
        "Q1: Singular",
        "Q2: Valid",
        "Q3: Anomalous",
        "Q4: Valid"
    ]

    with open("/home/user/model_inputs.log", "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"The contents of /home/user/model_inputs.log are incorrect.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )