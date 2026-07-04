# test_final_state.py

import os
import stat
import subprocess
import requests
import pytest
import math

def test_start_services_script_exists_and_executable():
    script_path = "/home/user/start_services.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable."

def test_regression_test_script_exists():
    script_path = "/home/user/regression_test.py"
    assert os.path.isfile(script_path), f"{script_path} does not exist."

def test_coordinator_run_sim_100_2():
    url = "http://127.0.0.1:5000/run_sim"
    payload = {"N": 100, "workers": 2}
    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to coordinator at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    data = response.json()
    assert isinstance(data, list), "Expected a JSON array response"
    assert len(data) == 100, f"Expected length 100, got {len(data)}"

    expected = [math.sin(i * 0.1) for i in range(100)]
    for i, (val, exp) in enumerate(zip(data, expected)):
        assert abs(val - exp) < 1e-5, f"Mismatch at index {i}: expected {exp}, got {val}"

def test_regression_test_execution():
    script_path = "/home/user/regression_test.py"
    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"regression_test.py failed with return code {result.returncode}\nstderr: {result.stderr}"
    assert "REGRESSION_PASSED" in result.stdout, f"Expected 'REGRESSION_PASSED' in stdout, got: {result.stdout}"

def test_coordinator_run_sim_105_4():
    url = "http://127.0.0.1:5000/run_sim"
    payload = {"N": 105, "workers": 4}
    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to coordinator at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    data = response.json()
    assert isinstance(data, list), "Expected a JSON array response"
    assert len(data) == 105, f"Expected length 105, got {len(data)}"

    expected = [math.sin(i * 0.1) for i in range(105)]
    for i, (val, exp) in enumerate(zip(data, expected)):
        assert abs(val - exp) < 1e-5, f"Mismatch at index {i}: expected {exp}, got {val}"