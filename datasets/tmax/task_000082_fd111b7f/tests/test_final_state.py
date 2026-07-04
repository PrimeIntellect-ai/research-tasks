# test_final_state.py

import os
import json
import pytest

def test_cpp_file_exists():
    cpp_path = "/home/user/fit_model.cpp"
    assert os.path.isfile(cpp_path), f"The C++ source file is missing at {cpp_path}"

def test_results_json_exists_and_valid():
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"The results file is missing at {results_path}"

    with open(results_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file at {results_path} is not valid JSON.")

    assert "p1" in data, "The results.json file is missing the 'p1' key."
    assert "p2" in data, "The results.json file is missing the 'p2' key."
    assert "sse" in data, "The results.json file is missing the 'sse' key."

    p1 = data["p1"]
    p2 = data["p2"]
    sse = data["sse"]

    assert isinstance(p1, (int, float)), f"'p1' must be a number, got {type(p1)}"
    assert isinstance(p2, (int, float)), f"'p2' must be a number, got {type(p2)}"
    assert isinstance(sse, (int, float)), f"'sse' must be a number, got {type(sse)}"

    assert 1.9 <= p1 <= 2.1, f"p1 out of bounds: {p1}. Expected between 1.9000 and 2.1000."
    assert 3.9 <= p2 <= 4.1, f"p2 out of bounds: {p2}. Expected between 3.9000 and 4.1000."
    assert sse < 0.05, f"sse too high: {sse}. Expected less than 0.05."