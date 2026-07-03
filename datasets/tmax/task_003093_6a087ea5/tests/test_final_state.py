# test_final_state.py

import os
import json
import csv
import math
import pytest

ORGANIZED_DATA_PATH = '/home/user/data/organized_data.csv'
MODEL_RESULTS_PATH = '/home/user/data/model_results.json'

def test_organized_data_exists_and_format():
    """Test that organized_data.csv exists and has the correct number of rows."""
    assert os.path.exists(ORGANIZED_DATA_PATH), f"Missing cleaned data file at {ORGANIZED_DATA_PATH}"
    assert os.path.isfile(ORGANIZED_DATA_PATH), f"Path {ORGANIZED_DATA_PATH} is not a file"

    with open(ORGANIZED_DATA_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "organized_data.csv is empty"

    header = rows[0]
    # Check that required columns are in the header
    assert 'mass' in header, "Column 'mass' missing from organized_data.csv header"
    assert 'volume' in header, "Column 'volume' missing from organized_data.csv header"
    assert 'class' in header, "Column 'class' missing from organized_data.csv header"

    # The truth data has exactly 200 valid rows
    data_rows = rows[1:]
    assert len(data_rows) == 200, f"Expected exactly 200 data rows, but found {len(data_rows)}"

def test_model_results_json():
    """Test that model_results.json exists and contains the correct keys and values."""
    assert os.path.exists(MODEL_RESULTS_PATH), f"Missing results file at {MODEL_RESULTS_PATH}"
    assert os.path.isfile(MODEL_RESULTS_PATH), f"Path {MODEL_RESULTS_PATH} is not a file"

    with open(MODEL_RESULTS_PATH, 'r', encoding='utf-8') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {MODEL_RESULTS_PATH} is not valid JSON")

    expected_keys = {"best_var_smoothing", "best_cv_score", "cleaned_row_count"}
    actual_keys = set(results.keys())

    missing_keys = expected_keys - actual_keys
    assert not missing_keys, f"Missing keys in model_results.json: {missing_keys}"

    extra_keys = actual_keys - expected_keys
    assert not extra_keys, f"Unexpected extra keys in model_results.json: {extra_keys}"

    # Check cleaned_row_count
    assert isinstance(results["cleaned_row_count"], int), "cleaned_row_count must be an integer"
    assert results["cleaned_row_count"] == 200, f"Expected cleaned_row_count to be 200, got {results['cleaned_row_count']}"

    # Check best_var_smoothing
    assert isinstance(results["best_var_smoothing"], float), "best_var_smoothing must be a float"
    assert math.isclose(results["best_var_smoothing"], 0.1, rel_tol=1e-5), \
        f"Expected best_var_smoothing to be 0.1, got {results['best_var_smoothing']}"

    # Check best_cv_score
    assert isinstance(results["best_cv_score"], float), "best_cv_score must be a float"
    assert math.isclose(results["best_cv_score"], 1.0, rel_tol=1e-5), \
        f"Expected best_cv_score to be 1.0, got {results['best_cv_score']}"