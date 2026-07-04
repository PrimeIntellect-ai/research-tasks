# test_final_state.py

import os
import json
import subprocess

def test_build_system_script_exists():
    path = "/home/user/build_system.py"
    assert os.path.isfile(path), f"File {path} does not exist."

def test_generated_c_file_exists():
    path = "/home/user/impl.c"
    assert os.path.isfile(path), f"File {path} does not exist."

def test_generated_py_file_exists():
    path = "/home/user/impl.py"
    assert os.path.isfile(path), f"File {path} does not exist."

def test_executable_exists():
    path = "/home/user/impl_bin"
    assert os.path.isfile(path), f"Executable {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_validation_json_correct():
    path = "/home/user/validation.json"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {path} does not contain valid JSON."

    expected_data = {
        "ALPHA": 49,
        "BETA": 83,
        "c_results": [35, -7, -37, -49, -37],
        "py_results": [35, -7, -37, -49, -37],
        "match": True
    }

    for key in expected_data:
        assert key in data, f"Key '{key}' missing from validation.json."
        assert data[key] == expected_data[key], f"Value for '{key}' in validation.json is incorrect. Expected {expected_data[key]}, got {data[key]}."

def test_c_executable_functionality():
    path = "/home/user/impl_bin"
    expected_results = [35, -7, -37, -49, -37]

    for i, x in enumerate(range(1, 6)):
        result = subprocess.run([path, str(x)], capture_output=True, text=True)
        assert result.returncode == 0, f"Running {path} {x} failed."
        try:
            output_val = int(result.stdout.strip())
        except ValueError:
            assert False, f"Output of {path} {x} is not an integer: '{result.stdout.strip()}'"

        assert output_val == expected_results[i], f"Expected {path} {x} to output {expected_results[i]}, got {output_val}."