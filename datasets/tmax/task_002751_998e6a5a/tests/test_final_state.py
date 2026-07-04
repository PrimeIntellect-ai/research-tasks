# test_final_state.py
import os
import json
import math

def test_ml_data_summary_exists_and_correct():
    file_path = "/home/user/ml_data_summary.json"
    assert os.path.isfile(file_path), f"The file {file_path} does not exist."

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {file_path} is not valid JSON."

    assert "top_3_singular_values" in data, "The JSON file is missing the 'top_3_singular_values' key."
    assert "max_abs_jerk" in data, "The JSON file is missing the 'max_abs_jerk' key."

    top_3 = data["top_3_singular_values"]
    max_jerk = data["max_abs_jerk"]

    assert isinstance(top_3, list), "'top_3_singular_values' should be a list."
    assert len(top_3) == 3, "'top_3_singular_values' must contain exactly 3 values."
    assert isinstance(max_jerk, (int, float)), "'max_abs_jerk' should be a number."

    # Expected approximate values from the problem description
    expected_top_3 = [44.116, 26.155, 6.746]
    expected_max_jerk = 31.815

    # Check top 3 singular values with a relative tolerance
    for i, (val, exp) in enumerate(zip(top_3, expected_top_3)):
        assert math.isclose(val, exp, rel_tol=5e-3), (
            f"Singular value at index {i} ({val}) is not close to the expected value ({exp})."
        )

    # Check max absolute jerk with a relative tolerance
    assert math.isclose(max_jerk, expected_max_jerk, rel_tol=5e-3), (
        f"Max absolute jerk ({max_jerk}) is not close to the expected value ({expected_max_jerk})."
    )