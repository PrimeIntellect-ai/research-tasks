# test_final_state.py

import os
import pytest

def test_predictions_csv_exists_and_correct():
    file_path = "/home/user/predictions.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} is missing. The script did not generate it."

    expected_lines = [
        "ServerID,RiskScore,Alert",
        "srv_004,174.19,1",
        "srv_005,81.78,1",
        "srv_001,48.28,0",
        "srv_002,45.19,0",
        "srv_003,1.60,0"
    ]

    with open(file_path, "r") as f:
        # Read lines, strip whitespace/newlines, and ignore empty lines
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"The content of {file_path} does not match the expected output. "
        f"Expected:\n{chr(10).join(expected_lines)}\n\nActual:\n{chr(10).join(actual_lines)}"
    )