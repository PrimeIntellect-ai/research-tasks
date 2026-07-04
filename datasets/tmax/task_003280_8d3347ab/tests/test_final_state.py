# test_final_state.py
import requests
import pytest

BASE_URL = "http://127.0.0.1:9090"

def test_health_endpoint():
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /health endpoint: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response from /health, got: {response.text}")

    assert data == {"status": "ok"}, f"Expected {{'status': 'ok'}}, got {data}"

def test_process_endpoint():
    csv_data = (
        "1,Alice,alice.smith@domain.com,111-22-3333\n"
        "2,Bob,bob@other.com,444-55-6666\n"
        "3,Charlie,c@test.com,777-88-9999\n"
    )

    try:
        response = requests.post(
            f"{BASE_URL}/process", 
            data=csv_data, 
            headers={"Content-Type": "text/csv"},
            timeout=10
        )
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to /process endpoint: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response from /process, got: {response.text}")

    assert isinstance(data, list), f"Expected response to be a JSON array, got {type(data)}"
    assert len(data) == 3, f"Expected exactly 3 records after deduplication, got {len(data)}"

    expected_records = [
        {"record_id": "1", "name": "Alice", "email": "a*@domain.com", "ssn": "***-**-3333"},
        {"record_id": "2", "name": "Bob", "email": "b*@other.com", "ssn": "***-**-6666"},
        {"record_id": "3", "name": "Charlie", "email": "c*@test.com", "ssn": "***-**-9999"}
    ]

    for expected, actual in zip(expected_records, data):
        assert actual.get("record_id") == expected["record_id"], f"Expected record_id {expected['record_id']}, got {actual.get('record_id')}"
        assert actual.get("name") == expected["name"], f"Expected name {expected['name']}, got {actual.get('name')}"
        assert actual.get("email") == expected["email"], f"Expected email {expected['email']}, got {actual.get('email')}"
        assert actual.get("ssn") == expected["ssn"], f"Expected ssn {expected['ssn']}, got {actual.get('ssn')}"