# test_final_state.py
import requests
import pytest

BASE_URL = "http://127.0.0.1:9090"
ENDPOINT = f"{BASE_URL}/etl/process"
API_KEY = "etl-secret-key-998"

CSV_PAYLOAD = """record_id,event_time,message
101,2023-11-20T08:15:00Z,   Hello   World  
102,2023-11-20T08:45:00Z, FIRST   TRY
101,2023-11-20T09:05:00Z, Hello World Updated
103,2023-11-20T09:10:00Z,   New   Line \n \t Test  
102,2023-11-20T08:45:00Z, FIRST   TRY
"""

EXPECTED_RESPONSE = {
  "2023-11-20T08": [
    {
      "record_id": "102",
      "event_time": "2023-11-20T08:45:00Z",
      "message": "first try"
    }
  ],
  "2023-11-20T09": [
    {
      "record_id": "101",
      "event_time": "2023-11-20T09:05:00Z",
      "message": "hello world updated"
    },
    {
      "record_id": "103",
      "event_time": "2023-11-20T09:10:00Z",
      "message": "new line test"
    }
  ]
}

def sort_bucket(bucket):
    return sorted(bucket, key=lambda x: x["record_id"])

def test_missing_auth():
    try:
        response = requests.post(ENDPOINT, data=CSV_PAYLOAD.encode("utf-16le"), headers={"Content-Type": "text/csv; charset=utf-16le"})
    except requests.exceptions.ConnectionError:
        pytest.fail("Server is not running or not listening on 127.0.0.1:9090")

    assert response.status_code == 401, f"Expected 401 Unauthorized for missing API key, got {response.status_code}"

def test_incorrect_auth():
    headers = {
        "X-API-Key": "wrong-key",
        "Content-Type": "text/csv; charset=utf-16le"
    }
    response = requests.post(ENDPOINT, data=CSV_PAYLOAD.encode("utf-16le"), headers=headers)
    assert response.status_code == 401, f"Expected 401 Unauthorized for incorrect API key, got {response.status_code}"

def test_successful_processing():
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "text/csv; charset=utf-16le"
    }
    response = requests.post(ENDPOINT, data=CSV_PAYLOAD.encode("utf-16le"), headers=headers)

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    # Normalize expected and actual data for comparison
    actual_normalized = {k: sort_bucket(v) for k, v in data.items()}
    expected_normalized = {k: sort_bucket(v) for k, v in EXPECTED_RESPONSE.items()}

    assert actual_normalized == expected_normalized, f"Response JSON does not match expected output.\nExpected: {expected_normalized}\nActual: {actual_normalized}"