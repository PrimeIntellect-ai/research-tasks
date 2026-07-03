# test_final_state.py

import os
import json
import pytest

def test_results_json_exists_and_correct():
    results_file = "/home/user/results.json"
    assert os.path.isfile(results_file), f"Expected results file {results_file} does not exist."

    with open(results_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_file} is not valid JSON.")

    expected_data = {
        "A.txt": 30,
        "B.txt": 20,
        "C.txt": 10,
        "D.txt": 15,
        "E.txt": 15,
        "F.txt": 100
    }

    for key, expected_value in expected_data.items():
        assert key in data, f"Key '{key}' is missing from {results_file}."
        assert data[key] == expected_value, f"Value for '{key}' is incorrect. Expected {expected_value}, got {data[key]}."

def test_evaluator_go_exists_and_uses_cgo_and_goroutines():
    evaluator_file = "/home/user/evaluator.go"
    assert os.path.isfile(evaluator_file), f"Expected Go program {evaluator_file} does not exist."

    with open(evaluator_file, "r") as f:
        content = f.read()

    assert 'import "C"' in content or 'import (\n\t"C"' in content or 'import (\n\t"fmt"\n\t"C"' in content or '"C"' in content, \
        f"The Go program {evaluator_file} does not appear to import 'C' (cgo)."

    assert 'go ' in content, f"The Go program {evaluator_file} does not appear to use goroutines ('go ' keyword missing)."