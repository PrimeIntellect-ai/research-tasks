# test_final_state.py

import os
import json
import pytest

CLEANED_DATA_PATH = '/home/user/results/cleaned_data.csv'
SUMMARY_JSON_PATH = '/home/user/results/summary.json'

def test_cleaned_data_exists_and_has_correct_rows():
    """Verify that the cleaned_data.csv exists and has exactly 501 lines (header + 500 rows)."""
    assert os.path.exists(CLEANED_DATA_PATH), f"Cleaned data CSV missing at {CLEANED_DATA_PATH}."

    with open(CLEANED_DATA_PATH, 'r') as f:
        lines = f.readlines()

    assert len(lines) == 501, f"Expected 501 lines (1 header + 500 data rows) in {CLEANED_DATA_PATH}, got {len(lines)}."

def test_summary_json_exists_and_valid():
    """Verify that summary.json exists and is valid JSON."""
    assert os.path.exists(SUMMARY_JSON_PATH), f"Summary JSON missing at {SUMMARY_JSON_PATH}."

    with open(SUMMARY_JSON_PATH, 'r') as f:
        try:
            json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {SUMMARY_JSON_PATH} is not valid JSON.")

def test_summary_json_contents():
    """Verify the contents of summary.json match the expected values."""
    with open(SUMMARY_JSON_PATH, 'r') as f:
        summary = json.load(f)

    expected_keys = {"num_rows_cleaned", "model_accuracy", "avg_inference_ms"}
    assert set(summary.keys()) == expected_keys, f"summary.json keys mismatch. Expected {expected_keys}, got {set(summary.keys())}."

    # Check num_rows_cleaned
    assert summary['num_rows_cleaned'] == 500, f"Expected num_rows_cleaned to be 500, got {summary['num_rows_cleaned']}."

    # Check model_accuracy
    # Random Forest without max_depth perfectly overfits to the training data.
    accuracy = summary['model_accuracy']
    assert isinstance(accuracy, (int, float)), "model_accuracy must be a number."
    assert round(accuracy, 2) == 1.0, f"Expected model_accuracy ~1.0, got {accuracy}."

    # Check avg_inference_ms
    avg_inference_ms = summary['avg_inference_ms']
    assert isinstance(avg_inference_ms, float), f"avg_inference_ms must be a float, got {type(avg_inference_ms).__name__}."
    assert avg_inference_ms > 0.0, f"avg_inference_ms must be greater than 0, got {avg_inference_ms}."