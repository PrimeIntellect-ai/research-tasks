# test_final_state.py

import os
import json
import math
import pytest

def test_script_exists():
    script_path = "/home/user/clean_pipeline.py"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_json_output_exists():
    json_path = "/home/user/cleaning_summary.json"
    assert os.path.exists(json_path), f"The output file {json_path} was not created."
    assert os.path.isfile(json_path), f"{json_path} is not a file."

def test_json_content():
    json_path = "/home/user/cleaning_summary.json"

    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    expected_keys = [
        "correlated_pair",
        "correlation_coefficient",
        "removed_anomalies_count",
        "t_test_p_value"
    ]

    for key in expected_keys:
        assert key in data, f"Key '{key}' is missing from {json_path}."

    # Expected values derived from the fixed random seed dataset
    expected_pair = ["sensor_A", "sensor_B"]
    expected_corr = 0.9859
    expected_removed = 14
    expected_p_value = 0.0528

    assert isinstance(data["correlated_pair"], list), "correlated_pair must be a list."
    assert sorted(data["correlated_pair"]) == expected_pair, \
        f"Expected correlated_pair to be {expected_pair}, got {data['correlated_pair']}."

    assert isinstance(data["correlation_coefficient"], (int, float)), "correlation_coefficient must be a number."
    assert math.isclose(data["correlation_coefficient"], expected_corr, abs_tol=1e-4), \
        f"Expected correlation_coefficient to be close to {expected_corr}, got {data['correlation_coefficient']}."

    assert isinstance(data["removed_anomalies_count"], int), "removed_anomalies_count must be an integer."
    assert data["removed_anomalies_count"] == expected_removed, \
        f"Expected removed_anomalies_count to be {expected_removed}, got {data['removed_anomalies_count']}."

    assert isinstance(data["t_test_p_value"], (int, float)), "t_test_p_value must be a number."
    assert math.isclose(data["t_test_p_value"], expected_p_value, abs_tol=1e-4), \
        f"Expected t_test_p_value to be close to {expected_p_value}, got {data['t_test_p_value']}."