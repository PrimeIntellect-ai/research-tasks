# test_final_state.py
import os
import json
import math

def test_report_json_exists_and_valid():
    report_path = '/home/user/report.json'
    assert os.path.isfile(report_path), f"Expected report file at {report_path} is missing."

    with open(report_path, 'r') as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {report_path} does not contain valid JSON."

    expected_keys = {"leaky_mse", "fixed_mse", "p_value"}
    actual_keys = set(report_data.keys())
    assert actual_keys == expected_keys, f"JSON keys in {report_path} do not match expected. Expected: {expected_keys}, Got: {actual_keys}"

    for key in expected_keys:
        val = report_data[key]
        assert isinstance(val, (int, float)), f"Expected numeric value for {key}, got {type(val).__name__}."
        assert not math.isnan(val), f"Value for {key} is NaN."

def test_report_json_values_plausible():
    report_path = '/home/user/report.json'
    if not os.path.isfile(report_path):
        return # Handled by previous test

    with open(report_path, 'r') as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            return

    if not set(report_data.keys()) == {"leaky_mse", "fixed_mse", "p_value"}:
        return

    leaky_mse = report_data["leaky_mse"]
    fixed_mse = report_data["fixed_mse"]
    p_value = report_data["p_value"]

    assert leaky_mse > 0, f"leaky_mse must be strictly positive, got {leaky_mse}"
    assert fixed_mse > 0, f"fixed_mse must be strictly positive, got {fixed_mse}"
    assert 0.0 <= p_value <= 1.0, f"p_value must be a valid probability between 0 and 1, got {p_value}"