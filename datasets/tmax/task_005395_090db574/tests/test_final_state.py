# test_final_state.py

import json
import requests
import pytest

BASE_URL = "http://127.0.0.1:8080"
AUTH_TOKEN = "Bearer super-secret-etl-token"

def test_server_is_running_and_dump_accessible():
    """Verify the server is running on the correct port and /api/dump works."""
    try:
        response = requests.get(f"{BASE_URL}/api/dump", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Server is not reachable on {BASE_URL}. Error: {e}")

    assert response.status_code == 200, f"Expected 200 OK from /api/dump, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response from /api/dump is not valid JSON.")

    assert isinstance(data, dict), "Expected dump to return a JSON object (dictionary)."

def test_initial_load_stratified_data():
    """Verify that the initial data load contains the correctly stratified sample."""
    response = requests.get(f"{BASE_URL}/api/dump", timeout=2)
    data = response.json()

    txn_id = "TXN-INITIAL-LOAD"
    assert txn_id in data, f"Transaction '{txn_id}' not found in server data. Did the script run and send data?"

    records = data[txn_id]
    assert isinstance(records, list), "Expected transaction data to be a list of records."

    # Extract event_ids
    event_ids = [record.get("event_id") for record in records]

    # The expected event_ids based on the rules:
    # ja: 4 records -> top 10% ceiling(0.4) = 1. Top score is 95.5 (e1).
    # en: 11 records -> top 10% ceiling(1.1) = 2. Top scores are 100.0 (e13) and 99.0 (e12).
    expected_event_ids = {"e1", "e13", "e12"}

    assert set(event_ids) == expected_event_ids, (
        f"Incorrect stratified sample. Expected event_ids {expected_event_ids}, "
        f"but got {set(event_ids)}."
    )
    assert len(event_ids) == 3, f"Expected exactly 3 records, got {len(event_ids)}."

def test_retry_bug_is_fixed():
    """Verify that retrying a POST with the same Transaction-Id overwrites rather than appends."""
    headers = {
        "Authorization": AUTH_TOKEN,
        "Transaction-Id": "TXN-VERIFIER-TEST",
        "Content-Type": "application/json"
    }
    payload = [{"test": 1}]

    # First request
    try:
        res1 = requests.post(f"{BASE_URL}/api/ingest", headers=headers, json=payload, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"POST /api/ingest failed: {e}")

    assert res1.status_code == 200, f"Expected 200 OK on first ingest, got {res1.status_code}"

    # Second request (retry)
    res2 = requests.post(f"{BASE_URL}/api/ingest", headers=headers, json=payload, timeout=2)
    assert res2.status_code == 200, f"Expected 200 OK on retry ingest, got {res2.status_code}"

    # Check dump
    dump_res = requests.get(f"{BASE_URL}/api/dump", timeout=2)
    data = dump_res.json()

    assert "TXN-VERIFIER-TEST" in data, "Test transaction not found in dump."
    records = data["TXN-VERIFIER-TEST"]

    assert len(records) == 1, (
        f"Server retry bug is not fixed! Expected 1 record in 'TXN-VERIFIER-TEST', "
        f"but found {len(records)}. The server is likely still appending data."
    )
    assert records == payload, "Stored data does not match the payload."

def test_unauthorized_ingest_rejected():
    """Verify that /api/ingest rejects requests with invalid or missing Authorization."""
    headers = {
        "Authorization": "Bearer wrong-token",
        "Transaction-Id": "TXN-AUTH-TEST"
    }
    payload = [{"test": 2}]

    res = requests.post(f"{BASE_URL}/api/ingest", headers=headers, json=payload, timeout=2)
    assert res.status_code == 401, f"Expected 401 Unauthorized for bad token, got {res.status_code}"