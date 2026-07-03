# test_final_state.py

import os
import time
import urllib.request
import urllib.error
import pytest

def test_success_log_exists():
    """Verify that the success.log file was created."""
    assert os.path.isfile("/home/user/success.log"), "The file /home/user/success.log does not exist. Did you forget to create it?"

def test_server_built():
    """Verify that the server executable was built successfully."""
    server_path = "/home/user/backend/server"
    assert os.path.isfile(server_path), f"The server executable at {server_path} does not exist. Make sure the Makefile is fixed and make was run."
    assert os.access(server_path, os.X_OK), f"The file at {server_path} is not executable."

def test_nginx_invalid_header():
    """Verify that requests without the correct X-Utility-Key header return 403."""
    req = urllib.request.Request("http://127.0.0.1:8000/api/")
    try:
        urllib.request.urlopen(req)
        pytest.fail("Expected 403 Forbidden for missing X-Utility-Key header, but the request succeeded.")
    except urllib.error.HTTPError as e:
        assert e.code == 403, f"Expected 403 Forbidden, but got {e.code}."
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx on port 8000: {e.reason}")

def test_nginx_valid_request_and_rate_limit():
    """Verify that a valid request returns 200, and a subsequent immediate request returns 503 due to rate limiting."""
    req = urllib.request.Request("http://127.0.0.1:8000/api/")
    req.add_header("X-Utility-Key", "secret123")

    # Wait a bit to ensure the rate limit bucket has a token
    time.sleep(1.1)

    # First request should succeed
    try:
        resp = urllib.request.urlopen(req)
        assert resp.getcode() == 200, f"Expected 200 OK for valid request, but got {resp.getcode()}."
    except urllib.error.HTTPError as e:
        pytest.fail(f"Expected 200 OK for valid request, but got HTTP {e.code}.")
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx on port 8000: {e.reason}")

    # Immediate second request should hit the rate limit (1 req/sec) and return 503
    try:
        urllib.request.urlopen(req)
        pytest.fail("Expected 503 Service Unavailable due to rate limit, but the request succeeded.")
    except urllib.error.HTTPError as e:
        assert e.code == 503, f"Expected 503 Service Unavailable for rate-limited request, but got {e.code}."