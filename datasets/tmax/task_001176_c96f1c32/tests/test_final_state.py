# test_final_state.py

import pytest
import requests
import re

BASE_URL = "http://127.0.0.1:8000"

def test_api_transcript():
    try:
        response = requests.get(f"{BASE_URL}/api/transcript", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /api/transcript: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response from /api/transcript is not valid JSON")

    assert "transcript" in data, "Response JSON missing 'transcript' key"

    transcript = data["transcript"].lower()
    # Remove punctuation for comparison
    transcript_clean = re.sub(r'[^\w\s]', '', transcript)

    assert "cluster delta prime" in transcript_clean, f"Expected 'cluster delta prime' in transcript, got: {transcript}"

def test_api_match_cluster_delta_prime():
    payload = {"query": "cluster delta prime"}
    try:
        response = requests.post(f"{BASE_URL}/api/match", json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /api/match: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response from /api/match is not valid JSON")

    assert "closest_match" in data, "Response JSON missing 'closest_match' key"
    assert "distance" in data, "Response JSON missing 'distance' key"

    assert data["closest_match"] == "cluster-delta-prime", f"Expected closest_match 'cluster-delta-prime', got {data['closest_match']}"
    assert data["distance"] == 2, f"Expected distance 2, got {data['distance']}"

def test_api_match_alpha_node_1():
    payload = {"query": "alpha node 1"}
    try:
        response = requests.post(f"{BASE_URL}/api/match", json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /api/match: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response from /api/match is not valid JSON")

    assert "closest_match" in data, "Response JSON missing 'closest_match' key"
    assert "distance" in data, "Response JSON missing 'distance' key"

    assert data["closest_match"] == "alpha-node-01", f"Expected closest_match 'alpha-node-01', got {data['closest_match']}"
    assert data["distance"] == 3, f"Expected distance 3, got {data['distance']}"