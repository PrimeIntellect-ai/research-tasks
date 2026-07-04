# test_final_state.py

import os
import pytest

def test_error_code_txt():
    path = "/home/user/error_code.txt"
    assert os.path.exists(path), f"File {path} does not exist. Did you extract the error code?"
    assert os.path.isfile(path), f"Path {path} is not a file."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "ERR_CODE_9X2A_MALFORMED_CSV", f"Incorrect error code found in {path}. Expected 'ERR_CODE_9X2A_MALFORMED_CSV', got '{content}'."

def test_final_sum_txt():
    path = "/home/user/final_sum.txt"
    assert os.path.exists(path), f"File {path} does not exist. Did you run the aggregator and save the output?"
    assert os.path.isfile(path), f"Path {path} is not a file."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "10000015.09", f"Incorrect final sum found in {path}. Expected '10000015.09', got '{content}'. Did you fix the precision loss and skip malformed rows correctly?"

def test_aggregator_cpp_fixed():
    path = "/home/user/aggregator.cpp"
    assert os.path.exists(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    # The precision loss bug must be fixed, likely by changing float to double
    assert "float total" not in content, "The precision loss bug is still present: 'float total' found in aggregator.cpp. You should use 'double' or 'long double'."
    assert "double" in content, "Expected to find 'double' in aggregator.cpp to fix the precision loss."