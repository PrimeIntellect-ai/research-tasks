# test_final_state.py

import os
import subprocess
import json
import math
import pytest
import requests

def test_binary_compiled_and_reproducible():
    binary_path = "/app/graph-sim-1.0/bin/simulate_graph"
    assert os.path.isfile(binary_path), f"Compiled binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary at {binary_path} is not executable"

    # Run the binary multiple times to ensure deterministic output
    outputs = []
    for _ in range(5):
        result = subprocess.run([binary_path, "/app/molecule_graph.dat"], capture_output=True, text=True)
        assert result.returncode == 0, "Binary execution failed"
        outputs.append(result.stdout)

    # Check reproducibility
    for i in range(1, 5):
        assert outputs[0] == outputs[i], "Binary output is not deterministic across runs. The OpenMP reduction issue was not fixed properly."

def test_api_server_responses():
    binary_path = "/app/graph-sim-1.0/bin/simulate_graph"
    # Get the deterministic output
    result = subprocess.run([binary_path, "/app/molecule_graph.dat"], capture_output=True, text=True)
    lines = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
    values = [float(x) for x in lines]

    # Calculate expected mean and std
    n = len(values)
    sim_mean = sum(values) / n
    sim_std = math.sqrt(sum((x - sim_mean) ** 2 for x in values) / n)  # Population std

    # Read reference data
    ref_path = "/app/reference_data.csv"
    with open(ref_path, "r") as f:
        ref_line = f.read().strip()
    ref_mean_str, ref_std_str = ref_line.split(',')
    ref_mean = float(ref_mean_str)
    ref_std = float(ref_std_str)

    diff_mean = sim_mean - ref_mean
    diff_std = sim_std - ref_std

    expected_json = {
        "sim_mean": round(sim_mean, 4),
        "sim_std": round(sim_std, 4),
        "diff_mean": round(diff_mean, 4),
        "diff_std": round(diff_std, 4)
    }

    url = "http://127.0.0.1:9090/simulate"

    # Test without API key
    try:
        resp_no_auth = requests.post(url, timeout=2)
        assert resp_no_auth.status_code in [400, 401, 403], f"Expected 4xx status code when missing API key, got {resp_no_auth.status_code}"
    except requests.exceptions.ConnectionError:
        pytest.fail("API server is not running or not reachable on 127.0.0.1:9090")

    # Test with correct API key
    headers = {"X-API-Key": "moleculardynamics42"}
    resp = requests.post(url, headers=headers, timeout=5)

    assert resp.status_code == 200, f"Expected HTTP 200 OK, got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"API did not return valid JSON. Response text: {resp.text}")

    for key in expected_json:
        assert key in data, f"Missing key '{key}' in JSON response"
        # Allow small floating point differences due to rounding implementations, but rounding to 4 decimal places should be exact or very close
        assert math.isclose(data[key], expected_json[key], abs_tol=1e-4), \
            f"Value for {key} mismatch. Expected approx {expected_json[key]}, got {data[key]}"