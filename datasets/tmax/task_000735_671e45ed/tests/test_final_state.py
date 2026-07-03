# test_final_state.py

import os
import h5py
import numpy as np
import pytest
import requests
import time

def get_expected_trace(seq_id):
    spectra_file = "/app/data/spectra.h5"
    if not os.path.exists(spectra_file):
        pytest.fail(f"Data file {spectra_file} is missing.")

    with h5py.File(spectra_file, "r") as f:
        if seq_id not in f:
            pytest.fail(f"Dataset {seq_id} missing in HDF5 file.")
        M = f[seq_id][:]

    L = np.linalg.cholesky(M + np.eye(M.shape[0]) * 1e-5)
    return np.trace(L)

def wait_for_server(url, timeout=5):
    start = time.time()
    while time.time() - start < timeout:
        try:
            requests.get(url)
            return
        except requests.ConnectionError:
            time.sleep(0.2)
    pytest.fail(f"Server not reachable at {url} within {timeout} seconds.")

def test_results_file_exists_and_format():
    results_file = "/home/user/results.txt"
    assert os.path.isfile(results_file), f"Results file {results_file} is missing."

    with open(results_file, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 50, f"Expected 50 lines in {results_file}, found {len(lines)}."

    # Check one specific line to ensure formatting is correct
    seq_10_line = next((line for line in lines if line.startswith("seq_10:")), None)
    assert seq_10_line is not None, "seq_10 not found in results.txt"

    parts = seq_10_line.split(":")
    assert len(parts) == 2, f"Malformed line for seq_10 in results.txt: {seq_10_line}"

    val_str = parts[1].strip()
    try:
        val = float(val_str)
    except ValueError:
        pytest.fail(f"Value for seq_10 is not a valid float: {val_str}")

    expected_val = get_expected_trace("seq_10")
    assert np.isclose(val, expected_val, rtol=1e-4), f"Incorrect trace for seq_10 in results.txt. Expected {expected_val}, got {val}"

def test_server_unauthorized():
    url = "http://127.0.0.1:9090/trace/seq_10"
    wait_for_server("http://127.0.0.1:9090")

    response = requests.get(url)
    assert response.status_code == 401, f"Expected 401 Unauthorized for missing token, got {response.status_code}"

def test_server_invalid_token():
    url = "http://127.0.0.1:9090/trace/seq_10"
    headers = {"Authorization": "Bearer wrong-token"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 401, f"Expected 401 Unauthorized for invalid token, got {response.status_code}"

def test_server_valid_request():
    url = "http://127.0.0.1:9090/trace/seq_10"
    headers = {"Authorization": "Bearer secret-bio-token"}
    response = requests.get(url, headers=headers)

    assert response.status_code == 200, f"Expected 200 OK for valid request, got {response.status_code}. Response: {response.text}"

    try:
        returned_trace = float(response.text.strip())
    except ValueError:
        pytest.fail(f"Server returned non-float response: {response.text}")

    expected_val = get_expected_trace("seq_10")
    assert np.isclose(returned_trace, expected_val, rtol=1e-4), f"Server returned incorrect trace for seq_10. Expected {expected_val}, got {returned_trace}"

def test_server_another_sequence():
    url = "http://127.0.0.1:9090/trace/seq_42"
    headers = {"Authorization": "Bearer secret-bio-token"}
    response = requests.get(url, headers=headers)

    assert response.status_code == 200, f"Expected 200 OK for valid request, got {response.status_code}"

    try:
        returned_trace = float(response.text.strip())
    except ValueError:
        pytest.fail(f"Server returned non-float response: {response.text}")

    expected_val = get_expected_trace("seq_42")
    assert np.isclose(returned_trace, expected_val, rtol=1e-4), f"Server returned incorrect trace for seq_42. Expected {expected_val}, got {returned_trace}"