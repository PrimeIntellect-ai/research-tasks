# test_final_state.py
import os
import json
import pytest

WORKSPACE_DIR = "/home/user/workspace"
METRICS_JSON = os.path.join(WORKSPACE_DIR, "metrics.json")

def test_metrics_json_exists():
    assert os.path.isfile(METRICS_JSON), f"Expected file {METRICS_JSON} to be generated, but it does not exist. Did you run the Go pipeline?"

def test_metrics_json_content():
    assert os.path.isfile(METRICS_JSON), f"{METRICS_JSON} is missing."

    with open(METRICS_JSON, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{METRICS_JSON} does not contain valid JSON.")

    assert "total_rows_processed" in data, "Key 'total_rows_processed' is missing from metrics.json."
    assert "evaluation_score" in data, "Key 'evaluation_score' is missing from metrics.json."

    expected_rows = 5
    actual_rows = data["total_rows_processed"]
    assert actual_rows == expected_rows, f"Expected {expected_rows} rows processed, got {actual_rows}. The bug dropping empty category_id rows might not be fixed correctly."

    expected_score = 12.8
    actual_score = data["evaluation_score"]
    assert isinstance(actual_score, (int, float)), f"Expected 'evaluation_score' to be a number, got {type(actual_score).__name__}."
    assert abs(actual_score - expected_score) < 1e-5, f"Expected evaluation_score to be {expected_score}, got {actual_score}. Check the ComputeEmbedding and Evaluate implementations."