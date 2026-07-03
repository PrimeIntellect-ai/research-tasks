# test_final_state.py

import os
import pytest

def test_crash_file_correct():
    crash_file_path = "/home/user/crash_file.txt"
    assert os.path.isfile(crash_file_path), f"File {crash_file_path} is missing."

    with open(crash_file_path, "r") as f:
        content = f.read().strip()

    expected = "batch_C broken.txt"
    assert content == expected, f"Expected crash_file.txt to contain '{expected}', but found '{content}'."

def test_fuzz_test_exists_and_valid():
    test_file_path = "/home/user/calc/calc_test.go"
    assert os.path.isfile(test_file_path), f"Fuzz test file {test_file_path} is missing."

    with open(test_file_path, "r") as f:
        content = f.read()

    assert "func FuzzCalculate" in content, "Could not find 'func FuzzCalculate' in calc_test.go."
    assert "testing.F" in content, "The fuzz test does not appear to use the '*testing.F' type."

def test_accumulator_value_correct():
    accumulator_file_path = "/home/user/accumulator.txt"
    assert os.path.isfile(accumulator_file_path), f"File {accumulator_file_path} is missing."

    with open(accumulator_file_path, "r") as f:
        content = f.read().strip()

    expected = "56"
    assert content == expected, f"Expected accumulator.txt to contain '{expected}', but found '{content}'."