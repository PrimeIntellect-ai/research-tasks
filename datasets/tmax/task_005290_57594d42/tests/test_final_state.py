# test_final_state.py
import os
import subprocess
import time
import requests
import pytest

def get_bad_commit():
    repo_path = "/app/bash-http-server"
    # Find the commit that introduced "fuzz-crash"
    cmd = ["git", "log", "-S", "fuzz-crash", "--format=%H", "--reverse"]
    result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True)
    commits = result.stdout.strip().splitlines()
    if commits:
        return commits[0]
    return None

def test_bad_commit_identified():
    bad_commit_file = "/home/user/bad_commit.txt"
    assert os.path.isfile(bad_commit_file), f"File {bad_commit_file} does not exist. Did you save the bad commit hash?"

    with open(bad_commit_file, "r") as f:
        student_commit = f.read().strip()

    expected_commit = get_bad_commit()
    assert expected_commit is not None, "Could not find the bad commit in the repository history."
    assert student_commit == expected_commit, f"Expected bad commit {expected_commit}, but got {student_commit}."

def test_server_responds_ok():
    try:
        response = requests.get("http://127.0.0.1:9090/", timeout=5)
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}."
        assert response.text.strip() == "OK", f"Expected body 'OK', got '{response.text}'."
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server on 127.0.0.1:9090: {e}")

def test_server_no_process_leak():
    def get_sleep_processes():
        try:
            result = subprocess.run(["pgrep", "-f", "sleep 0.1"], capture_output=True, text=True)
            return set(result.stdout.strip().splitlines())
        except subprocess.CalledProcessError:
            return set()

    initial_procs = get_sleep_processes()

    headers = {"User-Agent": "fuzz-crash-test"}
    try:
        requests.get("http://127.0.0.1:9090/compute", headers=headers, timeout=2)
    except requests.exceptions.RequestException:
        pass

    time.sleep(2)

    final_procs = get_sleep_processes()
    new_procs = final_procs - initial_procs

    assert len(new_procs) == 0, "Found leaked background processes after sending malicious request."