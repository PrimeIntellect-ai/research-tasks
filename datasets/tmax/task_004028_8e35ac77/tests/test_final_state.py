# test_final_state.py

import os
import pytest

def test_recovered_key_exists_and_correct():
    """Check if the recovered API key is correct."""
    path = "/home/user/recovered_key.txt"
    assert os.path.isfile(path), f"File {path} does not exist. Did you recover the API key?"

    with open(path, "r") as f:
        content = f.read().strip()

    expected_key = "SK-9942-ABCF-1111"
    assert content == expected_key, f"Recovered key is incorrect. Expected '{expected_key}', got '{content}'."

def test_result_exists_and_correct():
    """Check if the math result is correctly computed and written to the right path."""
    path = "/home/user/result.txt"
    assert os.path.isfile(path), f"File {path} does not exist. Did you fix the script and run it?"

    # Compute the expected 5000th Fibonacci number modulo 100000
    a, b = 0, 1
    for _ in range(5000):
        a, b = b, (a + b) % 100000
    expected_result = str(a)

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == expected_result, f"Math result is incorrect. Expected '{expected_result}', got '{content}'."