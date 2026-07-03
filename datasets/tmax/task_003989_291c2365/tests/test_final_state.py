# test_final_state.py

import os
import json
import hashlib
import requests
import pytest

AUDIO_DEST = "/home/user/organized_data/interview_sample.wav"
MANIFEST_PATH = "/home/user/organized_data/manifest.json"
API_URL = "http://127.0.0.1:9090/api/v1/record"
AUTH_HEADER = {"Authorization": "Bearer delta-v-2024"}

def get_sha256(path):
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def test_audio_copied():
    assert os.path.isfile(AUDIO_DEST), f"Audio file not copied to {AUDIO_DEST}"

def test_manifest_exists_and_valid():
    assert os.path.isfile(MANIFEST_PATH), f"Manifest file missing at {MANIFEST_PATH}"
    with open(MANIFEST_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Manifest is not valid JSON")

    assert isinstance(data, list), "Manifest must be a JSON array"

    item = next((x for x in data if x.get("filename") == "interview_sample.wav"), None)
    assert item is not None, "Manifest missing entry for interview_sample.wav"

    expected_keys = {"filename", "checksum", "participant_id", "location", "transcript"}
    assert set(item.keys()) == expected_keys, f"Manifest entry keys mismatch. Expected {expected_keys}, got {set(item.keys())}"

    assert item["participant_id"] == "P-8842", f"Expected participant_id P-8842, got {item['participant_id']}"
    assert item["location"] == "Clinic B", f"Expected location Clinic B, got {item['location']}"

    actual_checksum = get_sha256(AUDIO_DEST)
    assert item["checksum"] == actual_checksum, f"Checksum in manifest ({item['checksum']}) does not match actual file checksum ({actual_checksum})"

    transcript = item["transcript"].lower()
    for word in ["patient", "exhibits", "mild", "symptoms"]:
        assert word in transcript, f"Transcript missing expected word: '{word}'. Actual transcript: {transcript}"

def test_api_unauthorized():
    try:
        response = requests.get(f"{API_URL}?file=interview_sample.wav", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized without auth header, got {response.status_code}"

def test_api_authorized():
    try:
        response = requests.get(f"{API_URL}?file=interview_sample.wav", headers=AUTH_HEADER, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK with auth header, got {response.status_code}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail("API response is not valid JSON")

    assert data.get("filename") == "interview_sample.wav", "API response filename mismatch"
    assert data.get("participant_id") == "P-8842", "API response participant_id mismatch"
    assert data.get("location") == "Clinic B", "API response location mismatch"

    actual_checksum = get_sha256(AUDIO_DEST)
    assert data.get("checksum") == actual_checksum, "API response checksum does not match actual file checksum"

    transcript = data.get("transcript", "").lower()
    for word in ["patient", "exhibits", "mild", "symptoms"]:
        assert word in transcript, f"API Transcript missing expected word: '{word}'. Actual: {transcript}"