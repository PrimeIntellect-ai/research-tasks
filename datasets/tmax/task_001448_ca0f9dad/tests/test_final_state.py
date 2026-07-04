# test_final_state.py
import os
import stat
import pytest
import requests
import time

def test_binaries_and_scripts_exist():
    sim_server_path = "/app/bin/sim_server"
    start_script_path = "/app/start.sh"

    assert os.path.isfile(sim_server_path), f"Compiled backend {sim_server_path} is missing."
    assert os.access(sim_server_path, os.X_OK), f"Compiled backend {sim_server_path} is not executable."

    assert os.path.isfile(start_script_path), f"Startup script {start_script_path} is missing."
    assert os.access(start_script_path, os.X_OK), f"Startup script {start_script_path} is not executable."

def test_api_unauthorized():
    url = "http://127.0.0.1:8080/analyze?fasta_id=protA"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}. Response: {response.text}"

def test_api_not_found():
    url = "http://127.0.0.1:8080/analyze?fasta_id=does_not_exist"
    headers = {"Authorization": "Bearer biophysics2024"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert response.status_code == 404, f"Expected 404 Not Found for missing FASTA file, got {response.status_code}. Response: {response.text}"

def test_api_valid_request_protA():
    url = "http://127.0.0.1:8080/analyze?fasta_id=protA"
    headers = {"Authorization": "Bearer biophysics2024"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "fasta_header" in data, "Missing 'fasta_header' in JSON response."
    assert "peak_freq" in data, "Missing 'peak_freq' in JSON response."

    expected_header = "sp|P00001|CYC_MACMU Cytochrome c"
    assert data["fasta_header"] == expected_header, f"Expected fasta_header '{expected_header}', got '{data['fasta_header']}'"

    # "protA\n" has length 6. Row freq = 6 * 3 = 18. Col freq = 5.
    expected_freq = [18, 5]
    assert data["peak_freq"] == expected_freq, f"Expected peak_freq {expected_freq}, got {data['peak_freq']}"

def test_api_valid_request_protB():
    url = "http://127.0.0.1:8080/analyze?fasta_id=protB"
    headers = {"Authorization": "Bearer biophysics2024"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    expected_header = "sp|P00002|CYC_HUMAN Cytochrome c"
    assert data["fasta_header"] == expected_header, f"Expected fasta_header '{expected_header}', got '{data['fasta_header']}'"

    # "protB\n" has length 6. Row freq = 6 * 3 = 18. Col freq = 5.
    expected_freq = [18, 5]
    assert data["peak_freq"] == expected_freq, f"Expected peak_freq {expected_freq}, got {data['peak_freq']}"