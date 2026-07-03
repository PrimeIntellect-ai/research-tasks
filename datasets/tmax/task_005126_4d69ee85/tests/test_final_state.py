# test_final_state.py

import os
import json
import csv
import subprocess
import requests
import pytest
from collections import defaultdict

def get_expected_data():
    data = defaultdict(list)
    raw_dir = "/home/user/raw_data"
    for root, _, files in os.walk(raw_dir):
        for f in files:
            path = os.path.join(root, f)
            if f.endswith('.csv'):
                with open(path, 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        # date, time, sensor, reading
                        ts = f"{row['date'].strip()}T{row['time'].strip()}"
                        data[row['sensor'].strip()].append({"timestamp": ts, "value": float(row['reading'])})
            elif f.endswith('.json'):
                with open(path, 'r') as jsonfile:
                    try:
                        content = json.load(jsonfile)
                        for item in content:
                            data[item['sensor_id']].append({"timestamp": item['ts'], "value": float(item['val'])})
                    except Exception:
                        pass
            elif f.endswith('.log'):
                with open(path, 'r') as logfile:
                    records = logfile.read().strip().split('---RECORD---')
                    for record in records:
                        if not record.strip(): 
                            continue
                        ts = None
                        sid = None
                        val = None
                        for line in record.split('\n'):
                            line = line.strip()
                            if line.startswith('TS:'): 
                                ts = line.split(':', 1)[1].strip()
                            elif line.startswith('ID:'): 
                                sid = line.split(':', 1)[1].strip()
                            elif line.startswith('VAL:'): 
                                val = float(line.split(':', 1)[1].strip())
                        if ts and sid and val is not None:
                            data[sid].append({"timestamp": ts, "value": val})
            elif f.endswith('.dat'):
                try:
                    out = subprocess.check_output(['/app/sensor_decoder', path], text=True)
                    content = json.loads(out)
                    for item in content:
                        data[item['sensor']].append({"timestamp": item['timestamp'], "value": float(item['reading'])})
                except Exception:
                    pass

    for sid in data:
        data[sid].sort(key=lambda x: x['timestamp'])
    return data

@pytest.fixture(scope="module")
def expected_data():
    return get_expected_data()

def test_auth_missing():
    response = requests.get("http://127.0.0.1:8080/query?sensor=test")
    assert response.status_code == 401, "Expected 401 Unauthorized when auth header is missing"

def test_auth_invalid():
    headers = {"Authorization": "Bearer WRONG-TOKEN"}
    response = requests.get("http://127.0.0.1:8080/query?sensor=test", headers=headers)
    assert response.status_code == 401, "Expected 401 Unauthorized when auth header is incorrect"

def test_sensor_not_found():
    headers = {"Authorization": "Bearer RES-992"}
    response = requests.get("http://127.0.0.1:8080/query?sensor=NON_EXISTENT_SENSOR_999", headers=headers)
    assert response.status_code == 200, "Expected 200 OK for non-existent sensor"
    assert response.json() == [], "Expected empty JSON array for non-existent sensor"

def test_sensor_data(expected_data):
    assert expected_data, "No expected data found to test against. Check raw data parsing."
    headers = {"Authorization": "Bearer RES-992"}

    for sensor_id, expected_records in expected_data.items():
        response = requests.get(f"http://127.0.0.1:8080/query?sensor={sensor_id}", headers=headers)
        assert response.status_code == 200, f"Expected 200 OK for sensor {sensor_id}"

        actual_records = response.json()
        assert isinstance(actual_records, list), "Response must be a JSON array"

        # Check counts
        assert len(actual_records) == len(expected_records), f"Mismatch in number of records for sensor {sensor_id}"

        # Check values and sorting
        for actual, expected in zip(actual_records, expected_records):
            assert "timestamp" in actual, "Missing 'timestamp' in response object"
            assert "value" in actual, "Missing 'value' in response object"
            assert actual["timestamp"] == expected["timestamp"], f"Timestamp mismatch for sensor {sensor_id}"
            assert abs(float(actual["value"]) - expected["value"]) < 1e-5, f"Value mismatch for sensor {sensor_id}"