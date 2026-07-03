# test_final_state.py
import os
import threading
import requests
import pytest

def test_setup_py_fixed():
    """Verify that the dependency conflict in setup.py has been resolved."""
    setup_path = "/app/data_aggregator-1.0.0/setup.py"
    assert os.path.isfile(setup_path), f"File {setup_path} does not exist"

    with open(setup_path, "r") as f:
        content = f.read()

    assert "urllib3==1.24.0" not in content, "setup.py still contains the conflicting urllib3==1.24.0 dependency"

def test_server_py_has_assertion():
    """Verify that the payload assertion is present in server.py."""
    server_path = "/app/data_aggregator-1.0.0/data_aggregator/server.py"
    assert os.path.isfile(server_path), f"File {server_path} does not exist"

    with open(server_path, "r") as f:
        content = f.read()

    assert "assert isinstance(payload, dict)" in content, "server.py is missing the required assertion: assert isinstance(payload, dict)"

def test_server_concurrent_requests():
    """
    Verify that the server is running, accepts the correct API key,
    and successfully handles concurrent requests without deadlocking.
    """
    url = "http://127.0.0.1:8080/process"
    headers = {
        "X-API-Key": "secret-ops-token",
        "Content-Type": "application/json"
    }
    payload = {"data": "test_string", "value": 42}

    results = []
    exceptions = []

    def make_request():
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=5)
            results.append(response)
        except Exception as e:
            exceptions.append(e)

    threads = []
    num_requests = 10

    for _ in range(num_requests):
        t = threading.Thread(target=make_request)
        threads.append(t)
        t.start()

    for t in threads:
        t.join(timeout=6)

    assert not exceptions, f"Exceptions occurred during concurrent requests (possible connection refused or timeout): {exceptions}"
    assert len(results) == num_requests, "Not all requests completed within the timeout. The server might be deadlocking."

    for resp in results:
        assert resp.status_code == 200, f"Expected status code 200, got {resp.status_code}. Response body: {resp.text}"

        try:
            data = resp.json()
        except ValueError:
            pytest.fail(f"Response is not valid JSON: {resp.text}")

        assert data.get("status") == "success", f"Expected status 'success', got {data.get('status')}"
        assert data.get("processed_value") == 42, f"Expected processed_value 42, got {data.get('processed_value')}"