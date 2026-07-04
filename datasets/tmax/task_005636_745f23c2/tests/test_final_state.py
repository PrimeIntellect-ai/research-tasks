# test_final_state.py

import os
import json
import pytest

def test_c_file_exists():
    c_file_path = "/home/user/graph_query.c"
    assert os.path.exists(c_file_path), f"The required C source file was not found at {c_file_path}"
    assert os.path.isfile(c_file_path), f"The path {c_file_path} is not a file."

def test_results_json_exists_and_correct():
    json_file_path = "/home/user/results.json"
    assert os.path.exists(json_file_path), f"The results file was not found at {json_file_path}"
    assert os.path.isfile(json_file_path), f"The path {json_file_path} is not a file."

    with open(json_file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_file_path} does not contain valid JSON.")

    expected_data = ["metadata", "products", "sessions"]
    assert isinstance(data, list), "The JSON result must be a list (array)."
    assert data == expected_data, f"The JSON result does not match the expected output. Expected {expected_data}, got {data}."