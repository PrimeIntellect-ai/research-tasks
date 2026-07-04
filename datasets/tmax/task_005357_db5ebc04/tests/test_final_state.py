# test_final_state.py

import os
import time
import requests
import re
import pytest

def test_cjson_installed():
    """Verify that cJSON is compiled and installed correctly."""
    assert os.path.isfile("/app/local/lib/libcJSON.so"), "libcJSON.so is missing from /app/local/lib"
    assert os.path.isfile("/app/local/include/cJSON.h"), "cJSON.h is missing from /app/local/include"

def test_api_post_and_get_metrics():
    """Verify POST /metrics and GET /metrics behavior."""
    url = "http://127.0.0.1:8080/metrics"
    payload = [{"id": 3, "value": "apple"}, {"id": 1, "value": "banana"}]

    # POST metrics
    try:
        post_response = requests.post(url, json=payload, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server for POST /metrics: {e}")

    assert post_response.status_code == 200, f"Expected POST /metrics to return 200, got {post_response.status_code}"

    # GET metrics
    try:
        get_response = requests.get(url, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server for GET /metrics: {e}")

    assert get_response.status_code == 200, f"Expected GET /metrics to return 200, got {get_response.status_code}"

    expected_data = [{"id": 1, "value": "YmFuYW5h"}, {"id": 3, "value": "YXBwbGU="}]
    try:
        actual_data = get_response.json()
    except ValueError:
        pytest.fail("GET /metrics did not return valid JSON")

    assert actual_data == expected_data, f"Expected GET /metrics to return {expected_data}, got {actual_data}"

def test_rate_limiting():
    """Verify rate limiting: max 5 requests per second."""
    url = "http://127.0.0.1:8080/metrics"
    payload = [{"id": 10, "value": "test"}]

    # Wait a bit to ensure we start a fresh second window
    time.sleep(1.1)

    responses = []
    for _ in range(6):
        responses.append(requests.post(url, json=payload, timeout=2).status_code)

    # The first 5 should be accepted (or at least some accepted, but the 6th MUST be 429)
    assert responses[5] == 429, f"Expected 6th request to return 429 Too Many Requests, got {responses[5]}. All responses: {responses}"

def test_log_file_format():
    """Verify the log file exists and follows the expected format."""
    log_path = "/home/user/api.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        lines = f.readlines()

    assert len(lines) > 0, "Log file is empty."

    # Format: [TIMESTAMP] METHOD PATH STATUS
    # Example: [2023-10-25T12:34:56Z] POST /metrics 200
    pattern = re.compile(r"^\[.*?\]\s+(GET|POST)\s+/metrics\s+\d{3}\s*$")

    valid_lines = 0
    for line in lines:
        if pattern.match(line):
            valid_lines += 1

    assert valid_lines > 0, f"No lines in {log_path} matched the expected format '[TIMESTAMP] METHOD PATH STATUS'."