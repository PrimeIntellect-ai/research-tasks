# test_final_state.py

import os
import requests
import pytest

def calculate_xor_checksum(filepath):
    checksum = 0
    with open(filepath, 'rb') as f:
        while byte := f.read(1):
            checksum ^= byte[0]
    return checksum

def test_deploy_gate_unauthorized():
    url = "http://127.0.0.1:8080/deploy"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the deployment gate server at {url}: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized for request without token, got {response.status_code}"

def test_deploy_gate_authorized():
    url = "http://127.0.0.1:8080/deploy"
    headers = {"Authorization": "Bearer z9k-Delta-44"}

    try:
        response = requests.get(url, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the deployment gate server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK for valid token, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response body is not valid JSON")

    expected_version = "4.12.3"
    expected_checksum = calculate_xor_checksum("/app/payload.bin")

    assert data.get("status") == "ready", f"Expected status 'ready', got {data.get('status')}"
    assert data.get("version") == expected_version, f"Expected version '{expected_version}', got {data.get('version')}"
    assert data.get("checksum") == expected_checksum, f"Expected checksum {expected_checksum}, got {data.get('checksum')}"