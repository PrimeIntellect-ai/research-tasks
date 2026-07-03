# test_final_state.py

import os
import json
import pytest

def test_analyze_go_exists():
    file_path = "/home/user/analyze.go"
    assert os.path.exists(file_path), f"File {file_path} is missing."

def test_results_json_exists_and_correct():
    file_path = "/home/user/results.json"
    assert os.path.exists(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} does not contain valid JSON.")

    assert "A" in results, "Missing variant 'A' in results."
    assert "B" in results, "Missing variant 'B' in results."

    expected_A = {
        "mean": 0.1208,
        "variance": 0.0001,
        "ci_lower": 0.1006,
        "ci_upper": 0.1409
    }

    expected_B = {
        "mean": 0.1530,
        "variance": 0.0001,
        "ci_lower": 0.1313,
        "ci_upper": 0.1748
    }

    for variant, expected in [("A", expected_A), ("B", expected_B)]:
        for key, expected_val in expected.items():
            assert key in results[variant], f"Missing key '{key}' in variant '{variant}'."
            actual_val = results[variant][key]
            assert isinstance(actual_val, (int, float)), f"Value for '{key}' in variant '{variant}' must be a number."
            assert abs(actual_val - expected_val) <= 0.0001, f"Expected {key} for {variant} to be close to {expected_val}, got {actual_val}."