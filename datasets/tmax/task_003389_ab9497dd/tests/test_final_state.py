# test_final_state.py

import os
import json
import pytest
import requests

def test_source_code_exists():
    """Verify that the C source code exists at the specified location."""
    path = "/home/user/workspace/analyzer.c"
    assert os.path.isfile(path), f"Source code file {path} is missing."

def test_binary_exists():
    """Verify that the compiled binary exists."""
    path = "/home/user/workspace/analyzer"
    assert os.path.isfile(path), f"Compiled binary {path} is missing."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_http_metrics_endpoint():
    """Verify the /metrics endpoint returns the correct JSON and headers."""
    url = "http://127.0.0.1:8000/metrics"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Expected Content-Type: application/json, got {content_type}"

    assert "X-Process-Time-Us" in response.headers, "Header X-Process-Time-Us is missing"
    try:
        int(response.headers["X-Process-Time-Us"])
    except ValueError:
        pytest.fail(f"Header X-Process-Time-Us is not an integer: {response.headers['X-Process-Time-Us']}")

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse JSON response: {response.text}")

    assert "max_amp" in data, "Key 'max_amp' missing in JSON response"
    assert "zero_crossings" in data, "Key 'zero_crossings' missing in JSON response"

    assert data["max_amp"] == 30000, f"Expected max_amp=30000, got {data['max_amp']}"
    assert data["zero_crossings"] == 880, f"Expected zero_crossings=880, got {data['zero_crossings']}"

def test_http_404_endpoint():
    """Verify that an unknown path returns 404 Not Found."""
    url = "http://127.0.0.1:8000/unknown"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 404, f"Expected status code 404, got {response.status_code}"