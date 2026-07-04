# test_final_state.py
import os
import json
import subprocess
import pytest
import requests

def test_minimal_payload_correct():
    """Verify that the minimal payload was correctly identified and saved."""
    payload_path = "/home/user/minimal_payload.json"
    assert os.path.exists(payload_path), f"Minimal payload file {payload_path} does not exist."
    assert os.path.isfile(payload_path), f"{payload_path} is not a file."

    with open(payload_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{payload_path} is not a valid JSON file.")

    expected_payload = {"filters": {"metadata": {"is_archived": True}}}
    assert data == expected_payload, f"Minimal payload does not match the expected minimal JSON. Got: {data}"

def test_bad_commit_correct():
    """Verify that the student found the correct bad commit hash."""
    commit_file = "/home/user/bad_commit.txt"
    assert os.path.exists(commit_file), f"Bad commit file {commit_file} does not exist."

    with open(commit_file, 'r') as f:
        student_commit = f.read().strip()

    repo_path = "/app/api_repo"
    try:
        result = subprocess.run(
            ["git", "log", "--grep=Feature: filter by archive status", "--format=%H"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        expected_commit = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run git log in {repo_path}: {e.stderr}")

    assert expected_commit != "", "Could not find the expected commit in the repository."
    assert student_commit == expected_commit, f"Incorrect bad commit. Expected {expected_commit}, got {student_commit}"

def test_api_fixed_and_running():
    """Verify that the API is running, the bug is fixed, and it returns a 200 OK."""
    url = "http://127.0.0.1:8000/query"
    payload = {"filters": {"metadata": {"is_archived": True}}}

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the Flask API at {url}. Is it running? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"API did not return valid JSON. Response body: {response.text}")

    assert data.get("status") == "success", f"Expected 'status': 'success' in response, got: {data}"