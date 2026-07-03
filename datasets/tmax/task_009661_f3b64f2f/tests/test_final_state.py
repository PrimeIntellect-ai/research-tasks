# test_final_state.py

import os
import json
import pytest

def test_joined_csv_exists():
    path = "/home/user/data/joined.csv"
    assert os.path.isfile(path), f"File {path} is missing. The Python script should create it."

def test_results_json_exists():
    path = "/home/user/results.json"
    assert os.path.isfile(path), f"File {path} is missing. The R script should create it."

def test_results_json_contents():
    path = "/home/user/results.json"
    assert os.path.isfile(path), "results.json is missing"

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("results.json is not a valid JSON file.")

    expected_keys = {"joined_rows", "correlation", "ci_lower", "ci_upper"}
    missing_keys = expected_keys - set(data.keys())
    assert not missing_keys, f"results.json is missing keys: {missing_keys}"

    assert isinstance(data["joined_rows"], int), "joined_rows must be an integer"
    assert isinstance(data["correlation"], (int, float)), "correlation must be a float"
    assert isinstance(data["ci_lower"], (int, float)), "ci_lower must be a float"
    assert isinstance(data["ci_upper"], (int, float)), "ci_upper must be a float"

def test_results_values():
    path = "/home/user/results.json"
    if not os.path.isfile(path):
        pytest.skip("results.json missing")

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except:
            pytest.skip("invalid json")

    assert data.get("joined_rows") == 341, f"Expected 341 joined_rows, got {data.get('joined_rows')}"

    correlation = data.get("correlation")
    assert 0.9500 <= correlation <= 0.9650, f"Correlation {correlation} is outside the expected range [0.9500, 0.9650]"

    ci_lower = data.get("ci_lower")
    ci_upper = data.get("ci_upper")

    assert ci_lower < correlation < ci_upper, "Correlation should be between ci_lower and ci_upper"
    assert 0.93 <= ci_lower <= 0.96, f"ci_lower {ci_lower} is outside expected range"
    assert 0.96 <= ci_upper <= 0.98, f"ci_upper {ci_upper} is outside expected range"