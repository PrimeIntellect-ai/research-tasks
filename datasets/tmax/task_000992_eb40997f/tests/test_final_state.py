# test_final_state.py

import os
import pytest
import requests
import time

def test_auth_h_updated():
    path = "/home/user/server_src/auth.h"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "sunflower" in content.lower(), f"Passphrase 'sunflower' not found in {path}."

def test_bench_results_exist():
    path = "/home/user/bench_results.txt"
    assert os.path.isfile(path), f"Benchmark results file {path} does not exist."
    assert os.path.getsize(path) > 0, f"Benchmark results file {path} is empty."

def test_server_running_and_auth_works():
    url = "http://127.0.0.1:8080/secure"

    # Wait for server to be up, though it should be already
    max_retries = 5
    for i in range(max_retries):
        try:
            # Try with correct auth
            response = requests.get(url, auth=("admin", "sunflower"), timeout=2)
            break
        except requests.exceptions.ConnectionError:
            if i == max_retries - 1:
                pytest.fail("Could not connect to the server at 127.0.0.1:8080. Is it running?")
            time.sleep(1)

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}."
    assert "Access Granted" in response.text, f"Expected 'Access Granted' in response body, got: {response.text}"

def test_server_rejects_bad_auth():
    url = "http://127.0.0.1:8080/secure"
    try:
        response = requests.get(url, auth=("admin", "wrongpassword"), timeout=2)
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the server at 127.0.0.1:8080.")

    assert response.status_code != 200, "Server should not return 200 OK for incorrect credentials."