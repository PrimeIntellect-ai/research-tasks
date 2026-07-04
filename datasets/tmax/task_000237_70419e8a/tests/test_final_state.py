# test_final_state.py

import os
import pytest
import requests

APP_DIR = "/app"
LIBRARY_DIR = os.path.join(APP_DIR, "fast-url-parser-1.2.0")
SO_FILE = os.path.join(LIBRARY_DIR, "libfastparser.so")
BENCH_RESULTS = os.path.join(APP_DIR, "bench_results.txt")

BASE_URL = "http://127.0.0.1:8888/api/v1/normalize"
HEADERS = {"Authorization": "Bearer dev-sec-token"}

def test_shared_object_compiled():
    """Test that the C library was successfully compiled."""
    assert os.path.isfile(SO_FILE), f"Shared object not found: {SO_FILE}. The Makefile might not be fixed or 'make' was not run."

def test_server_no_auth():
    """Test that the server returns 401 Unauthorized when the Authorization header is missing."""
    try:
        response = requests.get(BASE_URL, params={"path": "/test", "min_version": "1.0.0", "client_version": "1.0.0"})
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the server at 127.0.0.1:8888. Is it running?")

    assert response.status_code == 401, f"Expected 401 for missing auth, got {response.status_code}"

def test_server_invalid_auth():
    """Test that the server returns 401 Unauthorized when the Authorization header is invalid."""
    response = requests.get(BASE_URL, headers={"Authorization": "Bearer wrong-token"}, params={"path": "/test", "min_version": "1.0.0", "client_version": "1.0.0"})
    assert response.status_code == 401, f"Expected 401 for invalid auth, got {response.status_code}"

def test_server_version_check_lower():
    """Test that the server returns 403 Forbidden when client_version is lower than min_version."""
    params = {"path": "/test", "min_version": "2.0.0", "client_version": "1.0.0"}
    response = requests.get(BASE_URL, headers=HEADERS, params=params)
    assert response.status_code == 403, f"Expected 403 for client_version < min_version, got {response.status_code}"

def test_server_version_check_malformed():
    """Test that the server returns 403 Forbidden when versions are malformed."""
    params = {"path": "/test", "min_version": "1.0.0", "client_version": "1.0a"}
    response = requests.get(BASE_URL, headers=HEADERS, params=params)
    assert response.status_code == 403, f"Expected 403 for malformed version, got {response.status_code}"

def test_server_success_normalization():
    """Test that the server successfully normalizes the path using the C library."""
    params = {"path": "../../../etc/passwd", "min_version": "1.0.0", "client_version": "1.2.0"}
    response = requests.get(BASE_URL, headers=HEADERS, params=params)
    assert response.status_code == 200, f"Expected 200 for valid request, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data.get("status") == "success", f"Expected status 'success', got {data.get('status')}"
    assert data.get("cleaned_path") == "etc/passwd", f"Expected cleaned_path 'etc/passwd', got {data.get('cleaned_path')}"

def test_bench_results_exist_and_valid():
    """Test that the bench_results.txt file exists and contains a valid float."""
    assert os.path.isfile(BENCH_RESULTS), f"Benchmark results file missing: {BENCH_RESULTS}"

    with open(BENCH_RESULTS, "r") as f:
        content = f.read().strip()

    try:
        time_taken = float(content)
    except ValueError:
        pytest.fail(f"Benchmark results file does not contain a valid float: '{content}'")

    assert time_taken > 0, "Benchmark time should be greater than 0."