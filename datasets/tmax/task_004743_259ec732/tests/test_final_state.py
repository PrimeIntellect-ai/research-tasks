# test_final_state.py

import os
import subprocess
import requests
import pytest

def test_failure_frame():
    frame_file = "/home/user/failure_frame.txt"
    assert os.path.isfile(frame_file), f"File {frame_file} does not exist."
    with open(frame_file, "r") as f:
        content = f.read().strip()
    assert content == "142", f"Expected failure frame to be 142, but got '{content}'."

def test_bad_commit():
    commit_file = "/home/user/bad_commit.txt"
    repo_path = "/home/user/monitor_repo"

    assert os.path.isfile(commit_file), f"File {commit_file} does not exist."
    with open(commit_file, "r") as f:
        submitted_hash = f.read().strip()

    # The bad commit is the 3rd commit in the repository history
    try:
        git_log = subprocess.check_output(
            ["git", "-C", repo_path, "log", "--reverse", "--format=%H"],
            text=True
        )
        commits = git_log.strip().split("\n")
        assert len(commits) >= 3, "Repository does not have enough commits."
        expected_hash = commits[2].strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run git command in {repo_path}: {e}")

    assert submitted_hash == expected_hash, f"Expected bad commit hash {expected_hash}, but got {submitted_hash}."

def test_http_service_success():
    url = "http://127.0.0.1:8080/api/v1/sla"
    headers = {
        "Authorization": "Bearer uptime-token-2024",
        "Content-Type": "application/json"
    }
    payload = {"event_time": "2023-10-27T15:30:00Z"}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response: {response.text}")

    assert "sla" in data, f"Response JSON missing 'sla' key. Response: {data}"
    assert isinstance(data["sla"], (int, float)), f"'sla' value is not a number. Response: {data}"
    assert data.get("status") == "ok", f"Expected status 'ok', but got {data.get('status')}."

def test_http_service_unauthorized():
    url = "http://127.0.0.1:8080/api/v1/sla"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {"event_time": "2023-10-27T15:30:00Z"}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code in (401, 403), f"Expected status code 401 or 403 for unauthorized request, but got {response.status_code}."