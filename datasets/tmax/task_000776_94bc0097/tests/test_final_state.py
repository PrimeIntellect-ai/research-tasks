# test_final_state.py

import os
import json
import pytest

def test_venv_exists():
    venv_python = "/home/user/venv/bin/python"
    assert os.path.isfile(venv_python), f"Virtual environment python not found at {venv_python}. Make sure you created the venv at /home/user/venv."

def test_report_exists():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"Report file not found at {report_path}."

def test_report_content():
    report_path = "/home/user/report.json"
    if not os.path.isfile(report_path):
        pytest.fail(f"Report file {report_path} is missing.")

    with open(report_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The report.json file is not valid JSON.")

    expected_keys = {"pearson_correlation", "mse", "most_similar_to_0"}
    missing_keys = expected_keys - set(results.keys())
    assert not missing_keys, f"Report is missing required keys: {missing_keys}"

    assert isinstance(results["pearson_correlation"], (float, int)), "pearson_correlation must be a float"
    assert isinstance(results["mse"], (float, int)), "mse must be a float"
    assert isinstance(results["most_similar_to_0"], str), "most_similar_to_0 must be a string"

def test_most_similar_dataset():
    report_path = "/home/user/report.json"
    if not os.path.isfile(report_path):
        pytest.fail(f"Report file {report_path} is missing.")

    with open(report_path, 'r') as f:
        results = json.load(f)

    actual_similar = results.get("most_similar_to_0")
    assert actual_similar == "dataset_10", f"Expected most_similar_to_0 to be 'dataset_10', but got '{actual_similar}'."