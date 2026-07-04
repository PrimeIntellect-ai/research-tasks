# test_final_state.py

import os
import json
import pytest
import requests

NGINX_URL = "http://127.0.0.1:8080/api/transcribe"
AUTH = ("ci_runner", "build_pass_2024")
PAYLOAD = {"filepath": "/app/build_audio_test.wav"}

def test_nginx_unauthenticated_rejected():
    """Verify that the Nginx proxy rejects unauthenticated requests."""
    try:
        response = requests.post(NGINX_URL, json=PAYLOAD, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx proxy at {NGINX_URL}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"

def test_nginx_authenticated_success():
    """Verify that the Nginx proxy forwards authenticated requests to the C++ service."""
    try:
        response = requests.post(NGINX_URL, json=PAYLOAD, auth=AUTH, timeout=30)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx proxy at {NGINX_URL}: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got: {response.text}")

    assert "transcript" in data, "Response JSON missing 'transcript' key."
    transcript = data["transcript"].lower()

    expected_words = ["mobile", "build", "alpha", "seven", "two", "successful"]
    for word in expected_words:
        assert word in transcript, f"Expected word '{word}' not found in transcript: {transcript}"

def test_result_log_exists_and_correct():
    """Verify that the test pipeline script saved the correct result to result.log."""
    log_path = "/home/user/workspace/result.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing. Did you run the test pipeline script?"

    with open(log_path, "r") as f:
        content = f.read()

    try:
        data = json.loads(content)
    except ValueError:
        pytest.fail(f"Expected JSON in {log_path}, got: {content}")

    assert "transcript" in data, f"{log_path} JSON missing 'transcript' key."
    transcript = data["transcript"].lower()

    expected_words = ["mobile", "build", "alpha", "seven", "two", "successful"]
    for word in expected_words:
        assert word in transcript, f"Expected word '{word}' not found in log transcript: {transcript}"

def test_pipeline_script_exists():
    """Verify that the test_pipeline.sh script exists."""
    script_path = "/home/user/workspace/test_pipeline.sh"
    assert os.path.isfile(script_path), f"File {script_path} is missing."
    assert os.access(script_path, os.X_OK) or "curl" in open(script_path).read(), "Script should contain curl command."