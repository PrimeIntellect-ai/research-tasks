# test_final_state.py

import os
import re
import pytest

def test_results_file_exists():
    """Check if the results.txt file has been created."""
    results_file = "/home/user/project/results.txt"
    assert os.path.isfile(results_file), f"Results file {results_file} is missing."

def test_results_content_and_accuracy():
    """Parse results.txt and verify that c_mean and k_mean are within the expected ranges."""
    results_file = "/home/user/project/results.txt"
    assert os.path.isfile(results_file), f"Results file {results_file} is missing."

    with open(results_file, 'r') as f:
        content = f.read()

    c_match = re.search(r'c_mean:\s*([0-9.]+)', content)
    k_match = re.search(r'k_mean:\s*([0-9.]+)', content)

    assert c_match is not None, "Could not find 'c_mean: X.XX' in results.txt."
    assert k_match is not None, "Could not find 'k_mean: Y.YY' in results.txt."

    try:
        c_mean = float(c_match.group(1))
        k_mean = float(k_match.group(1))
    except ValueError:
        pytest.fail("Found c_mean or k_mean, but the values are not valid numbers.")

    assert 0.4 <= c_mean <= 0.6, f"c_mean {c_mean} is not within the expected range [0.4, 0.6]."
    assert 1.9 <= k_mean <= 2.1, f"k_mean {k_mean} is not within the expected range [1.9, 2.1]."