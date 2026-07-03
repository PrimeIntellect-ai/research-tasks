# test_final_state.py

import json
import re
import requests
import pytest

BASE_URL = "http://127.0.0.1:8080"

def normalize_text(text):
    # Convert to lowercase and remove punctuation
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def test_anomalies_endpoint():
    try:
        response = requests.get(f"{BASE_URL}/anomalies", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/anomalies: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from /anomalies is not valid JSON. Response text: {response.text}")

    expected_anomalies = [
        "2024-01-05T08:30:00Z",
        "2024-01-15T09:11:00Z"
    ]

    assert isinstance(data, list), f"Expected JSON array, got {type(data)}"
    assert data == expected_anomalies, f"Anomalies mismatch. Expected {expected_anomalies}, got {data}"

def test_transcript_endpoint():
    try:
        response = requests.get(f"{BASE_URL}/transcript", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/transcript: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from /transcript is not valid JSON. Response text: {response.text}")

    assert isinstance(data, dict), f"Expected JSON object, got {type(data)}"
    assert "transcript" in data, "Key 'transcript' missing from JSON response."

    actual_transcript = data["transcript"]
    assert isinstance(actual_transcript, str), "Transcript value must be a string."

    expected_transcript = "the primary sensor malfunctioned due to wildlife interference"

    norm_actual = normalize_text(actual_transcript)
    norm_expected = normalize_text(expected_transcript)

    actual_words = norm_actual.split()
    expected_words = norm_expected.split()

    # Calculate simple word error rate or just check if enough words match
    # We'll check if at least 80% of expected words are present in the actual transcript
    matched_words = [word for word in expected_words if word in actual_words]
    match_ratio = len(matched_words) / len(expected_words)

    assert match_ratio >= 0.8, (
        f"Transcript does not match closely enough. "
        f"Expected: '{expected_transcript}', Actual: '{actual_transcript}'"
    )