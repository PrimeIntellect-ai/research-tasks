# test_final_state.py
import pytest
import requests
import os

def test_predict_intent_endpoint():
    """Test the /predict_intent endpoint with the provided support_call.wav."""
    url = "http://127.0.0.1:5000/predict_intent"
    wav_path = "/app/support_call.wav"

    assert os.path.isfile(wav_path), f"Test file {wav_path} is missing."

    with open(wav_path, "rb") as f:
        audio_data = f.read()

    try:
        response = requests.post(
            url,
            data=audio_data,
            headers={"Content-Type": "audio/wav"},
            timeout=30
        )
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Failed to connect to the service at {url}. Is the server running?")
    except requests.exceptions.Timeout:
        pytest.fail(f"Request to {url} timed out.")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response body: {response.text}")

    assert "transcription" in data, "Response JSON missing 'transcription' key."
    assert "intent" in data, "Response JSON missing 'intent' key."

    # Check intent prediction
    expected_intent = "password_reset"
    actual_intent = data["intent"]
    assert actual_intent == expected_intent, f"Expected intent '{expected_intent}', got '{actual_intent}'."

    # Basic check on transcription
    transcription = data["transcription"].lower()
    assert "password" in transcription, f"Expected 'password' in transcription, got '{data['transcription']}'"