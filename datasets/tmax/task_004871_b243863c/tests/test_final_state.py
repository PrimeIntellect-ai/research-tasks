# test_final_state.py

import os
import re
import math
import requests
import pytest

def test_debugging_report_exists():
    report_path = "/home/user/debugging_report.txt"
    assert os.path.exists(report_path), f"Debugging report {report_path} does not exist."
    assert os.path.isfile(report_path), f"{report_path} is not a file."

    with open(report_path, "r") as f:
        content = f.read().strip()

    # Check if it contains a valid git commit hash (40 hex chars)
    # The user might have written some text around it, so search for a 40-char hex string
    match = re.search(r'\b[0-9a-f]{40}\b', content)
    assert match is not None, f"Could not find a valid 40-character git commit hash in {report_path}."

def test_audio_service_endpoint():
    url = "http://127.0.0.1:9090/api/v1/analyze"
    headers = {
        "Authorization": "Bearer secret-token-8842"
    }
    audio_file_path = "/app/test_audio.wav"

    assert os.path.exists(audio_file_path), f"Audio file {audio_file_path} is missing."

    try:
        with open(audio_file_path, "rb") as f:
            files = {"audio_file": f}
            response = requests.post(url, headers=headers, files=files, timeout=10)
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to the service at 127.0.0.1:9090. Is it running?")
    except requests.exceptions.Timeout:
        pytest.fail("Request to the service timed out.")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert "transcript" in data, "Response JSON is missing 'transcript' field."
    assert "peak_frequency_hz" in data, "Response JSON is missing 'peak_frequency_hz' field."

    expected_transcript = "testing one two three regression found"
    actual_transcript = data["transcript"]

    # Allow case-insensitive matching and stripping of punctuation just in case Whisper adds slight variations
    def normalize_text(text):
        return re.sub(r'[^\w\s]', '', text.lower()).strip()

    assert normalize_text(actual_transcript) == normalize_text(expected_transcript), \
        f"Expected transcript '{expected_transcript}', got '{actual_transcript}'"

    expected_frequency = 1024.50
    actual_frequency = data["peak_frequency_hz"]

    assert isinstance(actual_frequency, (int, float)), "peak_frequency_hz must be a number."
    assert math.isclose(actual_frequency, expected_frequency, rel_tol=1e-2), \
        f"Expected peak frequency ~{expected_frequency}, got {actual_frequency}"