# test_final_state.py

import os
import subprocess
import requests
import pytest
import time

def get_actual_commit_count():
    repo_path = "/home/user/source_repo"
    try:
        result = subprocess.run(
            ["git", "-C", repo_path, "rev-list", "--count", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return int(result.stdout.strip())
    except Exception as e:
        pytest.fail(f"Could not get commit count from {repo_path}: {e}")

def test_crontab_installed():
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
        assert "/home/user/cron_task.sh" in result.stdout, "cron_task.sh is not installed in the crontab"
        assert "* * * * *" in result.stdout, "cron_task.sh is not scheduled to run every minute"
    except subprocess.CalledProcessError:
        pytest.fail("No crontab installed for the user.")

def test_cron_script_fixed():
    script_path = "/home/user/cron_task.sh"
    assert os.path.isfile(script_path), f"Missing {script_path}"
    with open(script_path, "r") as f:
        content = f.read()
    # Check that absolute paths are used, or at least it doesn't just do `cd source_repo`
    assert "/home/user/source_repo" in content or "cd /home/user/source_repo" in content, \
        "cron_task.sh does not seem to use the absolute path for source_repo"
    assert "/home/user/metrics_output.json" in content, \
        "cron_task.sh does not seem to use the absolute path for metrics_output.json"

def test_api_unauthorized():
    url = "http://127.0.0.1:7331/api/metrics"
    try:
        response = requests.get(url, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the dashboard backend at {url}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized without token, got {response.status_code}"

def test_api_authorized_and_content():
    url = "http://127.0.0.1:7331/api/metrics"
    headers = {"Authorization": "Bearer T0k3n_S3cr3t"}
    try:
        response = requests.get(url, headers=headers, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the dashboard backend at {url}: {e}")

    assert response.status_code == 200, f"Expected 200 OK with valid token, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response body is not valid JSON")

    assert "commits" in data, "JSON response missing 'commits' key"

    expected_commits = get_actual_commit_count()
    assert data["commits"] == expected_commits, \
        f"Expected {expected_commits} commits, but API returned {data['commits']}"