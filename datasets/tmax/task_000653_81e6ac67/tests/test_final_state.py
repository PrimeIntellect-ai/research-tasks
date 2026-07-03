# test_final_state.py

import os
import json
import math
import pytest

def test_script_exists():
    """Test that the analysis script was created."""
    script_path = "/home/user/analyze_spectrum.py"
    assert os.path.exists(script_path), f"Expected script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_result_file_exists():
    """Test that the output JSON file exists."""
    result_path = "/home/user/hypothesis_result.json"
    assert os.path.exists(result_path), f"Expected result file {result_path} does not exist."
    assert os.path.isfile(result_path), f"{result_path} is not a file."

def test_result_values():
    """Test that the output JSON file contains the correct calculated values."""
    result_path = "/home/user/hypothesis_result.json"
    if not os.path.exists(result_path):
        pytest.skip("Result file does not exist, skipping value checks.")

    with open(result_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Result file is not valid JSON.")

    expected_keys = {"power_A", "power_B", "best_model"}
    missing_keys = expected_keys - set(data.keys())
    assert not missing_keys, f"Result JSON is missing keys: {missing_keys}"

    # Expected values derived from the truth script
    expected_power_a = 41.05050519159955
    expected_power_b = 24.939151247065902
    expected_best_model = "A"

    assert isinstance(data["power_A"], (int, float)), "power_A must be a number."
    assert isinstance(data["power_B"], (int, float)), "power_B must be a number."

    assert math.isclose(data["power_A"], expected_power_a, rel_tol=1e-3), \
        f"power_A value {data['power_A']} is not close to expected {expected_power_a}."

    assert math.isclose(data["power_B"], expected_power_b, rel_tol=1e-3), \
        f"power_B value {data['power_B']} is not close to expected {expected_power_b}."

    assert data["best_model"] == expected_best_model, \
        f"best_model is '{data['best_model']}', expected '{expected_best_model}'."