# test_final_state.py

import pytest
import requests
import concurrent.futures
import time

TOKEN = "SECRET_TOKEN_992"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}
BASE_URL = "http://127.0.0.1:8080"

def make_request(endpoint):
    try:
        if endpoint == "/query":
            response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS, timeout=3)
        else:
            response = requests.post(f"{BASE_URL}{endpoint}", headers=HEADERS, timeout=3)
        return response.status_code, response.text
    except requests.exceptions.Timeout:
        return "TIMEOUT", "Request timed out, possible deadlock."
    except requests.exceptions.ConnectionError:
        return "CONNECTION_ERROR", "Failed to connect, is the server running?"
    except Exception as e:
        return "ERROR", str(e)

def test_server_running_and_no_deadlock():
    # Attempt a single connection first to check if the server is up
    try:
        init_resp = requests.get(f"{BASE_URL}/query", headers=HEADERS, timeout=2)
        assert init_resp.status_code == 200, f"Initial request failed with status {init_resp.status_code}: {init_resp.text}"
    except requests.exceptions.ConnectionError:
        pytest.fail("Server is not running on 127.0.0.1:8080 or refused connection.")
    except requests.exceptions.Timeout:
        pytest.fail("Initial request timed out. Server might be hanging.")

    # Send 100 concurrent requests mixing /query and /update to trigger potential deadlocks
    endpoints = ["/query", "/update"] * 50

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(make_request, ep): ep for ep in endpoints}
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    failures = [r for r in results if r[0] != 200]

    if failures:
        error_summary = {}
        for status, msg in failures:
            error_summary[status] = error_summary.get(status, 0) + 1
        pytest.fail(f"Concurrent requests failed. Summary of errors: {error_summary}. First few errors: {failures[:5]}")