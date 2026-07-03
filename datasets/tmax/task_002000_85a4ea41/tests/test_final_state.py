# test_final_state.py

import os
import time
import requests
import pytest
import threading

def test_files_exist():
    assert os.path.exists("/home/user/etl_service"), "/home/user/etl_service does not exist"
    assert os.access("/home/user/etl_service", os.X_OK), "/home/user/etl_service is not executable"
    assert os.path.exists("/home/user/start.sh"), "/home/user/start.sh does not exist"
    assert os.access("/home/user/start.sh", os.X_OK), "/home/user/start.sh is not executable"

def test_unauthorized_request():
    url = "http://127.0.0.1:9090/traverse?start_node=1&depth=1"
    try:
        response = requests.get(url, timeout=2)
        assert response.status_code in (401, 403), f"Expected 401 or 403 for unauthorized request, got {response.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

def test_authorized_request():
    url = "http://127.0.0.1:9090/traverse?start_node=1&depth=1"
    headers = {"Authorization": "Bearer secret-etl-token"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

        data = response.json()
        assert isinstance(data, list) or "nodes" in data, "Response should be a JSON array of node IDs or an object with 'nodes' array"
        if isinstance(data, dict) and "nodes" in data:
            assert isinstance(data["nodes"], list), "'nodes' field must be a list"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")
    except ValueError:
        pytest.fail("Response is not valid JSON")

def test_concurrent_requests():
    url = "http://127.0.0.1:9090/traverse?start_node=1&depth=2"
    headers = {"Authorization": "Bearer secret-etl-token"}

    results = []

    def make_request():
        try:
            response = requests.get(url, headers=headers, timeout=10)
            results.append(response.status_code)
        except Exception as e:
            results.append(str(e))

    threads = [threading.Thread(target=make_request) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    for res in results:
        assert res == 200, f"Concurrent request failed with status/error: {res}"