# test_final_state.py

import os
import json
import pytest

def test_fit_comparison_png_exists():
    file_path = "/home/user/fit_comparison.png"
    assert os.path.exists(file_path), f"The plot file {file_path} does not exist."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_model_params_json_exists():
    file_path = "/home/user/model_params.json"
    assert os.path.exists(file_path), f"The parameters file {file_path} does not exist."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_model_params_content():
    file_path = "/home/user/model_params.json"
    assert os.path.exists(file_path), f"The parameters file {file_path} does not exist."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {file_path} is not a valid JSON file.")

    expected = {"omega": 15.0, "c": 0.8, "k": 25.0, "F": 3.5}
    tolerances = {"omega": 0.5, "c": 0.2, "k": 1.0, "F": 0.5}

    for key in expected:
        assert key in data, f"Missing key '{key}' in {file_path}."

        val = data[key]
        assert isinstance(val, (int, float)), f"Value for '{key}' must be a number, got {type(val)}."

        diff = abs(val - expected[key])
        assert diff <= tolerances[key], (
            f"Value for '{key}' is out of bounds. "
            f"Expected ~{expected[key]} (\u00b1{tolerances[key]}), got {val}."
        )