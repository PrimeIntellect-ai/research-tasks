# test_final_state.py

import os
import json
import pytest
import requests

def test_engineered_datasets_created():
    path = "/home/user/engineered_datasets.csv"
    assert os.path.isfile(path), f"Missing engineered dataset file: {path}"

    with open(path, 'r') as f:
        header = f.readline().strip()

    assert "time_since_creation" in header, "Engineered dataset missing 'time_since_creation' feature"
    assert "size_category" in header, "Engineered dataset missing 'size_category' feature"

def test_server_log_exists():
    path = "/home/user/server.log"
    assert os.path.isfile(path), f"Missing server log file: {path}"

def test_api_server_unauthorized():
    url = "http://127.0.0.1:8080/score"
    payload = {"time_since_creation": 150, "size_category": "medium"}
    try:
        response = requests.post(url, json=payload, timeout=2)
        # Should not succeed without authorization
        assert response.status_code in (401, 403), f"Expected 401 or 403 for unauthorized request, got {response.status_code}"
    except requests.exceptions.ConnectionError:
        pytest.fail("API server is not running or not reachable on 127.0.0.1:8080")

def test_api_server_authorized():
    url = "http://127.0.0.1:8080/score"
    payload = {"time_since_creation": 150, "size_category": "medium"}
    headers = {"Authorization": "Bearer secret-research-token"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"Response is not valid JSON: {response.text}")

        assert "score" in data, f"Response JSON missing 'score' key: {data}"
        assert isinstance(data["score"], (int, float)), f"Score must be a number, got {type(data['score'])}"

    except requests.exceptions.ConnectionError:
        pytest.fail("API server is not running or not reachable on 127.0.0.1:8080")