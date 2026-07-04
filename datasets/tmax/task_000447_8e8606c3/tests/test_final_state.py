# test_final_state.py
import os
import pytest
import requests

def test_env_file_recovered():
    """Verify that the SECRET_SALT was recovered and placed in .env."""
    env_path = "/home/user/app/.env"
    assert os.path.isfile(env_path), f"File {env_path} does not exist."

    with open(env_path, "r") as f:
        content = f.read()

    assert "SECRET_SALT=42" in content, "SECRET_SALT=42 is missing from the .env file."

def test_server_processing_and_fd_leak_fixed():
    """
    Verify that the server is running, correctly processes the audio,
    and survives more than 10 requests (proving the FD leak is fixed).
    """
    url = "http://127.0.0.1:8080/process"
    audio_path = "/app/test_audio.wav"

    assert os.path.isfile(audio_path), f"Test audio file {audio_path} is missing."

    with open(audio_path, "rb") as f:
        audio_data = f.read()

    results = set()

    # Send 15 requests. If the FD leak is not fixed, it will fail after 10 requests.
    for i in range(15):
        try:
            response = requests.post(url, data=audio_data, timeout=5)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Request {i+1}/15 failed: {e}. The server might have crashed due to the FD leak.")

        assert response.status_code == 200, f"Request {i+1}/15 returned status {response.status_code}: {response.text}"

        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"Request {i+1}/15 did not return valid JSON. Response: {response.text}")

        assert "result" in data, f"Response JSON missing 'result' key: {data}"
        results.add(data["result"])

    # The result should be deterministic for the same audio input
    assert len(results) == 1, f"Expected consistent results across requests, but got multiple: {results}"