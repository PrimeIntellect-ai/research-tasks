# test_final_state.py

import os
import json
import csv
import pytest

def test_clean_obs_csv():
    """Test that clean_obs.csv is correctly extracted for subject 42."""
    file_path = "/home/user/clean_obs.csv"
    assert os.path.exists(file_path), f"File missing: {file_path}"

    with open(file_path, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "clean_obs.csv is empty."
    assert rows[0] == ["time", "B_conc"], f"Incorrect header in clean_obs.csv: {rows[0]}"

    # Check that it has 11 data rows (from t=0 to t=10)
    assert len(rows) == 12, f"Expected 1 header + 11 data rows, got {len(rows)} total rows."

    # Check first row of data
    assert float(rows[1][0]) == 0.0, "First time point should be 0."

def test_best_params_json():
    """Test that best_params.json contains valid k1 and k2."""
    file_path = "/home/user/best_params.json"
    assert os.path.exists(file_path), f"File missing: {file_path}"

    with open(file_path, "r") as f:
        try:
            params = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("best_params.json is not valid JSON.")

    assert "k1" in params, "Missing 'k1' in best_params.json"
    assert "k2" in params, "Missing 'k2' in best_params.json"

    k1 = float(params["k1"])
    k2 = float(params["k2"])

    assert 0.34 < k1 < 0.37, f"k1 value {k1} is outside the expected range (0.34 - 0.37)"
    assert 0.73 < k2 < 0.78, f"k2 value {k2} is outside the expected range (0.73 - 0.78)"

def test_best_fit_curve_csv():
    """Test that best_fit_curve.csv exists and has correct headers."""
    file_path = "/home/user/best_fit_curve.csv"
    assert os.path.exists(file_path), f"File missing: {file_path}"

    with open(file_path, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "best_fit_curve.csv is empty."
    assert rows[0] == ["time", "B_num"], f"Incorrect header in best_fit_curve.csv: {rows[0]}"
    assert len(rows) == 12, f"Expected 1 header + 11 data rows, got {len(rows)} total rows."

def test_validation_result_txt():
    """Test that validation_result.txt contains the correct output."""
    file_path = "/home/user/validation_result.txt"
    assert os.path.exists(file_path), f"File missing: {file_path}"

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in validation_result.txt, got {len(lines)}"
    assert lines[0] == "VALID", f"Expected first line to be 'VALID', got '{lines[0]}'"
    assert lines[1] == "FAST", f"Expected second line to be 'FAST', got '{lines[1]}'"