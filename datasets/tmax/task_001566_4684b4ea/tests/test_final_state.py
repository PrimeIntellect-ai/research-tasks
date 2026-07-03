# test_final_state.py
import csv
import json
import subprocess
import time
from datetime import datetime, timezone
import pytest
import requests

def get_expected_distance(details):
    out = subprocess.check_output(["/app/log_distance", "root shell attempt", details])
    return float(out.strip())

def parse_timestamp(ts_str):
    try:
        # Try epoch
        ts = float(ts_str)
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    except ValueError:
        # Try MM/DD/YYYY HH:MM:SS
        dt = datetime.strptime(ts_str, "%m/%d/%Y %H:%M:%S").replace(tzinfo=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def get_expected_logs(max_distance):
    logs = []
    with open("/home/user/logs.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dist = get_expected_distance(row["details"])
            if dist <= max_distance:
                logs.append({
                    "timestamp": parse_timestamp(row["raw_timestamp"]),
                    "ip": "X.X.X.X",
                    "action": row["action"],
                    "distance": dist
                })
    # Sort by timestamp ascending
    logs.sort(key=lambda x: x["timestamp"])
    return logs

def test_api_anomalies_endpoint():
    """Test the /api/anomalies endpoint with max_distance=1.5"""
    max_dist = 1.5
    url = f"http://127.0.0.1:8080/api/anomalies?max_distance={max_dist}"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got: {response.text}")

    expected_data = get_expected_logs(max_dist)

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} logs, got {len(data)}"

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert actual["timestamp"] == expected["timestamp"], f"Log {i} timestamp mismatch: expected {expected['timestamp']}, got {actual.get('timestamp')}"
        assert actual["ip"] == expected["ip"], f"Log {i} IP mismatch: expected {expected['ip']}, got {actual.get('ip')}"
        assert actual["action"] == expected["action"], f"Log {i} action mismatch: expected {expected['action']}, got {actual.get('action')}"
        assert abs(float(actual["distance"]) - expected["distance"]) < 0.01, f"Log {i} distance mismatch: expected {expected['distance']}, got {actual.get('distance')}"

def test_api_anomalies_endpoint_strict():
    """Test the /api/anomalies endpoint with max_distance=0.1"""
    max_dist = 0.1
    url = f"http://127.0.0.1:8080/api/anomalies?max_distance={max_dist}"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got: {response.text}")

    expected_data = get_expected_logs(max_dist)

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} logs for max_distance={max_dist}, got {len(data)}"