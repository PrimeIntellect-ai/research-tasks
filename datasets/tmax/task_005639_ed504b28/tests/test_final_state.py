# test_final_state.py

import os
import json
import math
import pytest

def test_results_file_exists():
    """Check that the results.json file exists."""
    results_path = "/home/user/results.json"
    assert os.path.exists(results_path), f"Results file {results_path} does not exist."
    assert os.path.isfile(results_path), f"{results_path} is not a file."

def test_results_json_structure():
    """Check that the results.json file contains the exact required keys with float values."""
    results_path = "/home/user/results.json"
    with open(results_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} is not valid JSON.")

    expected_keys = {
        "E_10", "E_20", "E_40", "p_1", "p_2", 
        "shapiro_statistic", "shapiro_p_value"
    }

    actual_keys = set(data.keys())
    missing_keys = expected_keys - actual_keys
    extra_keys = actual_keys - expected_keys

    assert not missing_keys, f"Missing keys in results.json: {missing_keys}"
    assert not extra_keys, f"Extra keys in results.json: {extra_keys}"

    for key in expected_keys:
        val = data[key]
        assert isinstance(val, (int, float)), f"Value for {key} must be a number, got {type(val)}."

def test_results_values_plausible():
    """Check that the values in results.json are mathematically plausible for this problem."""
    results_path = "/home/user/results.json"
    with open(results_path, "r") as f:
        data = json.load(f)

    E_10 = data["E_10"]
    E_20 = data["E_20"]
    E_40 = data["E_40"]
    p_1 = data["p_1"]
    p_2 = data["p_2"]
    stat = data["shapiro_statistic"]
    pval = data["shapiro_p_value"]

    # Errors should be positive and decreasing
    assert E_10 > 0, "Max error E_10 should be positive."
    assert E_20 > 0, "Max error E_20 should be positive."
    assert E_40 > 0, "Max error E_40 should be positive."
    assert E_10 > E_20 > E_40, "Errors should decrease as N increases."

    # Convergence order for 2nd order central difference is expected to be around 2
    assert 1.8 < p_1 < 2.2, f"Convergence order p_1={p_1} is far from expected ~2.0."
    assert 1.8 < p_2 < 2.2, f"Convergence order p_2={p_2} is far from expected ~2.0."

    # Shapiro-Wilk statistic is between 0 and 1
    assert 0.0 <= stat <= 1.0, f"Shapiro-Wilk statistic {stat} must be between 0 and 1."

    # p-value is between 0 and 1
    assert 0.0 <= pval <= 1.0, f"Shapiro-Wilk p-value {pval} must be between 0 and 1."

def test_results_rounding():
    """Check that the results are rounded to exactly 6 decimal places."""
    results_path = "/home/user/results.json"
    with open(results_path, "r") as f:
        # Read as text to check string representation
        content = f.read()
        data = json.loads(content)

    for key, val in data.items():
        # A float rounded to 6 decimal places should stringify to at most 6 decimal places
        # (though Python's float representation might add noise, we check if the value is close to its rounded self)
        rounded_val = round(val, 6)
        assert math.isclose(val, rounded_val, rel_tol=1e-9, abs_tol=1e-9), \
            f"Value for {key} ({val}) does not appear to be rounded to 6 decimal places."