# test_final_state.py

import os
import json
import math
import pytest

REPORT_PATH = '/home/user/analysis_report.json'

def test_analysis_report_exists():
    """Check if the analysis report JSON file was created."""
    assert os.path.exists(REPORT_PATH), f"File not found: {REPORT_PATH}"
    assert os.path.isfile(REPORT_PATH), f"Path is not a file: {REPORT_PATH}"

def test_analysis_report_format():
    """Verify that the JSON file contains the correct keys and types."""
    with open(REPORT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} is not valid JSON.")

    expected_keys = {"p_value", "best_max_depth", "best_cv_accuracy"}
    assert set(data.keys()) == expected_keys, f"JSON keys must be exactly {expected_keys}, but got {set(data.keys())}"

    assert isinstance(data["p_value"], float), "p_value must be a float"
    assert data["best_max_depth"] is None or isinstance(data["best_max_depth"], int), "best_max_depth must be an integer or null"
    assert isinstance(data["best_cv_accuracy"], float), "best_cv_accuracy must be a float"

def test_analysis_report_values():
    """Verify the computed metrics are correct based on the deterministic dataset."""
    with open(REPORT_PATH, 'r') as f:
        data = json.load(f)

    p_val = data["p_value"]
    best_max_depth = data["best_max_depth"]
    best_cv_acc = data["best_cv_accuracy"]

    # The expected p-value is approximately 1.22e-15
    assert p_val < 1e-10, f"p_value {p_val} is too high. Expected a very small value (~1.22e-15)."
    assert p_val > 0, f"p_value {p_val} cannot be zero or negative."

    # The expected best max_depth is 3
    assert best_max_depth == 3, f"best_max_depth is {best_max_depth}, expected 3."

    # The expected cross-validation accuracy is approximately 0.762
    assert 0.70 < best_cv_acc < 0.85, f"best_cv_accuracy {best_cv_acc} is out of expected range (~0.762)."