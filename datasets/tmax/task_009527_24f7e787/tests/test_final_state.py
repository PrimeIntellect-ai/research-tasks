# test_final_state.py

import os
import json
import pytest

def test_cycles_output_exists_and_correct():
    output_path = "/home/user/cycles_output.json"
    assert os.path.exists(output_path), f"File {output_path} is missing. Did the C++ program run successfully?"
    assert os.path.isfile(output_path), f"{output_path} is not a file."

    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{output_path} does not contain valid JSON.")

    assert "cycles" in data, f"Key 'cycles' missing from {output_path}."

    expected_cycles = [
        ["DS_A", "DS_B", "DS_C"],
        ["DS_E", "DS_F", "DS_G"]
    ]

    assert data["cycles"] == expected_cycles, (
        f"The cycles in {output_path} do not match the expected output. "
        f"Expected {expected_cycles}, but got {data['cycles']}."
    )

def test_cpp_artifacts_exist():
    cpp_file = "/home/user/find_cycles.cpp"
    executable = "/home/user/find_cycles"

    assert os.path.exists(cpp_file), f"C++ source file {cpp_file} is missing."
    assert os.path.exists(executable), f"Compiled executable {executable} is missing."
    assert os.access(executable, os.X_OK), f"{executable} is not executable."