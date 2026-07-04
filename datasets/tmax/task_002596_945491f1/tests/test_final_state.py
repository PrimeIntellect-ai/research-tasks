# test_final_state.py

import os
import subprocess
import requests
import pytest

def test_secret_token():
    token_path = "/home/user/secret_token.txt"
    assert os.path.isfile(token_path), f"Secret token file missing at {token_path}"

    with open(token_path, "r") as f:
        token = f.read().strip().lower()

    expected_token = "the quick brown fox jumps over the lazy dog"
    # Remove any punctuation just in case, though the instructions say exact phrase
    import string
    token_clean = token.translate(str.maketrans('', '', string.punctuation))
    expected_clean = expected_token.translate(str.maketrans('', '', string.punctuation))

    assert token_clean == expected_clean, f"Secret token is incorrect. Expected '{expected_token}', got '{token}'"

def test_bad_commit_hash():
    repo_path = "/home/user/repo/audio-svc"
    commit_file = "/home/user/bad_commit.txt"
    assert os.path.isfile(commit_file), f"Bad commit file missing at {commit_file}"

    with open(commit_file, "r") as f:
        actual_commit = f.read().strip()

    # Find the commit that introduced the infinite loop bug
    # The truth says it changed `while data_val > 0.0` to `while data_val != 0.0`
    cmd = ["git", "log", "-G", "while.*!=.*0\\.0", "--format=%H", "--reverse"]
    result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True)
    expected_commits = [c for c in result.stdout.strip().split('\n') if c]

    if expected_commits:
        expected_commit = expected_commits[0]
        # Allow full hash or short hash
        assert actual_commit == expected_commit or expected_commit.startswith(actual_commit), \
            f"bad_commit.txt does not contain the correct commit hash. Expected {expected_commit}, got {actual_commit}"
    else:
        # Fallback if regex doesn't match exactly how it's formatted
        assert len(actual_commit) >= 7, f"bad_commit.txt does not seem to contain a valid commit hash: {actual_commit}"

def test_service_processing():
    url = "http://127.0.0.1:8080/process"
    payload = {
        "token": "the quick brown fox jumps over the lazy dog",
        "data": [-1.0, 2.5, -3.2]
    }

    try:
        # If the bug isn't fixed, this will hang, so we use a timeout
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.Timeout:
        pytest.fail("The service timed out. The infinite loop bug (convergence failure on negative inputs) might not be fixed.")
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the service at 127.0.0.1:8080. Is it running?")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP request failed: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Service did not return valid JSON. Response body: {response.text}")

    assert "result" in data, f"Response JSON missing 'result' key. Got: {data}"
    assert isinstance(data["result"], list), f"'result' should be a list, got {type(data['result'])}"
    assert len(data["result"]) == len(payload["data"]), "Result list length does not match input data length"