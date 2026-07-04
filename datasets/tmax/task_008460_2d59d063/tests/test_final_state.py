# test_final_state.py
import os
import json
import math
import pytest

def test_cpp_source_exists():
    """Test that the C++ source file exists."""
    assert os.path.isfile("/home/user/etl_bayes.cpp"), "The C++ source file /home/user/etl_bayes.cpp does not exist."

def test_cpp_executable_exists():
    """Test that the compiled executable exists."""
    assert os.path.isfile("/home/user/etl_bayes"), "The compiled executable /home/user/etl_bayes does not exist."
    assert os.access("/home/user/etl_bayes", os.X_OK), "The file /home/user/etl_bayes is not executable."

def test_posterior_json_exists_and_correct():
    """Test that the posterior.json file exists and contains the correct Bayesian update results."""
    json_path = "/home/user/posterior.json"
    assert os.path.isfile(json_path), f"The output file {json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    assert "posterior_mean" in data, "The JSON output is missing the 'posterior_mean' key."
    assert "posterior_variance" in data, "The JSON output is missing the 'posterior_variance' key."

    # The expected values based on the valid rows (1, 2, 6)
    # n = 3, sum = 3.0
    # posterior_variance = 1 / (1/1.0 + 3/1.0) = 0.25
    # posterior_mean = 0.25 * (0.0/1.0 + 3.0/1.0) = 0.75

    expected_mean = 0.75
    expected_variance = 0.25

    assert math.isclose(data["posterior_mean"], expected_mean, abs_tol=1e-4), \
        f"Expected posterior_mean to be {expected_mean}, but got {data['posterior_mean']}."

    assert math.isclose(data["posterior_variance"], expected_variance, abs_tol=1e-4), \
        f"Expected posterior_variance to be {expected_variance}, but got {data['posterior_variance']}."