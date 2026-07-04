# test_final_state.py

import os
import csv
import binascii
import subprocess
import requests
import pytest
from collections import defaultdict

def get_expected_data():
    hourly_temps = defaultdict(list)
    csv_path = '/home/user/data/telemetry.csv'

    if not os.path.exists(csv_path):
        return {}

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ts = row['timestamp']
            hour_bucket = ts[:13] + ":00:00Z"
            hex_payload = row['raw_payload']

            try:
                raw_bytes = binascii.unhexlify(hex_payload)
                decoded = raw_bytes.decode('utf-8', errors='ignore')
            except Exception:
                continue

            try:
                out = subprocess.check_output(['/app/log_decoder', decoded]).decode('utf-8')
                parts = out.strip().split('|')
                for p in parts:
                    if p.startswith('CPU_TEMP='):
                        temp = float(p.split('=')[1])
                        hourly_temps[hour_bucket].append(temp)
            except Exception:
                continue

    avg_temps = {}
    for h, temps in hourly_temps.items():
        if temps:
            avg_temps[h] = round(sum(temps) / len(temps), 2)
    return avg_temps

@pytest.fixture(scope="module")
def expected_data():
    return get_expected_data()

def test_api_valid_hours(expected_data):
    assert expected_data, "No expected data could be generated from the CSV."

    base_url = "http://127.0.0.1:8080/api/temperature"

    for hour, expected_temp in expected_data.items():
        try:
            response = requests.get(f"{base_url}?hour={hour}", timeout=5)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to API for hour {hour}: {e}")

        assert response.status_code == 200, f"Expected status code 200 for hour {hour}, got {response.status_code}"

        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"Response for hour {hour} is not valid JSON. Response text: {response.text}")

        assert "hour" in data, f"Missing 'hour' key in JSON response for {hour}"
        assert data["hour"] == hour, f"Expected hour {hour}, got {data['hour']}"

        assert "avg_cpu_temp" in data, f"Missing 'avg_cpu_temp' key in JSON response for {hour}"
        actual_temp = data["avg_cpu_temp"]

        # Allow small floating point differences due to rounding
        assert abs(actual_temp - expected_temp) <= 0.02, \
            f"Expected avg_cpu_temp {expected_temp} for hour {hour}, got {actual_temp}"

def test_api_invalid_hour():
    base_url = "http://127.0.0.1:8080/api/temperature"
    invalid_hour = "2099-01-01T12:00:00Z"

    try:
        response = requests.get(f"{base_url}?hour={invalid_hour}", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API for invalid hour: {e}")

    assert response.status_code == 404, f"Expected status code 404 for invalid hour, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response for invalid hour is not valid JSON. Response text: {response.text}")

    assert "error" in data, "Missing 'error' key in 404 JSON response"