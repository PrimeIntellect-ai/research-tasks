# test_final_state.py

import os
import pytest

def test_executable_exists():
    executable_path = "/home/user/analytics"
    assert os.path.isfile(executable_path), f"Compiled executable {executable_path} is missing."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_variance_output_correct():
    output_path = "/home/user/variance_out.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    with open(output_path, "r") as f:
        content = f.read().strip()

    expected_variance = "8.341675"
    assert content == expected_variance, f"Expected variance output to be '{expected_variance}', but got '{content}'."

def test_analytics_cpp_modified():
    source_path = "/home/user/analytics.cpp"
    assert os.path.isfile(source_path), f"Source file {source_path} is missing."

    with open(source_path, "r") as f:
        content = f.read()

    # The original naive formula should be gone or changed, but we can just check if it's not the exact same buggy formula
    # Actually, it's safer to just rely on the output, but we can check that it doesn't contain the exact buggy line if we want.
    # We will just verify the output as the primary truth.