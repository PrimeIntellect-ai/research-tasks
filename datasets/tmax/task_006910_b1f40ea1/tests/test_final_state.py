# test_final_state.py

import os
import math

def test_result_file_exists_and_correct():
    result_file = "/home/user/math_service/result.txt"
    assert os.path.exists(result_file), f"Result file {result_file} does not exist."

    with open(result_file, "r") as f:
        content = f.read().strip()

    assert content, "Result file is empty."

    try:
        result_val = float(content)
    except ValueError:
        raise AssertionError(f"Result file contains non-numeric data: {content}")

    # Recompute the expected integral
    # Values are x^2 for x in 1 to 100
    values = [float(x**2) for x in range(1, 101)]

    # Trapezoidal rule: sum of all elements minus half of the first and half of the last
    expected = sum(values) - (values[0] / 2.0) - (values[-1] / 2.0)

    assert math.isclose(result_val, expected, rel_tol=1e-5), \
        f"Expected integral value {expected}, but got {result_val}."