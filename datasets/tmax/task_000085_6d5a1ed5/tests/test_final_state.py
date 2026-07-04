# test_final_state.py

import os
import time
import pytest
import requests

def test_required_files_exist():
    """Verify that the required files have been created."""
    required_files = [
        "/home/user/app/plugin.c",
        "/home/user/app/libgateway_plugins.so",
        "/home/user/test_results.log"
    ]
    for file_path in required_files:
        assert os.path.isfile(file_path), f"Required file {file_path} is missing."

def test_test_results_log_content():
    """Verify that the test results log contains the success message."""
    log_path = "/home/user/test_results.log"
    assert os.path.isfile(log_path), f"{log_path} is missing."
    with open(log_path, "r") as f:
        content = f.read()
    assert "ALL TESTS PASSED" in content, f"'{log_path}' does not contain 'ALL TESTS PASSED'."

def test_gateway_validation_rejection():
    """Verify that paths not starting with /api/v1/ are rejected with 403."""
    url = "http://127.0.0.1:8080/api/v2/test"
    try:
        resp = requests.get(url, timeout=2)
        assert resp.status_code == 403, f"Expected 403 Forbidden for {url}, got {resp.status_code}. Response: {resp.text}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Connection to Gateway at {url} failed: {e}")

def test_gateway_validation_acceptance():
    """Verify that valid paths are accepted with 200."""
    url = "http://127.0.0.1:8080/api/v1/ping"
    try:
        resp = requests.get(url, timeout=2)
        assert resp.status_code == 200, f"Expected 200 OK for {url}, got {resp.status_code}. Response: {resp.text}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Connection to Gateway at {url} failed: {e}")

def test_gateway_rate_limiting():
    """Verify that /api/v1/data enforces a rate limit of 3 requests per 2 seconds."""
    url = "http://127.0.0.1:8080/api/v1/data"

    # Wait for 2.1 seconds to ensure a clean rolling window before testing
    time.sleep(2.1)

    try:
        # Request 1
        resp1 = requests.get(url, timeout=2)
        assert resp1.status_code == 200, f"Request 1 expected 200 OK, got {resp1.status_code}. Response: {resp1.text}"

        # Request 2
        resp2 = requests.get(url, timeout=2)
        assert resp2.status_code == 200, f"Request 2 expected 200 OK, got {resp2.status_code}. Response: {resp2.text}"

        # Request 3
        resp3 = requests.get(url, timeout=2)
        assert resp3.status_code == 200, f"Request 3 expected 200 OK, got {resp3.status_code}. Response: {resp3.text}"

        # Request 4 (Should be rate limited)
        resp4 = requests.get(url, timeout=2)
        assert resp4.status_code == 429, f"Request 4 expected 429 Too Many Requests, got {resp4.status_code}. Response: {resp4.text}"

    except requests.exceptions.RequestException as e:
        pytest.fail(f"Rate limiting requests to {url} failed: {e}")