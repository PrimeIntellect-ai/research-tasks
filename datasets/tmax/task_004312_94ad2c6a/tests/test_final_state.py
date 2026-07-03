# test_final_state.py
import pytest
import requests

BASE_URL = "http://127.0.0.1:8080"

def test_stats_endpoint():
    """Verify the /stats endpoint returns the correct deduplication statistics."""
    try:
        response = requests.get(f"{BASE_URL}/stats", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {BASE_URL}/stats: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from /stats is not valid JSON. Response text: {response.text}")

    assert "total_unique_screens" in data, "Missing 'total_unique_screens' in /stats response"
    assert "total_deduplicated_records" in data, "Missing 'total_deduplicated_records' in /stats response"

    assert data["total_unique_screens"] == 5, f"Expected 5 unique screens, got {data['total_unique_screens']}"
    assert data["total_deduplicated_records"] == 15, f"Expected 15 deduplicated records, got {data['total_deduplicated_records']}"

def test_data_endpoint():
    """Verify the /data endpoint returns the correct deduplicated records sorted by timestamp."""
    try:
        response = requests.get(f"{BASE_URL}/data", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {BASE_URL}/data: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from /data is not valid JSON. Response text: {response.text}")

    assert isinstance(data, list), f"Expected /data to return a JSON array, got {type(data).__name__}"
    assert len(data) == 15, f"Expected 15 records in /data response, got {len(data)}"

    # Check that records are sorted by timestamp ascending
    timestamps = [record.get("timestamp", 0) for record in data]
    assert timestamps == sorted(timestamps), "Records in /data are not sorted by timestamp ascending"

    # Check that all records have the required keys
    for i, record in enumerate(data):
        assert "timestamp" in record, f"Record at index {i} missing 'timestamp'"
        assert "loc_key" in record, f"Record at index {i} missing 'loc_key'"
        assert "text" in record, f"Record at index {i} missing 'text'"