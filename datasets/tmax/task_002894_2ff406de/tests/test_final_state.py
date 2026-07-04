# test_final_state.py

import json
import pytest
import requests

BASE_URL = "http://127.0.0.1:8080"

def test_stats_endpoint():
    """Verify the /stats endpoint returns the correct summary statistics."""
    try:
        response = requests.get(f"{BASE_URL}/stats", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /stats endpoint: {e}")

    assert response.status_code == 200, f"Expected status code 200 for /stats, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from /stats is not valid JSON. Response text: {response.text}")

    assert "total_raw" in data, "Missing 'total_raw' in /stats response"
    assert data["total_raw"] == 10, f"Expected total_raw to be 10, got {data['total_raw']}"

    assert "total_cleaned" in data, "Missing 'total_cleaned' in /stats response"
    assert data["total_cleaned"] == 7, f"Expected total_cleaned to be 7, got {data['total_cleaned']}"

    assert "removed_ids" in data, "Missing 'removed_ids' in /stats response"
    removed_ids = sorted(data["removed_ids"])
    assert removed_ids == [4, 5, 8], f"Expected removed_ids to be [4, 5, 8], got {removed_ids}"

def test_cleaned_endpoint():
    """Verify the /cleaned endpoint returns the deduplicated and masked JSONL data."""
    try:
        response = requests.get(f"{BASE_URL}/cleaned", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /cleaned endpoint: {e}")

    assert response.status_code == 200, f"Expected status code 200 for /cleaned, got {response.status_code}"

    lines = [line for line in response.text.split("\n") if line.strip()]
    assert len(lines) == 7, f"Expected 7 records in /cleaned response, got {len(lines)}"

    expected_ids = {1, 2, 3, 6, 7, 9, 10}
    received_ids = set()

    for i, line in enumerate(lines):
        try:
            record = json.loads(line)
        except ValueError:
            pytest.fail(f"Line {i+1} in /cleaned response is not valid JSON: {line}")

        assert "id" in record, f"Missing 'id' in record: {record}"
        received_ids.add(record["id"])

        assert "email" in record, f"Missing 'email' in record: {record}"
        email = record["email"]
        assert email.startswith("[MASKED]@"), f"Email '{email}' is not properly masked. Expected prefix '[MASKED]@'."

    assert received_ids == expected_ids, f"Expected IDs {expected_ids} in cleaned data, but got {received_ids}"