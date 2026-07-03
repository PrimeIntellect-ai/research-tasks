# test_final_state.py

import os
import requests
import pytest

def test_isolated_bug_file():
    bug_file_path = '/home/user/isolated_bug.txt'
    assert os.path.isfile(bug_file_path), f"The isolated bug file {bug_file_path} does not exist."

    with open(bug_file_path, 'r') as f:
        content = f.read().strip()

    expected_line = "[ERROR] [System] [Auth Missing closing bracket"
    assert content == expected_line, f"The isolated bug file contains '{content}' instead of the expected '{expected_line}'."

def test_process_logs_endpoint():
    url = "http://localhost:5000/process_logs"
    payload = {
        "logs": [
            "[INFO] Normal log",
            "[ERROR] [System] [Auth Missing closing bracket"
        ]
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API Gateway at {url}. Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    expected_results = ["Normal log", "malformed"]
    assert "results" in data, f"Response JSON missing 'results' key. Data: {data}"
    assert data["results"] == expected_results, f"Expected results {expected_results}, but got {data['results']}."