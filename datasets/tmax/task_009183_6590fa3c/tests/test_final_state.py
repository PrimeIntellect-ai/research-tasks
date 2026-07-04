# test_final_state.py

import os
import json
import pytest

def test_recovery_info():
    target_hash_path = "/tmp/target_hash.txt"
    recovery_info_path = "/home/user/recovery_info.txt"

    assert os.path.isfile(target_hash_path), f"Truth file {target_hash_path} is missing."
    assert os.path.isfile(recovery_info_path), f"Student output file {recovery_info_path} is missing."

    with open(target_hash_path, "r") as f:
        expected_hash = f.read().strip()

    with open(recovery_info_path, "r") as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"Expected commit hash {expected_hash}, but found {actual_hash} in {recovery_info_path}"

def test_results_json():
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"Results file {results_path} is missing."

    try:
        with open(results_path, "r") as f:
            # The prompt says "a single valid JSON object mapping each filename...".
            # If the student just redirected multiple JSONs, it might fail to parse as a single object.
            # We must parse it as a single JSON object.
            content = f.read().strip()
            # If the student produced multiple JSON objects, we should try to parse them or fail.
            # The prompt explicitly asks for "a single valid JSON object mapping each filename".
            results = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"File {results_path} does not contain a single valid JSON object.")

    assert "sensor_A.csv" in results, "'sensor_A.csv' missing from results.json"
    assert "sensor B.csv" in results, "'sensor B.csv' missing from results.json"

    sensor_a = results["sensor_A.csv"]
    assert "mean" in sensor_a and "variance" in sensor_a, "Missing mean or variance for sensor_A.csv"
    assert abs(sensor_a["mean"] - 3.0) < 1e-6, f"Incorrect mean for sensor_A.csv: {sensor_a['mean']}"
    assert abs(sensor_a["variance"] - 2.0) < 1e-6, f"Incorrect variance for sensor_A.csv: {sensor_a['variance']}"

    sensor_b = results["sensor B.csv"]
    assert "mean" in sensor_b and "variance" in sensor_b, "Missing mean or variance for sensor B.csv"
    assert abs(sensor_b["mean"] - 10000000001.0) < 1e-6, f"Incorrect mean for sensor B.csv: {sensor_b['mean']}"

    variance_b = sensor_b["variance"]
    assert 0.65 < variance_b < 0.67, f"Variance for sensor B.csv is out of expected range (0.65 - 0.67): {variance_b}. Did you fix the numerical instability?"