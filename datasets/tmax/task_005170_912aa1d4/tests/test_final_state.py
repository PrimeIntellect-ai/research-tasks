# test_final_state.py

import os
import re
import math
from datetime import datetime, timedelta
from collections import defaultdict
import requests
import pytest

def test_vendored_parse_fixed():
    path = "/app/vendored/parse/parse.py"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    correct_line = "match = self._search_re.search(string)"
    broken_line = "match = self._search_re.match(string)"

    assert correct_line in content, f"The fix '{correct_line}' was not found in {path}."
    assert broken_line not in content, f"The perturbation '{broken_line}' is still present in {path}."

def compute_expected_data(sensor_id):
    log_path = "/home/user/data/raw_sensors.log"
    assert os.path.exists(log_path), f"Log file {log_path} is missing."

    # Regex to parse the log line
    # Example: [2023-10-01T10:03:15] SYSTEM_LOG: Sensor TX-99 recorded a value of 45.2 at the edge node.
    pattern = re.compile(r"\[(.*?)\] SYSTEM_LOG: Sensor (.*?) recorded a value of (.*?) at the edge node.")

    raw_data = defaultdict(list)

    with open(log_path, "r") as f:
        for line in f:
            match = pattern.search(line)
            if match:
                ts_str, s_id, val_str = match.groups()
                if s_id == sensor_id:
                    dt = datetime.fromisoformat(ts_str)
                    val = float(val_str)
                    # Round down to nearest minute
                    dt_min = dt.replace(second=0, microsecond=0)
                    raw_data[dt_min].append(val)

    if not raw_data:
        return []

    # Average multiple readings in the same minute
    minute_data = {dt: sum(vals)/len(vals) for dt, vals in raw_data.items()}

    sorted_minutes = sorted(minute_data.keys())
    min_time = sorted_minutes[0]
    max_time = sorted_minutes[-1]

    # Create full time series
    full_series = {}
    current = min_time
    while current <= max_time:
        full_series[current] = minute_data.get(current, None)
        current += timedelta(minutes=1)

    # Linear interpolation
    # Find gaps and fill
    times = sorted(full_series.keys())
    for i, t in enumerate(times):
        if full_series[t] is None:
            # Find previous known
            prev_idx = i - 1
            while prev_idx >= 0 and full_series[times[prev_idx]] is None:
                prev_idx -= 1

            # Find next known
            next_idx = i + 1
            while next_idx < len(times) and full_series[times[next_idx]] is None:
                next_idx += 1

            if prev_idx >= 0 and next_idx < len(times):
                prev_t = times[prev_idx]
                next_t = times[next_idx]
                prev_v = full_series[prev_t]
                next_v = full_series[next_t]

                # Interpolate
                total_diff = (next_t - prev_t).total_seconds()
                curr_diff = (t - prev_t).total_seconds()

                interpolated_val = prev_v + (next_v - prev_v) * (curr_diff / total_diff)
                full_series[t] = interpolated_val

    # Stratified sampling: 0, 12, 24, 36, 48
    sampled_data = []
    target_minutes = {0, 12, 24, 36, 48}
    for t in times:
        if t.minute in target_minutes and full_series[t] is not None:
            sampled_data.append({
                "timestamp": t.isoformat(),
                "value": round(full_series[t], 2)
            })

    return sampled_data

def test_api_unauthorized():
    url = "http://127.0.0.1:8080/api/v1/samples?sensor=TX-99"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API on 127.0.0.1:8080: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for missing auth, got {response.status_code}"

def test_api_authorized_tx99():
    url = "http://127.0.0.1:8080/api/v1/samples?sensor=TX-99"
    headers = {"Authorization": "Bearer secret_sensor_token_99X"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API on 127.0.0.1:8080: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    expected_data = compute_expected_data("TX-99")

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} samples, got {len(data)}"

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert actual["timestamp"] == expected["timestamp"], f"Mismatch in timestamp at index {i}. Expected {expected['timestamp']}, got {actual['timestamp']}"
        assert math.isclose(actual["value"], expected["value"], rel_tol=1e-5, abs_tol=0.01), f"Mismatch in value at index {i}. Expected {expected['value']}, got {actual['value']}"

def test_api_authorized_rx42():
    url = "http://127.0.0.1:8080/api/v1/samples?sensor=RX-42"
    headers = {"Authorization": "Bearer secret_sensor_token_99X"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API on 127.0.0.1:8080: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    expected_data = compute_expected_data("RX-42")

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} samples, got {len(data)}"

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert actual["timestamp"] == expected["timestamp"], f"Mismatch in timestamp at index {i}. Expected {expected['timestamp']}, got {actual['timestamp']}"
        assert math.isclose(actual["value"], expected["value"], rel_tol=1e-5, abs_tol=0.01), f"Mismatch in value at index {i}. Expected {expected['value']}, got {actual['value']}"