# test_final_state.py
import pytest
import requests
import math
import binascii
import json

URL = "http://127.0.0.1:8080/process"

def encode_payload(temp, pressure, humidity):
    payload_str = json.dumps({"temp": temp, "pressure": pressure, "humidity": humidity})
    return binascii.hexlify(payload_str.encode('utf-8')).decode('utf-8')

def test_process_deviation_alert():
    # Test case with distance > 10.0
    payload = encode_payload(35.0, 1020.0, 45.0)
    req_data = {
        "timestamp": "2024-01-01T10:13:45Z",
        "payload": payload
    }

    try:
        response = requests.post(URL, json=req_data, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the middleware service at {URL}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data.get("bucket") == "2024-01-01T10:10:00Z", f"Incorrect bucket. Got: {data.get('bucket')}"
    assert data.get("distance") == 17.19, f"Incorrect distance. Got: {data.get('distance')}"
    expected_alert = "ALERT: Deviation of 17.19 detected at 2024-01-01T10:10:00Z."
    assert data.get("alert") == expected_alert, f"Incorrect alert. Got: {data.get('alert')}"

def test_process_no_deviation():
    # Test case with distance <= 10.0
    payload = encode_payload(20.0, 1013.25, 50.0)
    req_data = {
        "timestamp": "2024-02-29T23:59:59Z",
        "payload": payload
    }

    try:
        response = requests.post(URL, json=req_data, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the middleware service at {URL}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data.get("bucket") == "2024-02-29T23:55:00Z", f"Incorrect bucket. Got: {data.get('bucket')}"
    assert data.get("distance") == 0.0, f"Incorrect distance. Got: {data.get('distance')}"
    assert data.get("alert") is None, f"Alert should be null. Got: {data.get('alert')}"

def test_process_bucketing_edge_cases():
    # Test exact bucket time
    payload = encode_payload(22.0, 1010.0, 55.0)
    req_data = {
        "timestamp": "2023-10-01T12:00:00Z",
        "payload": payload
    }

    response = requests.post(URL, json=req_data, timeout=5)
    assert response.status_code == 200
    data = response.json()
    assert data.get("bucket") == "2023-10-01T12:00:00Z"

    # Test just before next bucket
    req_data["timestamp"] = "2023-10-01T12:04:59Z"
    response = requests.post(URL, json=req_data, timeout=5)
    assert response.status_code == 200
    data = response.json()
    assert data.get("bucket") == "2023-10-01T12:00:00Z"