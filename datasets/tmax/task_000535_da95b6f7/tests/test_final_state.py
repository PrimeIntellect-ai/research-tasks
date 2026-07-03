# test_final_state.py

import os
import json
import pytest
import requests
import time

def test_incident_data_file_exists():
    file_path = "/home/user/incident_data.json"
    assert os.path.exists(file_path), f"Output file missing: {file_path}"
    assert os.path.isfile(file_path), f"Expected a file, but found a directory: {file_path}"

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} does not contain valid JSON.")

    assert isinstance(data, list), "Expected a JSON array in the output file."
    assert len(data) == 3, f"Expected exactly 3 rows in the JSON array, got {len(data)}."

    # Check the values
    frame_indices = []
    for row in data:
        if isinstance(row, dict):
            # Try to find frame_idx
            idx = row.get("frame_idx")
            if idx is not None:
                frame_indices.append(int(idx))
        elif isinstance(row, list) and len(row) >= 1:
            frame_indices.append(int(row[0]))

    assert sorted(frame_indices) == [166, 167, 168], f"Expected frame indices 166, 167, 168, but got {frame_indices}."

def test_server_unauthorized():
    url = "http://127.0.0.1:8080/api/incident"
    try:
        response = requests.get(url, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for request without token, got {response.status_code}."

def test_server_wrong_token():
    url = "http://127.0.0.1:8080/api/incident"
    headers = {"Authorization": "Bearer wrong-token"}
    try:
        response = requests.get(url, headers=headers, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for request with wrong token, got {response.status_code}."

def test_server_authorized_and_correct_response():
    url = "http://127.0.0.1:8080/api/incident"
    headers = {"Authorization": "Bearer triage-token-99"}
    try:
        response = requests.get(url, headers=headers, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected 200 OK for authorized request, got {response.status_code}."

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Server did not return valid JSON. Response body: {response.text}")

    assert isinstance(data, list), "Expected a JSON array in the server response."
    assert len(data) == 3, f"Expected exactly 3 rows in the JSON array, got {len(data)}."

    frame_indices = []
    for row in data:
        if isinstance(row, dict):
            idx = row.get("frame_idx")
            if idx is not None:
                frame_indices.append(int(idx))
        elif isinstance(row, list) and len(row) >= 1:
            frame_indices.append(int(row[0]))

    assert sorted(frame_indices) == [166, 167, 168], f"Expected frame indices 166, 167, 168 in server response, but got {frame_indices}."