# test_final_state.py

import os
import json
import pytest
import requests

def test_files_exist():
    """Check if required files are generated."""
    assert os.path.exists("/home/user/raw_signal.csv"), "Missing /home/user/raw_signal.csv"
    assert os.path.exists("/home/user/cleaned_signal.json"), "Missing /home/user/cleaned_signal.json"
    assert os.path.exists("/home/user/pipeline.sh"), "Missing /home/user/pipeline.sh"
    assert os.path.exists("/home/user/pipeline.log"), "Missing /home/user/pipeline.log"

def test_pipeline_log_content():
    """Check if the pipeline log contains the required lines."""
    with open("/home/user/pipeline.log", "r") as f:
        log_content = f.read()

    assert "[INFO] Starting extraction" in log_content, "Missing '[INFO] Starting extraction' in log"
    assert "[INFO] Extraction complete" in log_content, "Missing '[INFO] Extraction complete' in log"
    assert "[INFO] Starting cleaning" in log_content, "Missing '[INFO] Starting cleaning' in log"
    assert "[INFO] Cleaning complete" in log_content, "Missing '[INFO] Cleaning complete' in log"

def test_http_api_no_auth():
    """Check that /api/data requires authorization."""
    try:
        response = requests.get("http://127.0.0.1:8080/api/data", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP server: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 without auth, got {response.status_code}"

def test_http_api_data_with_auth():
    """Check that /api/data returns the correct JSON array with auth."""
    headers = {"Authorization": "Bearer ds-secret-token"}
    try:
        response = requests.get("http://127.0.0.1:8080/api/data", headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP server: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 with auth, got {response.status_code}"
    assert "application/json" in response.headers.get("Content-Type", ""), "Expected application/json content type"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response from /api/data is not valid JSON")

    assert isinstance(data, list), "Expected a JSON array from /api/data"
    assert len(data) == 98, f"Expected 98 items in the cleaned data, got {len(data)}"

    # Check index 52
    item_52 = next((item for item in data if item.get("frame_index") == 52), None)
    assert item_52 is not None, "Missing frame_index 52 in the cleaned data"
    assert abs(item_52.get("smoothed_intensity", 0) - 100.0) < 1e-5, f"Expected smoothed_intensity of 100.0 for index 52, got {item_52.get('smoothed_intensity')}"

def test_http_api_status_with_auth():
    """Check that /api/status returns the correct latest log entry."""
    headers = {"Authorization": "Bearer ds-secret-token"}
    try:
        response = requests.get("http://127.0.0.1:8080/api/status", headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP server: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 with auth, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response from /api/status is not valid JSON")

    assert data.get("latest_log") == "[INFO] Cleaning complete", f"Expected latest_log to be '[INFO] Cleaning complete', got {data.get('latest_log')}"