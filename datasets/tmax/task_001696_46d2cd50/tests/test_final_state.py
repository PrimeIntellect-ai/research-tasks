# test_final_state.py

import os
import json
import pytest
import requests

MANIFEST_PATH = "/home/user/manifest.json"
TOKEN = "ARCHIVE_X77B9_SECURE"
URL = "http://127.0.0.1:8080/api/manifest"

def get_expected_manifest():
    return [
        {"filename": "chunk1.dat", "owner": "admin", "timestamp": "2023-10-01T12:00:00Z"},
        {"filename": "chunk3.dat", "owner": "admin", "timestamp": "2023-10-03T12:00:00Z"}
    ]

def test_manifest_file_exists_and_correct():
    assert os.path.isfile(MANIFEST_PATH), f"Manifest file missing at {MANIFEST_PATH}"

    with open(MANIFEST_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {MANIFEST_PATH} does not contain valid JSON")

    expected = get_expected_manifest()
    assert data == expected, f"Manifest JSON content is incorrect. Expected {expected}, got {data}"

def test_api_no_token_returns_401():
    try:
        response = requests.get(URL, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API at {URL}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized when no token is provided, got {response.status_code}"

def test_api_wrong_token_returns_401():
    headers = {"Authorization": "Bearer INVALID_TOKEN"}
    try:
        response = requests.get(URL, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API at {URL}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized when invalid token is provided, got {response.status_code}"

def test_api_correct_token_returns_200_and_json():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    try:
        response = requests.get(URL, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API at {URL}: {e}")

    assert response.status_code == 200, f"Expected 200 OK with correct token, got {response.status_code}. Response: {response.text}"

    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Expected Content-Type application/json, got {content_type}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON. Body: {response.text}")

    expected = get_expected_manifest()
    assert data == expected, f"API response JSON is incorrect. Expected {expected}, got {data}"