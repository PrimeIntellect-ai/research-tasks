# test_final_state.py

import requests
import csv
import io
import pytest

BASE_URL = "http://127.0.0.1:8000"
TOKEN = "EchoTango77"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def test_unauthorized_access():
    """Test that endpoints require authentication."""
    try:
        response = requests.get(f"{BASE_URL}/export", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API: {e}")

    assert response.status_code in (401, 403), f"Expected 401 or 403 for unauthorized access, got {response.status_code}"

def test_shortest_path():
    """Test the shortest path endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/path?source=Gateway&target=DB_Main", headers=HEADERS, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "path" in data, "Response JSON missing 'path' key"
    assert "total_latency" in data, "Response JSON missing 'total_latency' key"

    assert data["path"] == ["Gateway", "AuthService", "Cache", "DB_Main"], f"Incorrect path: {data['path']}"
    assert data["total_latency"] == 35, f"Incorrect total_latency: {data['total_latency']}"

def test_csv_export():
    """Test the CSV export endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/export", headers=HEADERS, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    content_type = response.headers.get("Content-Type", "")
    assert "csv" in content_type.lower() or "text" in content_type.lower(), f"Expected CSV content type, got {content_type}"

    reader = csv.reader(io.StringIO(response.text.strip()))
    rows = list(reader)

    assert len(rows) >= 5, f"Expected at least 5 rows (header + 4 data rows), got {len(rows)}"

    assert rows[0] == ["node_name", "total_outgoing_latency"], f"Incorrect CSV header: {rows[0]}"

    expected_data = [
        ["Gateway", "110"],
        ["AuthService", "55"],
        ["Cache", "20"],
        ["DB_Main", "0"]
    ]

    for i, expected_row in enumerate(expected_data):
        assert rows[i+1] == expected_row, f"Row {i+1} mismatch: expected {expected_row}, got {rows[i+1]}"