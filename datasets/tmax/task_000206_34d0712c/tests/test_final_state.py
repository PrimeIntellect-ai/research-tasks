# test_final_state.py

import os
import pytest

def test_transform_c_exists():
    path = "/home/user/transform.c"
    assert os.path.isfile(path), f"Expected C source file {path} is missing."

def test_transform_executable_exists():
    path = "/home/user/transform"
    assert os.path.isfile(path), f"Expected compiled binary {path} is missing."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_normalized_gcode_output():
    path = "/home/user/dataset/normalized_experiment_01.gcode"
    assert os.path.isfile(path), f"Expected output file {path} is missing."

    expected_output = (
        "G1 X110.5 Y70.0 F3000\n"
        "G0 X115.0 Y75.5\n"
        "G1 X120.0 Y80.0 E1.5\n"
    )

    with open(path, "r", encoding="utf-8") as f:
        actual_output = f.read()

    # Strip trailing whitespace/newlines for comparison
    assert actual_output.strip() == expected_output.strip(), (
        f"Content of {path} does not match expected output.\n"
        f"Expected:\n{expected_output}\n"
        f"Actual:\n{actual_output}"
    )