# test_final_state.py

import os
import math
import pytest

def test_fit_model_cpp_exists():
    cpp_path = "/home/user/fit_model.cpp"
    assert os.path.isfile(cpp_path), f"Expected C++ source file {cpp_path} does not exist."

def test_result_txt_exists_and_correct():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"Expected results file {result_path} does not exist."

    with open(result_path, 'r') as f:
        content = f.read().strip().split()

    assert len(content) == 3, f"Expected exactly 3 values in {result_path}, found {len(content)}."

    try:
        mean_t, ci_l, ci_u = map(float, content)
    except ValueError:
        pytest.fail(f"Could not parse the contents of {result_path} as 3 floating-point numbers.")

    expected_mean = 2.49
    expected_lower = 2.42
    expected_upper = 2.55
    tolerance = 0.1

    assert math.isclose(mean_t, expected_mean, abs_tol=tolerance), \
        f"Mean Theta1 {mean_t} is not within {tolerance} of expected {expected_mean}."

    assert math.isclose(ci_l, expected_lower, abs_tol=tolerance), \
        f"CI Lower {ci_l} is not within {tolerance} of expected {expected_lower}."

    assert math.isclose(ci_u, expected_upper, abs_tol=tolerance), \
        f"CI Upper {ci_u} is not within {tolerance} of expected {expected_upper}."