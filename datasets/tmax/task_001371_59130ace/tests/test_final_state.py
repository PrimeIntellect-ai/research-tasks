# test_final_state.py

import os
import subprocess
import requests
import json
import pytest
import time

def test_bad_commit_identified():
    repo_path = "/home/user/acoustic-node"
    bad_commit_file = "/home/user/bad_commit.txt"

    assert os.path.isfile(bad_commit_file), f"File {bad_commit_file} does not exist."

    with open(bad_commit_file, "r") as f:
        student_commit = f.read().strip()

    assert len(student_commit) == 40, f"Expected a 40-character SHA hash, got {len(student_commit)} characters."

    # Find the actual bad commit hash
    try:
        output = subprocess.check_output(
            ["git", "log", "--format=%H", "--grep=refactor: optimize concurrent chunk aggregation"],
            cwd=repo_path, text=True, stderr=subprocess.STDOUT
        )
        expected_commit = output.strip().splitlines()[0]
    except Exception as e:
        pytest.fail(f"Failed to find the expected bad commit in the repository: {e}")

    assert student_commit == expected_commit, f"Incorrect bad commit identified. Expected {expected_commit}, got {student_commit}."

def test_server_process_endpoint():
    url = "http://127.0.0.1:8080/process"
    headers = {
        "Authorization": "Bearer math-telemetry-xyz",
        "Content-Type": "application/json"
    }
    payload = {"filepath": "/app/telemetry_signal.wav"}
    expected_variance = 42.13371337890625

    # Wait briefly for server to be ready if needed, but it should be running
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Server did not return valid JSON. Response: {response.text}")

    assert "variance" in data, f"Response JSON missing 'variance' key. Got: {data}"
    assert isinstance(data["variance"], (int, float)), f"Expected 'variance' to be a number, got {type(data['variance'])}"

    # Check exact precision
    assert data["variance"] == expected_variance, f"Expected variance to be exactly {expected_variance}, got {data['variance']}."

def test_server_no_race_condition():
    url = "http://127.0.0.1:8080/process"
    headers = {
        "Authorization": "Bearer math-telemetry-xyz",
        "Content-Type": "application/json"
    }
    payload = {"filepath": "/app/telemetry_signal.wav"}
    expected_variance = 42.13371337890625

    # Issue multiple requests to ensure stability and no race condition
    for i in range(10):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=5)
            assert response.status_code == 200, f"Request {i+1} failed with status {response.status_code}."
            data = response.json()
            assert data["variance"] == expected_variance, f"Race condition detected on request {i+1}. Expected {expected_variance}, got {data['variance']}."
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Request {i+1} failed: {e}")