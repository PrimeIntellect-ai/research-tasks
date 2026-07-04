# test_final_state.py

import pytest
import requests
import hashlib

def compute_signature(timestamp: str, sensor_id: int, temperature: float) -> str:
    # Match the C binary logic: SHA256 of `<timestamp_iso8601>|<sensor_id>|<temperature>`
    payload = f"{timestamp}|{sensor_id}|{temperature}"
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()

def test_api_sensor_101():
    url = "http://127.0.0.1:8080/api/data?sensor_id=101"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    data = response.json()
    assert isinstance(data, list), "Expected API response to be a JSON array"
    assert len(data) == 5, f"Expected 5 records for sensor 101, got {len(data)}"

    expected_times = [
        "2023-10-01T10:00:00Z",
        "2023-10-01T10:05:00Z",
        "2023-10-01T10:10:00Z",
        "2023-10-01T10:15:00Z",
        "2023-10-01T10:20:00Z"
    ]
    expected_temps = [22.5, 22.6, 22.6, 22.6, 23.0]
    expected_humids = [45.0, 45.2, 45.2, 45.2, 46.0]

    for i, record in enumerate(data):
        assert record.get("timestamp") == expected_times[i], f"Mismatch in timestamp at index {i}"
        assert str(record.get("sensor_id")) == "101", f"Mismatch in sensor_id at index {i}"
        assert record.get("location") == "Warehouse_A", f"Mismatch in location at index {i}"
        assert float(record.get("temperature")) == expected_temps[i], f"Mismatch in temperature at index {i}"
        assert float(record.get("humidity")) == expected_humids[i], f"Mismatch in humidity at index {i}"

        expected_sig = compute_signature(expected_times[i], 101, expected_temps[i])
        assert record.get("signature") == expected_sig, f"Mismatch in signature at index {i}"

def test_api_sensor_102():
    url = "http://127.0.0.1:8080/api/data?sensor_id=102"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    data = response.json()
    assert isinstance(data, list), "Expected API response to be a JSON array"
    assert len(data) == 3, f"Expected 3 records for sensor 102, got {len(data)}"

    expected_times = [
        "2023-10-01T10:00:00Z",
        "2023-10-01T10:05:00Z",
        "2023-10-01T10:10:00Z"
    ]
    expected_temps = [19.0, 19.0, 19.5]
    expected_humids = [50.0, 50.0, 51.0]

    for i, record in enumerate(data):
        assert record.get("timestamp") == expected_times[i], f"Mismatch in timestamp at index {i}"
        assert str(record.get("sensor_id")) == "102", f"Mismatch in sensor_id at index {i}"
        assert record.get("location") == "Basement", f"Mismatch in location at index {i}"
        assert float(record.get("temperature")) == expected_temps[i], f"Mismatch in temperature at index {i}"
        assert float(record.get("humidity")) == expected_humids[i], f"Mismatch in humidity at index {i}"

        expected_sig = compute_signature(expected_times[i], 102, expected_temps[i])
        assert record.get("signature") == expected_sig, f"Mismatch in signature at index {i}"