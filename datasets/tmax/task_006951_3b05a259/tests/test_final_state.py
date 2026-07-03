# test_final_state.py
import os
import json
import pytest

def test_labels_json_exists_and_valid():
    """Verify that the labels.json file exists and contains the correct values."""
    file_path = "/home/user/labels.json"

    assert os.path.isfile(file_path), f"Required output file is missing: {file_path}"

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not valid JSON.")

    expected_keys = {"mu1", "mu2", "intersection_x"}
    actual_keys = set(data.keys())
    assert expected_keys.issubset(actual_keys), f"JSON is missing required keys. Expected: {expected_keys}, Found: {actual_keys}"

    mu1 = data["mu1"]
    mu2 = data["mu2"]
    intersection_x = data["intersection_x"]

    assert isinstance(mu1, (int, float)), "mu1 must be a number"
    assert isinstance(mu2, (int, float)), "mu2 must be a number"
    assert isinstance(intersection_x, (int, float)), "intersection_x must be a number"

    # Check values against expected approximations
    assert abs(mu1 - 500.0) < 1.0, f"mu1 is out of expected range. Expected ~500.0, got {mu1}"
    assert abs(mu2 - 700.0) < 1.0, f"mu2 is out of expected range. Expected ~700.0, got {mu2}"
    assert abs(intersection_x - 585.9) < 2.0, f"intersection_x is out of expected range. Expected ~585.9, got {intersection_x}"