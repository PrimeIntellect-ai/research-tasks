# test_final_state.py

import os
import requests
import pytest

def test_token_file():
    path = "/home/user/token.txt"
    assert os.path.isfile(path), f"Expected {path} to exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "sup3r_s3cr3t_v2_f0r3ns1cs", f"Token file content incorrect. Got: {content}"

def test_transcript_file():
    path = "/home/user/transcript.log"
    assert os.path.isfile(path), f"Expected {path} to exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "System alert core router temperature critical", f"Transcript file content incorrect. Got: {content}"

def test_api_unauthorized():
    url = "http://127.0.0.1:8080/api/v1/transcribe"
    headers = {"Authorization": "Bearer invalid_token"}
    try:
        resp = requests.post(url, headers=headers, timeout=2)
        assert resp.status_code == 401, f"Expected 401 Unauthorized for invalid token, got {resp.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

def test_api_authorized():
    url = "http://127.0.0.1:8080/api/v1/transcribe"
    headers = {"Authorization": "Bearer sup3r_s3cr3t_v2_f0r3ns1cs"}

    wav_path = "/app/voicemail.wav"
    if os.path.exists(wav_path):
        with open(wav_path, "rb") as f:
            data = f.read()
    else:
        data = b"dummy audio data"

    try:
        # Two requests to ensure the deadlock is fixed
        for _ in range(2):
            resp = requests.post(url, headers=headers, data=data, timeout=5)
            assert resp.status_code == 200, f"Expected 200 OK for valid token, got {resp.status_code}"

            json_resp = resp.json()
            assert "transcript" in json_resp, f"Expected 'transcript' key in JSON response, got: {json_resp}"
            assert json_resp["transcript"] == "System alert core router temperature critical", f"Unexpected transcript in response: {json_resp['transcript']}"
    except requests.exceptions.Timeout:
        pytest.fail("Request timed out. The deadlock concurrency bug may not be fixed.")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")
    except ValueError:
        pytest.fail(f"Response was not valid JSON: {resp.text}")