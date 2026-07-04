# test_final_state.py

import os
import json
import pytest

REPORT_PATH = "/home/user/report.json"
TRUTH_PATH = "/home/user/truth.json"

def test_report_exists():
    assert os.path.isfile(REPORT_PATH), f"The file {REPORT_PATH} does not exist. Did you save your output to the correct path?"

def test_report_structure():
    assert os.path.isfile(REPORT_PATH), f"Missing {REPORT_PATH}"
    with open(REPORT_PATH, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{REPORT_PATH} is not a valid JSON file.")

    assert "best_alpha" in report, "Missing 'best_alpha' key in report.json."
    assert "most_similar_pair" in report, "Missing 'most_similar_pair' key in report.json."
    assert "test_predictions" in report, "Missing 'test_predictions' key in report.json."

    assert isinstance(report["most_similar_pair"], list), "'most_similar_pair' must be a list."
    assert len(report["most_similar_pair"]) == 2, "'most_similar_pair' must contain exactly two experiment IDs."
    assert isinstance(report["test_predictions"], dict), "'test_predictions' must be a dictionary."

def test_report_values():
    assert os.path.isfile(REPORT_PATH), f"Missing {REPORT_PATH}"
    assert os.path.isfile(TRUTH_PATH), f"Missing {TRUTH_PATH}"

    with open(REPORT_PATH, "r") as f:
        report = json.load(f)

    with open(TRUTH_PATH, "r") as f:
        truth = json.load(f)

    # Check best alpha
    assert report["best_alpha"] == truth["best_alpha"], \
        f"Incorrect 'best_alpha'. Expected {truth['best_alpha']}, got {report.get('best_alpha')}."

    # Check most similar pair
    expected_pair = sorted(truth["most_similar_pair"])
    actual_pair = sorted(report.get("most_similar_pair", []))
    assert actual_pair == expected_pair, \
        f"Incorrect 'most_similar_pair'. Expected {expected_pair}, got {actual_pair}."

    # Check test predictions
    expected_preds = truth["test_predictions"]
    actual_preds = report.get("test_predictions", {})

    assert len(actual_preds) == len(expected_preds), \
        f"Expected {len(expected_preds)} test predictions, got {len(actual_preds)}."

    for exp_id, expected_val in expected_preds.items():
        assert exp_id in actual_preds, f"Missing prediction for test experiment: {exp_id}."
        actual_val = actual_preds[exp_id]
        assert isinstance(actual_val, (int, float)), f"Prediction for {exp_id} must be a number."
        assert abs(actual_val - expected_val) <= 1e-3, \
            f"Prediction for {exp_id} is incorrect. Expected {expected_val}, got {actual_val}."