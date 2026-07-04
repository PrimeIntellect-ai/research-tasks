# test_final_state.py

import pytest
import requests
import time

def wait_for_server(url, timeout=5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            requests.get(url, timeout=1)
            return True
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
    return False

def test_http_server_running():
    """Ensure the HTTP server is listening and responding on port 9000."""
    base_url = "http://127.0.0.1:9000"
    assert wait_for_server(f"{base_url}/api/v1/record/1"), "HTTP server is not reachable on 127.0.0.1:9000"

def test_api_valid_records():
    """Check that the API returns valid decoded records for existing IDs."""
    base_url = "http://127.0.0.1:9000"

    # We expect at least ID 1 to exist based on the setup (5 rows inserted)
    for record_id in range(1, 6):
        resp = requests.get(f"{base_url}/api/v1/record/{record_id}", timeout=2)
        assert resp.status_code == 200, f"Expected HTTP 200 for ID {record_id}, got {resp.status_code}"

        data = resp.json()
        assert "id" in data, "Response missing 'id' field"
        assert "timestamp" in data, "Response missing 'timestamp' field"
        assert "decoded_data" in data, "Response missing 'decoded_data' field"

        assert data["id"] == record_id, f"Expected id {record_id}, got {data['id']}"
        assert isinstance(data["timestamp"], int), "Timestamp should be an integer"
        assert isinstance(data["decoded_data"], str), "Decoded data should be a string"

def test_api_invalid_record():
    """Check that the API returns 404 for a non-existent ID."""
    base_url = "http://127.0.0.1:9000"
    resp = requests.get(f"{base_url}/api/v1/record/9999", timeout=2)
    assert resp.status_code == 404, f"Expected HTTP 404 for non-existent ID 9999, got {resp.status_code}"