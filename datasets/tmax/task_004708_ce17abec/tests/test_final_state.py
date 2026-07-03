# test_final_state.py

import os
import time
import subprocess
import requests
import pytest

@pytest.fixture(scope="session", autouse=True)
def ensure_service_running():
    """Ensure the service is running by invoking /app/start.sh if needed."""
    # Check if port 8080 is open
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("127.0.0.1", 8080))
        s.close()
        return
    except ConnectionRefusedError:
        pass

    # If not running, execute /app/start.sh
    if os.path.exists("/app/start.sh"):
        subprocess.Popen(["bash", "/app/start.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Wait for the service to come up
        for _ in range(30):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("127.0.0.1", 8080))
                s.close()
                time.sleep(1) # wait a bit more for the server to be fully ready
                return
            except ConnectionRefusedError:
                time.sleep(1)
        pytest.fail("Service on port 8080 did not start after running /app/start.sh")
    else:
        pytest.fail("/app/start.sh does not exist")

def test_database_index_created():
    """Verify that the idx_manager_id index was created on the employees table."""
    # Query pg_indexes to check for the index
    cmd = [
        "psql", "-U", "postgres", "-d", "company", "-tA", "-c",
        "SELECT indexname FROM pg_indexes WHERE tablename = 'employees' AND indexname = 'idx_manager_id';"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to query database: {result.stderr}"
    assert "idx_manager_id" in result.stdout, "The index 'idx_manager_id' was not found on the employees table."

def test_api_subordinates_response():
    """Verify that the API returns the correct recursive subordinates."""
    try:
        response = requests.get("http://127.0.0.1:8080/api/subordinates?manager_id=1", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP request failed: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Expected Content-Type: application/json, got {content_type}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert isinstance(data, list), "Expected response body to be a JSON array."

    expected = [
        {"id": 1, "name": "Alice", "depth": 0},
        {"id": 2, "name": "Bob", "depth": 1},
        {"id": 4, "name": "Diana", "depth": 1},
        {"id": 3, "name": "Charlie", "depth": 2},
        {"id": 5, "name": "Eve", "depth": 2}
    ]

    # Sort both lists by id to compare
    data_sorted = sorted(data, key=lambda x: x.get("id", 0))
    expected_sorted = sorted(expected, key=lambda x: x["id"])

    assert len(data_sorted) == len(expected_sorted), f"Expected {len(expected_sorted)} records, got {len(data_sorted)}"

    for actual_item, expected_item in zip(data_sorted, expected_sorted):
        assert actual_item.get("id") == expected_item["id"], f"Expected id {expected_item['id']}, got {actual_item.get('id')}"
        assert actual_item.get("name") == expected_item["name"], f"Expected name {expected_item['name']}, got {actual_item.get('name')}"
        assert actual_item.get("depth") == expected_item["depth"], f"Expected depth {expected_item['depth']}, got {actual_item.get('depth')}"