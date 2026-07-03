# test_final_state.py

import os
import math

def test_test_corr_mean_file():
    """Test that the test_corr_mean.txt file exists and contains the correct value."""
    file_path = "/home/user/test_corr_mean.txt"
    assert os.path.exists(file_path), f"Missing output file: {file_path}"

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content, f"File {file_path} is empty."

    try:
        val = float(content)
    except ValueError:
        raise AssertionError(f"Content of {file_path} is not a valid float: '{content}'")

    expected_val = 0.063063
    assert math.isclose(val, expected_val, abs_tol=1e-5), \
        f"Expected correlation mean to be close to {expected_val}, but got {val}"

def test_recommendations_file():
    """Test that the recommendations.txt file exists and contains the correct indices."""
    file_path = "/home/user/recommendations.txt"
    assert os.path.exists(file_path), f"Missing output file: {file_path}"

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content, f"File {file_path} is empty."

    # The indices should be exactly these based on the deterministic random seed and data
    expected_recs = "750,230,123"

    # Remove any spaces that might have been added
    actual_recs = content.replace(" ", "")

    assert actual_recs == expected_recs, \
        f"Expected recommendations to be '{expected_recs}', but got '{content}'"