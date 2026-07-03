# test_final_state.py

import os
import pytest
import requests
import time

def test_server_file_exists():
    assert os.path.isfile("/app/server.py"), "The server script /app/server.py does not exist."

def test_server_parse_endpoint():
    url = "http://127.0.0.1:8181/parse"

    # Wait for the server to be up, just in case
    max_retries = 5
    for i in range(max_retries):
        try:
            # Check if port is open / server is responding
            requests.get("http://127.0.0.1:8181")
            break
        except requests.exceptions.ConnectionError:
            time.sleep(1)

    # Test case 1: Normal log data
    payload = b'\x02\x05ERROR\x03\x02\x04WARN\x03'
    try:
        response = requests.post(url, data=payload, headers={'Content-Type': 'application/octet-stream'})
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to the parsing service at 127.0.0.1:8181.")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"
    assert response.headers.get('Content-Type', '').startswith('application/json'), "Expected Content-Type: application/json"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data == ["ERROR", "WARN"], f"Expected parsed output ['ERROR', 'WARN'], got {data}"

    # Test case 2: Empty log data
    payload_empty = b''
    response_empty = requests.post(url, data=payload_empty)
    assert response_empty.status_code == 200, "Expected status code 200 for empty payload"
    assert response_empty.json() == [], f"Expected empty list for empty payload, got {response_empty.json()}"