# test_final_state.py
import os
import json
import pytest

def test_c_source_file_exists():
    file_path = "/home/user/knn_cv.c"
    assert os.path.isfile(file_path), f"C source file {file_path} is missing."

def test_json_output_exists():
    file_path = "/home/user/best_model.json"
    assert os.path.isfile(file_path), f"Output JSON file {file_path} is missing."

def test_json_output_content():
    file_path = "/home/user/best_model.json"
    assert os.path.isfile(file_path), f"Output JSON file {file_path} is missing."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} does not contain valid JSON.")

    assert "best_k" in data, "JSON output is missing 'best_k' key."
    assert "best_mae" in data, "JSON output is missing 'best_mae' key."

    expected_best_k = 4
    expected_best_mae = 1.42

    assert data["best_k"] == expected_best_k, f"Expected best_k to be {expected_best_k}, got {data['best_k']}."

    mae = data["best_mae"]
    assert isinstance(mae, (int, float)), f"Expected best_mae to be a number, got {type(mae)}."
    assert abs(mae - expected_best_mae) <= 0.02, f"Expected best_mae to be approx {expected_best_mae}, got {mae}."