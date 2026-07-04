# test_final_state.py

import os
import pytest

def test_calibrator_c_exists():
    filepath = "/home/user/calibrator.c"
    assert os.path.isfile(filepath), f"File {filepath} does not exist. The source code must be preserved."

def test_calibrator_executable_exists():
    filepath = "/home/user/calibrator"
    assert os.path.isfile(filepath), f"Executable {filepath} does not exist. Did you compile the program?"
    assert os.access(filepath, os.X_OK), f"File {filepath} is not executable."

def test_calibration_output_correct():
    filepath = "/home/user/calibration_output.txt"
    assert os.path.isfile(filepath), f"Output file {filepath} does not exist. Did you run the program and redirect output?"

    expected_output = (
        "Sum: 150\n"
        "Root 0: 3.162\n"
        "Root 1: 4.472\n"
        "Root 2: 5.477\n"
        "Root 3: 6.325\n"
        "Root 4: 7.071\n"
    )

    with open(filepath, "r") as f:
        actual_output = f.read()

    assert actual_output.strip() == expected_output.strip(), (
        f"Contents of {filepath} do not match the expected output.\n"
        f"Expected:\n{expected_output}\n"
        f"Actual:\n{actual_output}"
    )