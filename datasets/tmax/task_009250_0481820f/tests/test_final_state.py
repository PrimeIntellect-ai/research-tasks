# test_final_state.py

import os
import pytest

def test_prepare_data_script_exists_and_executable():
    script_path = "/home/user/prepare_data.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_training_data_exists_and_correct():
    output_file = "/home/user/training_data.csv"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist. Did you run your script?"

    expected_content = (
        "sim_id,optimal_k\n"
        "1,0.01\n"
        "2,0.04\n"
        "3,0.00\n"
        "4,0.02"
    )

    with open(output_file, "r") as f:
        content = f.read().strip()

    # Compare line by line to give better error messages
    expected_lines = expected_content.splitlines()
    actual_lines = content.splitlines()

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {output_file}, but found {len(actual_lines)}."

    for i, (expected_line, actual_line) in enumerate(zip(expected_lines, actual_lines)):
        assert actual_line == expected_line, f"Mismatch at line {i + 1} in {output_file}. Expected '{expected_line}', got '{actual_line}'."