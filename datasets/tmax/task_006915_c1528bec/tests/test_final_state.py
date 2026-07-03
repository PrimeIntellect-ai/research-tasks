# test_final_state.py

import os
import pytest

def test_generate_cpp_exists_and_uses_openmp():
    """Check that generate.cpp exists and uses OpenMP."""
    cpp_file = "/home/user/generate.cpp"
    assert os.path.isfile(cpp_file), f"File {cpp_file} does not exist."

    with open(cpp_file, "r") as f:
        content = f.read()

    assert "omp" in content.lower(), f"File {cpp_file} does not seem to use OpenMP (no 'omp' found)."

def test_result_txt_exists_and_correct():
    """Check that result.txt exists and contains the correct computed sum."""
    result_file = "/home/user/result.txt"
    assert os.path.isfile(result_file), f"File {result_file} does not exist. Did you run the compiled program?"

    # Compute the expected sum
    s = 0.0
    for i in range(1000):
        k = 0.1 + i * (0.9 / 999)
        y = 1.0
        for _ in range(1000):
            y = y * (1.0 - k * 0.01)
        s += y
    expected_val = f"{s:.4f}"

    with open(result_file, "r") as f:
        content = f.read().strip()

    assert content == expected_val, f"Expected {expected_val} in {result_file}, but found '{content}'."