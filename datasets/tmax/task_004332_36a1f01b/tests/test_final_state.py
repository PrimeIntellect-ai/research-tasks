# test_final_state.py

import os
import pytest

def test_result_file_exists():
    assert os.path.isfile("/home/user/result.txt"), "The file /home/user/result.txt does not exist. Did you run `cargo run > /home/user/result.txt`?"

def test_result_file_content():
    with open("/home/user/result.txt", "r") as f:
        content = f.read().strip()

    assert content, "The file /home/user/result.txt is empty."

    try:
        value = float(content)
    except ValueError:
        pytest.fail(f"The content of /home/user/result.txt is not a valid float: '{content}'")

    # The expected value is approximately 52.6986
    expected_value = 52.6986
    tolerance = 0.01

    assert abs(value - expected_value) < tolerance, f"Expected value around {expected_value}, but got {value}. The data leak might not be fixed correctly."

def test_processor_file_modified():
    # Check if the code was actually modified to fix the data leak.
    # We can check if `calculate_mean` and `calculate_std` are called on the split data.
    with open("/home/user/dataset_processor/src/processor.rs", "r") as f:
        content = f.read()

    # A simple heuristic check to ensure the file was modified from its original state.
    assert "BUG: Data Leak" not in content or "calculate_mean(all_data)" not in content, "The data leak bug seems to still be present in src/processor.rs."