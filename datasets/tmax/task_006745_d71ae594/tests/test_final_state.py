# test_final_state.py
import os
import json
import pytest

def test_experiment_log_exists_and_valid():
    """Check if experiment_log.json exists, is valid JSON, and has correct structure."""
    log_path = "/home/user/experiment_log.json"
    assert os.path.isfile(log_path), f"File {log_path} is missing."

    with open(log_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{log_path} does not contain valid JSON.")

    assert isinstance(data, list), f"{log_path} should contain a JSON array."
    assert len(data) == 26, f"Expected 26 entries in {log_path}, got {len(data)}."

    for item in data:
        assert "D" in item, f"Missing 'D' key in {item}"
        assert "error" in item, f"Missing 'error' key in {item}"

def test_experiment_log_specific_values():
    """Check specific values in experiment_log.json."""
    log_path = "/home/user/experiment_log.json"
    assert os.path.isfile(log_path), f"File {log_path} is missing."

    with open(log_path, "r") as f:
        data = json.load(f)

    d1_error = None
    d3_error = None

    for item in data:
        if item.get("D") == 1:
            d1_error = item.get("error")
        elif item.get("D") == 3:
            d3_error = item.get("error")

    assert d1_error is not None, "No entry for D=1 found."
    assert d1_error == 1.00, f"Expected error for D=1 to be 1.00, got {d1_error}."

    assert d3_error is not None, "No entry for D=3 found."
    assert d3_error == 2.00, f"Expected error for D=3 to be 2.00, got {d3_error}."

def test_best_model_txt():
    """Check if best_model.txt contains the correct value."""
    best_model_path = "/home/user/best_model.txt"
    assert os.path.isfile(best_model_path), f"File {best_model_path} is missing."

    with open(best_model_path, "r") as f:
        content = f.read().strip()

    assert content == "1", f"Expected best_model.txt to contain '1', got '{content}'."