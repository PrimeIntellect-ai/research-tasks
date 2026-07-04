# test_final_state.py

import os
import requests
import pytest
import time

def test_makefile_fixed():
    makefile_path = "/app/wal-serve-v1.0/Makefile"
    assert os.path.isfile(makefile_path), f"Makefile is missing at {makefile_path}."

    with open(makefile_path, "r") as f:
        content = f.read()

    assert "-lz" in content, "Makefile was not updated to include the '-lz' linker flag."

def test_server_cpp_fixed():
    server_cpp_path = "/app/wal-serve-v1.0/server.cpp"
    assert os.path.isfile(server_cpp_path), f"server.cpp is missing at {server_cpp_path}."

    with open(server_cpp_path, "r") as f:
        content = f.read()

    assert "/var/old_data" not in content, "server.cpp still contains the buggy hardcoded path '/var/old_data'."
    assert "/home/user/dataset" in content, "server.cpp does not contain the correct dataset path '/home/user/dataset'."

def test_server_running_and_serving_data():
    url = "http://127.0.0.1:9090/records"

    # Retry a few times in case the server is slow to start, though it should already be running
    max_retries = 3
    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=2)
            break
        except requests.exceptions.RequestException as e:
            if i == max_retries - 1:
                pytest.fail(f"Failed to connect to the server at {url}. Is it running on port 9090? Error: {e}")
            time.sleep(1)

    assert response.status_code == 200, f"Expected HTTP 200 OK, but got {response.status_code}. Response body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, but failed to parse. Response body: {response.text}")

    assert data.get("status") == "success", f"Expected status 'success' in JSON, got: {data.get('status')}"
    assert "records" in data, "Expected 'records' key in JSON response."