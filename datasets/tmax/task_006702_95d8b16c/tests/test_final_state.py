# test_final_state.py
import os
import json
import pytest

def test_ttest_pvalue_file():
    file_path = "/home/user/ttest_pvalue.txt"
    assert os.path.exists(file_path), f"File {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    # The p-value for this specific dataset and test is extremely small
    # It should be rounded to 4 decimal places, so "0.0000"
    assert content == "0.0000", f"Expected '0.0000' in {file_path}, but found '{content}'."

def test_best_params_file():
    file_path = "/home/user/best_params.json"
    assert os.path.exists(file_path), f"File {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    with open(file_path, 'r') as f:
        try:
            params = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{file_path} does not contain valid JSON.")

    assert isinstance(params, dict), f"Expected JSON object in {file_path}."
    assert "max_depth" in params, f"'max_depth' missing from {file_path}."
    assert "n_estimators" in params, f"'n_estimators' missing from {file_path}."

    # Check if the values are within the grid
    assert params["max_depth"] in [None, 5, 10], f"Invalid max_depth: {params['max_depth']}"
    assert params["n_estimators"] in [50, 100], f"Invalid n_estimators: {params['n_estimators']}"

def test_best_cv_score_file():
    file_path = "/home/user/best_cv_score.txt"
    assert os.path.exists(file_path), f"File {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    try:
        score = float(content)
    except ValueError:
        pytest.fail(f"{file_path} does not contain a valid float.")

    assert 0.0 <= score <= 1.0, f"CV score {score} is out of bounds [0.0, 1.0]."

    # Check if it has exactly 4 decimal places
    parts = content.split('.')
    assert len(parts) == 2, f"Expected decimal point in {file_path}."
    assert len(parts[1]) == 4, f"Expected exactly 4 decimal places in {file_path}, found {len(parts[1])}."