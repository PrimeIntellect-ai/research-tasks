# test_final_state.py

import os
import json
import math
import pytest

def test_train_fixed_exists():
    """Verify that train_fixed.py exists."""
    file_path = "/home/user/train_fixed.py"
    assert os.path.isfile(file_path), f"File {file_path} is missing. You must create the fixed training script."

def test_model_fixed_exists():
    """Verify that model_fixed.pkl exists."""
    file_path = "/home/user/model_fixed.pkl"
    assert os.path.isfile(file_path), f"File {file_path} is missing. You must save the fixed model pipeline."

def test_report_json_exists_and_valid():
    """Verify that report.json exists, is valid JSON, and contains the correct keys."""
    file_path = "/home/user/report.json"
    assert os.path.isfile(file_path), f"File {file_path} is missing. You must create the report."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{file_path} is not a valid JSON file.")

    assert "leaky_accuracy" in data, "Key 'leaky_accuracy' is missing from report.json."
    assert "fixed_accuracy" in data, "Key 'fixed_accuracy' is missing from report.json."

def test_report_accuracies():
    """Verify that the accuracies in report.json match the expected values."""
    file_path = "/home/user/report.json"
    if not os.path.isfile(file_path):
        pytest.skip("report.json is missing.")

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.skip("report.json is not valid JSON.")

    leaky_acc = data.get("leaky_accuracy")
    fixed_acc = data.get("fixed_accuracy")

    assert isinstance(leaky_acc, (int, float)), "leaky_accuracy must be a number."
    assert isinstance(fixed_acc, (int, float)), "fixed_accuracy must be a number."

    # Expected values derived from the dataset generation and specific random states
    expected_leaky = 0.8000
    expected_fixed = 0.7933

    assert math.isclose(leaky_acc, expected_leaky, abs_tol=0.01), f"leaky_accuracy {leaky_acc} is incorrect. Expected ~{expected_leaky}."
    assert math.isclose(fixed_acc, expected_fixed, abs_tol=0.01), f"fixed_accuracy {fixed_acc} is incorrect. Expected ~{expected_fixed}."