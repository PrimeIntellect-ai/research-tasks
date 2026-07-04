# test_final_state.py

import os
import json
import subprocess
import pytest

def test_c_binary_exists_and_executable():
    path = "/home/user/polyglot/core/compute"
    assert os.path.isfile(path), f"C binary not found at {path}"
    assert os.access(path, os.X_OK), f"C binary at {path} is not executable"

def test_go_binary_exists_and_executable():
    path = "/home/user/polyglot/worker/worker"
    assert os.path.isfile(path), f"Go binary not found at {path}"
    assert os.access(path, os.X_OK), f"Go binary at {path} is not executable"

def test_python_script_exists():
    path = "/home/user/polyglot/build_and_test.py"
    assert os.path.isfile(path), f"Python script not found at {path}"

def test_c_binary_behavior():
    path = "/home/user/polyglot/core/compute"
    # test with N=10, sum of primes <= 10 is 2 + 3 + 5 + 7 = 17
    result = subprocess.run([path, "10"], capture_output=True, text=True)
    assert result.returncode == 0, f"C binary failed with return code {result.returncode}"
    assert result.stdout.strip() == "17", f"Expected '17', got '{result.stdout.strip()}'"

    # test with N=11, sum of primes <= 11 is 17 + 11 = 28
    result2 = subprocess.run([path, "11"], capture_output=True, text=True)
    assert result2.returncode == 0
    assert result2.stdout.strip() == "28", f"Expected '28', got '{result2.stdout.strip()}'"

def test_go_worker_behavior():
    path = "/home/user/polyglot/worker/worker"
    input_data = "[10, 20, 30]"
    result = subprocess.run([path], input=input_data, capture_output=True, text=True)
    assert result.returncode == 0, f"Go worker failed with return code {result.returncode}"

    try:
        output_json = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Go worker output is not valid JSON: {result.stdout}")

    expected_output = {"10": 17, "20": 77, "30": 129}

    # Compare string keys to int values, handling possible type mismatches gracefully
    output_normalized = {str(k): int(v) for k, v in output_json.items()}
    expected_normalized = {str(k): int(v) for k, v in expected_output.items()}

    assert output_normalized == expected_normalized, f"Expected {expected_normalized}, got {output_normalized}"

def test_python_script_execution_and_results():
    path = "/home/user/polyglot/build_and_test.py"
    result = subprocess.run(["python3", path], capture_output=True, text=True)
    assert result.returncode == 0, f"Python script failed with return code {result.returncode}\nstdout: {result.stdout}\nstderr: {result.stderr}"

    results_path = "/home/user/polyglot/test_results.json"
    assert os.path.isfile(results_path), f"Test results JSON not found at {results_path}"

    with open(results_path, "r") as f:
        try:
            results_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("test_results.json is not valid JSON")

    expected_results = {
        "c_build_ok": True,
        "go_build_ok": True,
        "integration_passed": True
    }

    assert results_data == expected_results, f"Expected {expected_results}, got {results_data}"