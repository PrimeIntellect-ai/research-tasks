# test_final_state.py
import os
import requests
import pytest
import math

def get_fasta_length(filepath, prot_id):
    if not os.path.exists(filepath):
        pytest.fail(f"FASTA file missing at {filepath}")
    with open(filepath, 'r') as f:
        lines = f.readlines()
    in_seq = False
    seq = ""
    for line in lines:
        line = line.strip()
        if line.startswith(">"):
            if line[1:] == prot_id:
                in_seq = True
            else:
                if in_seq:
                    break
        elif in_seq:
            seq += line
    return len(seq)

def test_server_log_exists():
    log_path = '/home/user/server_started.log'
    assert os.path.exists(log_path), f"Log file {log_path} does not exist. Did you create it?"

def test_api_unauthorized():
    url = "http://127.0.0.1:8080/api/protein/P12345/validate"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server on 127.0.0.1:8080: {e}. Is the server running?")

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized without token, got {response.status_code}"

def test_api_authorized_and_logic():
    url = "http://127.0.0.1:8080/api/protein/P12345/validate"
    headers = {"Authorization": "Bearer protein-secret-42"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server on 127.0.0.1:8080: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK with valid token, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "id" in data, "Response JSON missing 'id' key"
    assert "length" in data, "Response JSON missing 'length' key"
    assert "mse" in data, "Response JSON missing 'mse' key"

    assert data["id"] == "P12345", f"Expected id 'P12345', got {data['id']}"

    expected_length = get_fasta_length('/app/data/proteins.fasta', 'P12345')
    assert data["length"] == expected_length, f"Expected length {expected_length}, got {data['length']}"

    # Based on the setup, the experimental curve is exactly analytical + 1.0, so MSE is 1.0
    assert math.isclose(data["mse"], 1.0, rel_tol=1e-2), f"Expected MSE to be exactly 1.0, got {data['mse']}"