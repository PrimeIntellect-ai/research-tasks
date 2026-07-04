# test_final_state.py

import os
import json
import subprocess
import pytest

def test_logparser_binary_exists_and_executable():
    binary_path = "/home/user/release/logparser"
    assert os.path.isfile(binary_path), f"Binary {binary_path} does not exist. Did you run make?"
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_logparser_linked_with_math_lib():
    binary_path = "/home/user/release/logparser"
    assert os.path.isfile(binary_path), f"Binary {binary_path} does not exist."

    try:
        output = subprocess.check_output(["ldd", binary_path], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run ldd on {binary_path}: {e.output}")

    assert "libm." in output, "The logparser binary is not linked with the math library (-lm)."

def test_c_source_bug_fixed():
    c_file_path = "/home/user/release/logparser.c"
    assert os.path.isfile(c_file_path), f"File {c_file_path} is missing."

    with open(c_file_path, "r") as f:
        content = f.read()

    assert "/tmp/scratch.tmp" not in content, "The hardcoded temporary file path '/tmp/scratch.tmp' is still present in logparser.c."

def test_test_results_json_correct():
    json_path = "/home/user/test_results.json"
    assert os.path.isfile(json_path), f"The results file {json_path} does not exist. Did you run the Go orchestrator?"

    try:
        with open(json_path, "r") as f:
            results = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {json_path} does not contain valid JSON.")

    expected_results = {
        "app_01.txt": 1,
        "app_02.txt": 3,
        "app_03.txt": 0,
        "app_04.txt": 2,
        "app_05.txt": 4
    }

    assert isinstance(results, dict), f"The JSON in {json_path} should be an object (dictionary)."

    for key, expected_val in expected_results.items():
        assert key in results, f"Key '{key}' is missing from the JSON results."
        assert results[key] == expected_val, f"Expected {expected_val} errors for {key}, but got {results[key]}."

    # Also check that there are no unexpected keys
    for key in results.keys():
        assert key in expected_results, f"Unexpected key '{key}' found in the JSON results."