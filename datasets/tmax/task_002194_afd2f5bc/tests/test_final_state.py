# test_final_state.py
import os
import requests
import math

def test_initial_state_file():
    file_path = '/home/user/initial_state.txt'
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, 'r') as f:
        lines = f.readlines()

    assert len(lines) == 64, f"Expected 64 lines in {file_path}, got {len(lines)}"

    total_sum = 0.0
    for i, line in enumerate(lines):
        parts = line.strip().split()
        assert len(parts) == 64, f"Expected 64 values on line {i+1}, got {len(parts)}"
        for val in parts:
            total_sum += float(val)

    # The sum should be exactly 100.0 based on truth, allow small tolerance
    assert math.isclose(total_sum, 100.0, rel_tol=0.05), f"Expected initial sum to be around 100.0, got {total_sum}"

def test_simulate_c_exists():
    file_path = '/home/user/simulate.c'
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

def test_http_service():
    url = "http://127.0.0.1:8080/simulate"
    payload = {"t_end": 10.0}

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the HTTP service at {url}: {e}"

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        assert False, f"Response is not valid JSON: {response.text}"

    assert "sum" in data, f"Response JSON missing 'sum' key: {data}"

    sim_sum = float(data["sum"])
    # The sum should be conserved and remain around 100.0
    assert math.isclose(sim_sum, 100.0, rel_tol=0.05), f"Expected sum to be conserved around 100.0, got {sim_sum}"

def test_http_service_different_time():
    url = "http://127.0.0.1:8080/simulate"
    payload = {"t_end": 50.0}

    try:
        response = requests.post(url, json=payload, timeout=10)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the HTTP service at {url}: {e}"

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "sum" in data, f"Response JSON missing 'sum' key: {data}"

    sim_sum = float(data["sum"])
    assert math.isclose(sim_sum, 100.0, rel_tol=0.05), f"Expected sum to be conserved around 100.0 even for larger t_end, got {sim_sum}"