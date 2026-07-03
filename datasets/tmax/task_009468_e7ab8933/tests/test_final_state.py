# test_final_state.py

import os
import json
import pytest

def test_cpp_file_exists():
    cpp_file = "/home/user/shortest_path.cpp"
    assert os.path.isfile(cpp_file), f"C++ source file {cpp_file} is missing."

def test_output_json_exists_and_correct():
    output_json = "/home/user/output.json"
    assert os.path.isfile(output_json), f"Output file {output_json} is missing. Did you compile and run your program?"

    with open(output_json, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{output_json} does not contain valid JSON.")

    assert "path" in data, "JSON output is missing the 'path' key."
    assert "total_weight" in data, "JSON output is missing the 'total_weight' key."

    expected_path = ["A", "F", "G", "Z"]
    expected_weight = 11

    assert data["path"] == expected_path, f"Expected path {expected_path}, but got {data['path']}."
    assert data["total_weight"] == expected_weight, f"Expected total_weight {expected_weight}, but got {data['total_weight']}."