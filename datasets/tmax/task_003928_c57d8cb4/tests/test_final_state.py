# test_final_state.py

import os
import subprocess
import requests
import pytest

def test_deployment_log_exists():
    log_path = "/home/user/deployment.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read()
        assert "READY" in content, f"Log file {log_path} does not contain 'READY'."

def test_redis_motif_threshold():
    # Use redis-cli to get the value of motif_threshold
    result = subprocess.run(
        ["redis-cli", "GET", "motif_threshold"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, "Failed to run redis-cli GET motif_threshold."
    val = result.stdout.strip()
    # redis-cli might return '"15"' or '15', just check if it contains 15
    assert val == "15", f"Expected motif_threshold in Redis to be '15', but got '{val}'."

def test_flask_api_score_perfect_match():
    url = "http://127.0.0.1:8080/score"
    payload = {"target": "ATGCGTAC", "primer": "ATGC"}
    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Flask API at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    data = response.json()
    assert data.get("score") == 4, f"Expected score 4, got {data.get('score')}"
    assert data.get("threshold_met") is False, f"Expected threshold_met to be False, got {data.get('threshold_met')}"

def test_flask_api_score_with_mismatch():
    url = "http://127.0.0.1:8080/score"
    payload = {"target": "ATGCGTAC", "primer": "ATTC"}
    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Flask API at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    data = response.json()
    assert data.get("score") == 1, f"Expected score 1, got {data.get('score')}"
    assert data.get("threshold_met") is False, f"Expected threshold_met to be False, got {data.get('threshold_met')}"

def test_flask_api_score_threshold_met():
    url = "http://127.0.0.1:8080/score"
    # To meet threshold 15, we need 15 matches
    payload = {"target": "A"*20, "primer": "A"*15}
    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Flask API at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    data = response.json()
    assert data.get("score") == 15, f"Expected score 15, got {data.get('score')}"
    assert data.get("threshold_met") is True, f"Expected threshold_met to be True, got {data.get('threshold_met')}"

def test_c_binary_compiled():
    bin_path = "/app/bin/primer_score"
    assert os.path.isfile(bin_path), f"Compiled binary {bin_path} does not exist."
    assert os.access(bin_path, os.X_OK), f"Binary {bin_path} is not executable."