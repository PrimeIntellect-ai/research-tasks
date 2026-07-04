# test_final_state.py

import os
import pytest

def test_result_file_exists():
    path = "/home/user/result.txt"
    assert os.path.isfile(path), f"Expected file {path} does not exist."

def test_result_file_content():
    path = "/home/user/result.txt"
    assert os.path.isfile(path), f"Expected file {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content, f"{path} is empty."

    try:
        kl_value = float(content)
    except ValueError:
        pytest.fail(f"Content of {path} is not a valid float: '{content}'")

    assert kl_value < 0.01, f"KL divergence value in {path} is {kl_value}, which is not less than 0.01. The C code bug might not be correctly fixed."

def test_output_file_exists():
    path = "/home/user/output.txt"
    assert os.path.isfile(path), f"Expected output file {path} does not exist. Did you run the compiled C program?"

    with open(path, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) > 0, f"{path} is empty."
    # Basic check to ensure output.txt has numbers, not NaN
    try:
        float(lines[0])
    except ValueError:
        pytest.fail(f"First line of {path} is not a valid number: '{lines[0]}'")