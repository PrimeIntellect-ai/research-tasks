# test_final_state.py

import os
import subprocess
import json
import math
import pytest
import requests

def test_venv_exists():
    """Verify that the virtual environment was created correctly."""
    venv_dir = "/home/user/venv"
    python_bin = os.path.join(venv_dir, "bin", "python")

    assert os.path.isdir(venv_dir), f"Virtual environment directory {venv_dir} does not exist."
    assert os.path.isfile(python_bin), f"Python executable not found at {python_bin}."

def test_solve_endpoint_correctness():
    """Verify the /solve endpoint returns the mathematically exact solution."""
    # Compute the expected result using the student's virtual environment
    # This avoids relying on globally installed scientific libraries in the test runner.
    compute_script = """
import h5py
import numpy as np
import json

try:
    with h5py.File('/app/spectro_data.h5', 'r') as f:
        M = f['spectroscopy/raw'][:]
        b = f['spectroscopy/vector'][:]

    U, S, Vt = np.linalg.svd(M, full_matrices=False)
    S_filtered = np.zeros_like(S)
    S_filtered[:3] = S[:3]
    M_filtered = U @ np.diag(S_filtered) @ Vt

    x, _, _, _ = np.linalg.lstsq(M_filtered, b, rcond=None)
    print(json.dumps(x.tolist()))
except Exception as e:
    import sys
    sys.exit(str(e))
"""
    python_bin = "/home/user/venv/bin/python"

    try:
        result = subprocess.run(
            [python_bin, "-c", compute_script],
            capture_output=True, text=True, check=True
        )
        expected_x = json.loads(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to compute expected result using student's venv. Ensure numpy and h5py are installed. Error: {e.stderr}")
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse the expected result from the compute script. Output: {result.stdout}")

    # Query the student's API
    try:
        response = requests.get("http://127.0.0.1:8082/solve", timeout=10)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the processing API on port 8082. Is the service running? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        actual_x = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert isinstance(actual_x, list), f"Expected a JSON list of floats, got {type(actual_x).__name__}."
    assert len(actual_x) == len(expected_x), f"Expected list of length {len(expected_x)}, got {len(actual_x)}."

    # Compare values with a small numerical tolerance
    for i, (act, exp) in enumerate(zip(actual_x, expected_x)):
        assert isinstance(act, (int, float)), f"Element at index {i} is not a number: {act}"
        assert math.isclose(act, exp, rel_tol=1e-4, abs_tol=1e-5), \
            f"Mismatch at index {i}: expected {exp}, got {act}"