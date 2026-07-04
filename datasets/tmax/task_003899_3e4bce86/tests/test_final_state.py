# test_final_state.py

import os
import json
import math
import pytest

def test_files_exist():
    """Verify that the required files have been created."""
    required_files = [
        '/home/user/parallel_integrate.py',
        '/home/user/run_study.sh',
        '/home/user/convergence_results.json'
    ]
    for file_path in required_files:
        assert os.path.exists(file_path), f"Required file {file_path} is missing."

def test_convergence_results():
    """Verify the contents of convergence_results.json match the expected mathematical values."""
    json_path = '/home/user/convergence_results.json'
    assert os.path.exists(json_path), "convergence_results.json is missing."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    expected = {}
    for N in [100, 200, 400, 800]:
        val = (1.0 / N**2) * (1.0 / math.tan(math.pi / (2 * N)))**2
        expected[str(N)] = val

    for k, v in expected.items():
        assert k in data, f"Missing key '{k}' in convergence_results.json."
        try:
            actual_val = float(data[k])
        except ValueError:
            pytest.fail(f"Value for key '{k}' is not a valid float.")

        assert abs(actual_val - v) < 1e-10, f"Value for {k} incorrect. Expected {v}, got {actual_val}"