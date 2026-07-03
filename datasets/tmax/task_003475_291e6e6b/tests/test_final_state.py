# test_final_state.py

import os
import requests
import pytest
import time

def test_telemetry_mock_exists():
    path = "/home/user/pipeline/telemetry_mock.c"
    assert os.path.isfile(path), f"File {path} is missing. Did you implement the test mock?"

def test_audio_server_binary_exists():
    path = "/home/user/pipeline/audio_server"
    assert os.path.isfile(path), f"File {path} is missing. Did you successfully compile the application?"

def test_health_endpoint():
    try:
        response = requests.get("http://127.0.0.1:9090/health", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the audio_server on 127.0.0.1:9090. Is it running? Error: {e}")

    assert response.status_code == 200, f"Expected 200 OK for /health, got {response.status_code}"
    assert "OK" in response.text, f"Expected 'OK' in /health response body, got: {response.text}"

def test_transcript_endpoint_auth_failure():
    try:
        response = requests.get("http://127.0.0.1:9090/transcript", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the audio_server on 127.0.0.1:9090. Error: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for /transcript without auth, got {response.status_code}"

def test_transcript_endpoint_success():
    headers = {"Authorization": "Bearer ci_pipeline_token"}
    try:
        response = requests.get("http://127.0.0.1:9090/transcript", headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the audio_server on 127.0.0.1:9090. Error: {e}")

    assert response.status_code == 200, f"Expected 200 OK for /transcript with valid auth, got {response.status_code}"

    expected_text = "System update required for nodes alpha and beta."

    # Clean up both texts for a robust comparison
    actual_clean = ''.join(c.lower() for c in response.text if c.isalnum() or c.isspace()).strip()
    expected_clean = ''.join(c.lower() for c in expected_text if c.isalnum() or c.isspace()).strip()

    assert expected_clean in actual_clean, f"Expected transcript to contain '{expected_clean}', but got '{actual_clean}'"