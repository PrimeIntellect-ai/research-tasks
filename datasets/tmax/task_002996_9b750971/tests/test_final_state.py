# test_final_state.py
import os
import shutil
import pytest
import requests
import json

def test_datamash_installed():
    """Verify that datamash was successfully compiled and installed."""
    assert shutil.which("datamash") is not None, "datamash binary is not installed or not in PATH. The Makefile fix and installation may have failed."

def test_server_response():
    """Verify the HTTP server is running, returns correct headers, and accurate JSON aggregation."""
    url = "http://127.0.0.1:9090/"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}. Is the server running? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"
    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Expected Content-Type: application/json, got '{content_type}'"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response body is not valid JSON. Response text: {response.text}")

    expected_data = {
        "9223372036854775807": 150.75,
        "1234567890123456789": 150.00,
        "9999999999999999999": 10.00
    }

    # Verify the keys (large integers as strings) and their corresponding aggregated amounts
    for key, expected_value in expected_data.items():
        assert key in data, f"Expected user_id '{key}' is missing from the JSON response. Ensure 19-digit IDs are preserved as exact strings."
        actual_value = float(data[key])
        assert abs(actual_value - expected_value) < 1e-5, f"Expected sum {expected_value} for user_id '{key}', got {actual_value}"

    # Ensure no unexpected keys are present
    for key in data.keys():
        assert key in expected_data, f"Unexpected user_id '{key}' found in JSON response."