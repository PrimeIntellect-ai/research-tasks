# test_final_state.py

import os
import json
import pytest

def test_best_model_json():
    """Test that best_model.json exists and has the correct structure and valid values."""
    file_path = "/home/user/best_model.json"
    assert os.path.isfile(file_path), f"Missing file: {file_path}"

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not valid JSON.")

    assert "best_params" in data, "JSON missing 'best_params' key."
    assert "cv_score" in data, "JSON missing 'cv_score' key."

    best_params = data["best_params"]
    assert isinstance(best_params, dict), "'best_params' should be a dictionary."

    expected_keys = {"classifier__n_estimators", "classifier__max_depth"}
    assert expected_keys.issubset(set(best_params.keys())), f"'best_params' missing expected keys. Found: {list(best_params.keys())}"

    n_estimators = best_params["classifier__n_estimators"]
    max_depth = best_params["classifier__max_depth"]

    assert n_estimators in [50, 100], f"Invalid value for classifier__n_estimators: {n_estimators}"
    assert max_depth in [5, 10, None], f"Invalid value for classifier__max_depth: {max_depth}"

    cv_score = data["cv_score"]
    assert isinstance(cv_score, (float, int)), "'cv_score' must be a number."
    assert 0.0 <= cv_score <= 1.0, f"'cv_score' is out of expected bounds [0, 1]: {cv_score}"

def test_p_value_txt():
    """Test that p_value.txt exists and contains a valid probability value."""
    file_path = "/home/user/p_value.txt"
    assert os.path.isfile(file_path), f"Missing file: {file_path}"

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content, f"File {file_path} is empty."

    try:
        p_value = float(content)
    except ValueError:
        pytest.fail(f"Content of {file_path} is not a valid float: {content}")

    assert 0.0 <= p_value <= 1.0, f"p-value out of bounds [0, 1]: {p_value}"

    # Check if it's rounded to 4 decimal places (allow some flexibility for trailing zeros)
    parts = content.split('.')
    if len(parts) == 2:
        assert len(parts[1]) <= 4, f"p-value should be rounded to 4 decimal places, found: {content}"