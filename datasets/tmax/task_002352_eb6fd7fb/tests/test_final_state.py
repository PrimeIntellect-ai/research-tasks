# test_final_state.py
import requests
import concurrent.futures
import time
import json
import re

BASE_URL = "http://127.0.0.1:8000"
AUTH_HEADER = {"Authorization": "Bearer debug-admin-123"}

def test_auth_required():
    """Verify that the /transcribe endpoint requires the correct authorization."""
    try:
        response = requests.post(f"{BASE_URL}/transcribe", json={"file": "/app/corrupt_diag.wav"}, timeout=2)
    except requests.RequestException as e:
        assert False, f"Failed to connect to the service: {e}"

    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"

def test_concurrent_requests_no_deadlock():
    """Verify that the server can handle concurrent requests without deadlocking."""
    def make_get():
        return requests.get(f"{BASE_URL}/metrics", timeout=5)

    def make_post():
        return requests.post(
            f"{BASE_URL}/transcribe", 
            headers=AUTH_HEADER, 
            json={"file": "/dev/null"}, 
            timeout=5
        )

    tasks = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        for _ in range(10):
            tasks.append(executor.submit(make_get))
            tasks.append(executor.submit(make_post))

        try:
            results = [task.result(timeout=10) for task in tasks]
        except concurrent.futures.TimeoutError:
            assert False, "Server deadlocked or timed out under concurrent load."
        except Exception as e:
            assert False, f"Exception during concurrent requests: {e}"

    assert len(results) == 20, "Not all concurrent requests completed."

def test_transcribe_corrupt_wav():
    """Verify that the corrupted WAV file is correctly transcribed."""
    try:
        response = requests.post(
            f"{BASE_URL}/transcribe", 
            headers=AUTH_HEADER, 
            json={"file": "/app/corrupt_diag.wav"}, 
            timeout=30
        )
    except requests.RequestException as e:
        assert False, f"Failed to connect to the service: {e}"

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        assert False, f"Response was not valid JSON: {response.text}"

    assert "transcript" in data, "JSON response missing 'transcript' key."

    transcript = data["transcript"].lower()

    # Loosely match "system failure code bravo niner four"
    # Whisper might transcribe "niner" as "9" or "nine", "four" as "4"
    words = re.findall(r'[a-z0-9]+', transcript)

    assert "system" in words, f"Transcript did not contain 'system': {transcript}"
    assert "failure" in words, f"Transcript did not contain 'failure': {transcript}"
    assert "code" in words, f"Transcript did not contain 'code': {transcript}"
    assert "bravo" in words, f"Transcript did not contain 'bravo': {transcript}"
    assert "niner" in words or "9" in words or "nine" in words, f"Transcript did not contain 'niner' or '9': {transcript}"
    assert "four" in words or "4" in words, f"Transcript did not contain 'four' or '4': {transcript}"