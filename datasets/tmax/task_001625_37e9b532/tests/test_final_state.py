# test_final_state.py

import os
import pytest
import math

def test_calc_ci_cpp_exists():
    cpp_file = "/home/user/calc_ci.cpp"
    assert os.path.isfile(cpp_file), f"C++ source file missing: {cpp_file}"

def test_ci_output_exists_and_correct():
    out_file = "/home/user/ci_output.txt"
    assert os.path.isfile(out_file), f"Output file missing: {out_file}"

    # Calculate the expected values to ensure correctness
    accuracies = [0.81, 0.83, 0.80, 0.82, 0.84]
    n = len(accuracies)
    mean = sum(accuracies) / n
    variance = sum((x - mean) ** 2 for x in accuracies) / (n - 1)
    stddev = math.sqrt(variance)
    stderr = stddev / math.sqrt(n)
    margin = 1.96 * stderr
    lower_bound = mean - margin
    upper_bound = mean + margin

    expected_output = f"Mean: {mean:.4f}, CI: [{lower_bound:.4f}, {upper_bound:.4f}]"

    with open(out_file, 'r') as f:
        content = f.read().strip()

    assert content == expected_output, f"Output file content is incorrect. Expected '{expected_output}', got '{content}'"