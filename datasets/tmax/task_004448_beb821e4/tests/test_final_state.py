# test_final_state.py

import os
import requests
import pytest

def test_extraction_service():
    """
    Test that the extraction service is running on 127.0.0.1:8000,
    accepts a POST request with the WAV file, and returns the correct flag.
    """
    audio_path = "/app/suspicious_audio.wav"
    assert os.path.isfile(audio_path), f"File {audio_path} is missing."

    with open(audio_path, "rb") as f:
        audio_data = f.read()

    url = "http://127.0.0.1:8000/analyze"

    try:
        response = requests.post(url, data=audio_data, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to the extraction service at 127.0.0.1:8000. Is the server running?")
    except requests.exceptions.Timeout:
        pytest.fail("The request to the extraction service timed out.")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred while connecting to the service: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, but got {response.status_code}. Response body: {response.text}"

    expected_flag = "FLAG{0v3rfl0w_4n4lyz3d}"
    actual_response = response.text.strip()

    assert actual_response == expected_flag, f"Expected response '{expected_flag}', but got '{actual_response}'"