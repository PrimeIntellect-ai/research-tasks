# test_final_state.py

import os
import json
import requests
import pytest

def test_top_nodes_file_contents():
    file_path = "/home/user/top_nodes.json"
    assert os.path.exists(file_path), f"File {file_path} does not exist. Did you run the compute script and save the output?"

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} does not contain valid JSON.")

    expected = [
        {"node_id": "N1", "centrality": 4},
        {"node_id": "N2", "centrality": 2},
        {"node_id": "N3", "centrality": 0}
    ]

    assert data == expected, f"JSON content in {file_path} does not match expected output. Expected {expected}, got {data}"

def test_api_server_response():
    url = "http://127.0.0.1:8080/api/top_nodes"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API server at {url}. Is the server running? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP status 200, got {response.status_code}. Response: {response.text}"

    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Expected Content-Type to contain 'application/json', got '{content_type}'"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON. Response text: {response.text}")

    expected = [
        {"node_id": "N1", "centrality": 4},
        {"node_id": "N2", "centrality": 2},
        {"node_id": "N3", "centrality": 0}
    ]

    assert data == expected, f"API response JSON does not match expected output. Expected {expected}, got {data}"