# test_final_state.py
import requests
import pytest

API_URL = "http://127.0.0.1:8555/api/dataset/sample_features"
SECRET_TOKEN = "Bearer ds-research-secret"

def test_api_unauthorized_missing_header():
    """Test that the API rejects requests without the Authorization header."""
    try:
        response = requests.get(API_URL, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to the API. Is the server running on 127.0.0.1:8555?")

    assert response.status_code in (401, 403), f"Expected 401 or 403 for missing auth, got {response.status_code}"

def test_api_unauthorized_wrong_header():
    """Test that the API rejects requests with an incorrect Authorization header."""
    headers = {"Authorization": "Bearer wrong-secret"}
    try:
        response = requests.get(API_URL, headers=headers, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to the API. Is the server running on 127.0.0.1:8555?")

    assert response.status_code in (401, 403), f"Expected 401 or 403 for wrong auth, got {response.status_code}"

def test_api_authorized_response_structure():
    """Test that the API returns the correct JSON structure when authorized."""
    headers = {"Authorization": SECRET_TOKEN}
    try:
        response = requests.get(API_URL, headers=headers, timeout=15)
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to the API. Is the server running on 127.0.0.1:8555?")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    # Check top-level keys
    assert "audio_stats" in data, "Missing 'audio_stats' in response"
    assert "transcription" in data, "Missing 'transcription' in response"
    assert "tokens" in data, "Missing 'tokens' in response"

    # Check audio_stats structure and types
    audio_stats = data["audio_stats"]
    assert isinstance(audio_stats, dict), "'audio_stats' must be a dictionary"
    assert "mean" in audio_stats, "Missing 'mean' in audio_stats"
    assert "variance" in audio_stats, "Missing 'variance' in audio_stats"
    assert "rms_mean" in audio_stats, "Missing 'rms_mean' in audio_stats"

    assert isinstance(audio_stats["mean"], (int, float)), "'mean' must be a number"
    assert isinstance(audio_stats["variance"], (int, float)), "'variance' must be a number"
    assert isinstance(audio_stats["rms_mean"], (int, float)), "'rms_mean' must be a number"

    # Check transcription type
    assert isinstance(data["transcription"], str), "'transcription' must be a string"
    assert len(data["transcription"]) > 0, "'transcription' should not be empty"

    # Check tokens type
    assert isinstance(data["tokens"], list), "'tokens' must be a list"
    assert len(data["tokens"]) > 0, "'tokens' list should not be empty"
    assert all(isinstance(t, int) for t in data["tokens"]), "All items in 'tokens' must be integers"