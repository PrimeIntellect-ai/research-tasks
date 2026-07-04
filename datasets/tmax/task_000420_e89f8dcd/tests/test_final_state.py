# test_final_state.py

import os
import math

def test_variance_results_file_exists():
    """Check that the variance_results.csv file exists."""
    file_path = "/home/user/variance_results.csv"
    assert os.path.exists(file_path), f"File {file_path} is missing. Did you save the results?"
    assert os.path.isfile(file_path), f"Path {file_path} is not a file."

def test_variance_results_content():
    """Check that the variance results match the expected values."""
    file_path = "/home/user/variance_results.csv"

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content, "The variance_results.csv file is empty."

    parts = content.split(",")
    assert len(parts) == 2, f"Expected 2 comma-separated values, but got {len(parts)}: '{content}'"

    try:
        var_naive = float(parts[0])
        var_twopass = float(parts[1])
    except ValueError:
        assert False, f"Could not parse the results as floats. File content: '{content}'"

    # The two-pass variance should be numerically stable and match the mathematical expectation
    expected_twopass = 53.4725
    assert math.isclose(var_twopass, expected_twopass, abs_tol=0.001), \
        f"Two-pass variance {var_twopass} is incorrect. Expected approximately {expected_twopass}."

    # The naive variance should exhibit catastrophic cancellation due to the 1e9 offset
    # It will typically be 0.0000 or a wildly incorrect value, but definitely not the true variance
    assert var_naive < 1.0 or var_naive < 0, \
        f"Naive variance {var_naive} did not exhibit the expected catastrophic cancellation. Expected ~0.0000."