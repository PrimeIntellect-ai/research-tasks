# test_final_state.py
import os
import re
import requests
import pytest

def test_bad_commit_file_exists_and_valid():
    """Check that the bad_commit.txt file exists and contains a valid git hash."""
    bad_commit_path = "/home/user/bad_commit.txt"
    assert os.path.isfile(bad_commit_path), f"File {bad_commit_path} does not exist. You must write the bad commit hash to this file."

    with open(bad_commit_path, "r") as f:
        content = f.read().strip()

    assert re.match(r"^[0-9a-f]{40}$", content), f"File {bad_commit_path} does not contain a valid 40-character git commit hash. Found: {content}"

def test_server_metrics_endpoint():
    """Check that the server is running and the metrics endpoint returns the correct response."""
    url = "http://127.0.0.1:8080/api/v1/metrics"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}. Is the server running in the background? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP status code 200, got {response.status_code}. Response: {response.text}"
    assert response.text.strip() == "Metrics OK", f"Expected response body 'Metrics OK', got '{response.text}'"