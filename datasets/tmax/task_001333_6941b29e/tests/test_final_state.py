# test_final_state.py

import requests
import pytest

BASE_URL = "http://127.0.0.1:8080"
TOKEN = "blue sunrise"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def test_unauthorized_access():
    """Verify that accessing endpoints without the correct token returns 401."""
    try:
        resp = requests.get(f"{BASE_URL}/config", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {BASE_URL}: {e}")

    assert resp.status_code == 401, f"Expected 401 Unauthorized for missing token, got {resp.status_code}"

    # Test with incorrect token
    resp = requests.get(f"{BASE_URL}/config", headers={"Authorization": "Bearer wrong token"}, timeout=5)
    assert resp.status_code == 401, f"Expected 401 Unauthorized for incorrect token, got {resp.status_code}"

def test_ingest_and_data_cleaning():
    """Verify that the ingest endpoint correctly cleans data and updates state."""
    payload = [
        {"sequence": 1, "metric": 10.0, "config_hash": "abcde"},
        {"sequence": 2, "metric": None, "config_hash": "abXde"}, # Duplicate of 1 (distance 1), discarded
        {"sequence": 3, "metric": None, "config_hash": "vwxyz"}, # Kept. Metric interpolates to 20.0
        {"sequence": 4, "metric": 30.0, "config_hash": "vwxyA"}, # Duplicate of 3 (distance 1), discarded
        {"sequence": 5, "metric": 30.0, "config_hash": "pqrst"}  # Kept. Metric 30.0
    ]

    try:
        resp_post = requests.post(f"{BASE_URL}/ingest", json=payload, headers=HEADERS, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/ingest: {e}")

    assert resp_post.status_code == 200, f"Expected 200 OK from /ingest, got {resp_post.status_code}. Response: {resp_post.text}"

    try:
        resp_get = requests.get(f"{BASE_URL}/config", headers=HEADERS, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/config: {e}")

    assert resp_get.status_code == 200, f"Expected 200 OK from /config, got {resp_get.status_code}. Response: {resp_get.text}"

    try:
        data = resp_get.json()
    except ValueError:
        pytest.fail("Response from /config is not valid JSON.")

    assert isinstance(data, list), "Expected response to be a JSON array."

    # We might have run the test multiple times or just once, so we check the last 3 items if state accumulates
    # But assuming isolated state or just checking the presence of these specific sequences
    # Let's check the exact records that should have been kept from our payload

    # Filter out the items we just added based on sequence numbers (1, 3, 5)
    seq_1 = next((item for item in data if item.get("sequence") == 1), None)
    seq_3 = next((item for item in data if item.get("sequence") == 3), None)
    seq_5 = next((item for item in data if item.get("sequence") == 5), None)

    assert seq_1 is not None, "Sequence 1 is missing from the cleaned data."
    assert seq_3 is not None, "Sequence 3 is missing from the cleaned data."
    assert seq_5 is not None, "Sequence 5 is missing from the cleaned data."

    # Check that sequence 2 and 4 were discarded
    seq_2 = next((item for item in data if item.get("sequence") == 2), None)
    seq_4 = next((item for item in data if item.get("sequence") == 4), None)

    assert seq_2 is None, "Sequence 2 should have been discarded as a duplicate."
    assert seq_4 is None, "Sequence 4 should have been discarded as a duplicate."

    # Check interpolation
    assert seq_1["metric"] == 10.0, f"Expected metric 10.0 for sequence 1, got {seq_1.get('metric')}"
    assert seq_3["metric"] == 20.0, f"Expected interpolated metric 20.0 for sequence 3, got {seq_3.get('metric')}"
    assert seq_5["metric"] == 30.0, f"Expected metric 30.0 for sequence 5, got {seq_5.get('metric')}"