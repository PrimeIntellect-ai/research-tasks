# test_final_state.py
import os
import json
import urllib.request
import urllib.error
import pytest

WORKSPACE_DIR = "/home/user/mobile_pipeline"
LIB_PATH = os.path.join(WORKSPACE_DIR, "libsemver.so")
LOG_PATH = os.path.join(WORKSPACE_DIR, "pipeline.log")
API_URL = "http://127.0.0.1:8080/resolve"

def test_workspace_and_lib_exist():
    """Verify that the workspace directory and the compiled shared library exist."""
    assert os.path.isdir(WORKSPACE_DIR), f"Workspace directory missing: {WORKSPACE_DIR}"
    assert os.path.isfile(LIB_PATH), f"Shared library missing: {LIB_PATH}"

def test_log_file_content():
    """Verify that the log file contains the required startup message."""
    assert os.path.isfile(LOG_PATH), f"Log file missing: {LOG_PATH}"
    with open(LOG_PATH, "r") as f:
        content = f.read()
    expected_msg = "[API READY] Server listening on port 8080"
    assert expected_msg in content, f"Log file does not contain the expected message: '{expected_msg}'"

def test_api_resolve_endpoint():
    """Verify that the API resolves the latest version correctly, handling multi-digit version components."""
    payload = {
        "versions": ["1.0.0", "1.0.1", "1.2.0", "2.2.9", "2.10.1", "2.3.0"]
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        response = urllib.request.urlopen(req, timeout=5)
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to API at {API_URL} or request error: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error during API request: {e}")

    assert response.status == 200, f"Expected HTTP 200, got {response.status}"

    try:
        response_body = response.read().decode("utf-8")
        result = json.loads(response_body)
    except Exception as e:
        pytest.fail(f"Failed to parse JSON response: {e}")

    assert "latest" in result, "Response JSON is missing the 'latest' key"
    assert result["latest"] == "2.10.1", f"Expected latest version to be '2.10.1', got '{result['latest']}'"

def test_api_resolve_endpoint_edge_cases():
    """Verify API behavior with another set of versions to ensure robust semver parsing."""
    payload = {
        "versions": ["0.9.9", "10.0.0", "9.99.99"]
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        response = urllib.request.urlopen(req, timeout=5)
        response_body = response.read().decode("utf-8")
        result = json.loads(response_body)
    except Exception as e:
        pytest.fail(f"Failed during edge case API request: {e}")

    assert result.get("latest") == "10.0.0", f"Expected latest version to be '10.0.0', got '{result.get('latest')}'"