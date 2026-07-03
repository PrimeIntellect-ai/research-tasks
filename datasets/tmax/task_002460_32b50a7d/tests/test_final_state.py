# test_final_state.py
import requests
import pytest
import time

def test_ingest_endpoint():
    url = "http://127.0.0.1:8080/ingest"

    # Wait for the service to be ready
    max_retries = 5
    for _ in range(max_retries):
        try:
            requests.get("http://127.0.0.1:8080/")
            break
        except requests.exceptions.ConnectionError:
            time.sleep(1)

    payload = """[2023-10-14T08:30:00Z] SENSOR_1 msg_id=a1 temp=24.5
[2023-10-14T08:30:00Z] SENSOR_2 msg_id=a2 temp=24.1
[2023-10-14T08:30:00Z] SENSOR_2 msg_id=a2 temp=30.0
[2023-10-14T08:30:01Z] SENSOR_3 msg_id=a3 temp=26.8
[2023-10-14T08:30:03Z] SENSOR_4 msg_id=a4 temp=26.1"""

    try:
        response = requests.post(url, data=payload, headers={"Content-Type": "text/plain"}, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to the Rust service at 127.0.0.1:8080. Is it running?")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response: {response.text}")

    expected_data = [
        {"time": "2023-10-14T08:30:00Z", "avg_temp": 24.3},
        {"time": "2023-10-14T08:30:01Z", "avg_temp": 24.3},
        {"time": "2023-10-14T08:30:02Z", "avg_temp": 24.3},
        {"time": "2023-10-14T08:30:03Z", "avg_temp": 26.1}
    ]

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} records, got {len(data)}"

    for i, expected in enumerate(expected_data):
        actual = data[i]
        assert actual["time"] == expected["time"], f"Mismatch in time at index {i}. Expected {expected['time']}, got {actual.get('time')}"
        assert abs(actual["avg_temp"] - expected["avg_temp"]) < 0.01, f"Mismatch in avg_temp at index {i}. Expected {expected['avg_temp']}, got {actual.get('avg_temp')}"