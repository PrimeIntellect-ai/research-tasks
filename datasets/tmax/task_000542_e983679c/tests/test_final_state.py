# test_final_state.py
import csv
import math
import binascii
import requests
import pytest
from datetime import datetime, timezone

URL = "http://127.0.0.1:9042/api/v1/telemetry"
AUTH_HEADER = {"Authorization": "Bearer sec-iot-pipeline-8821"}

def get_historical_data():
    data = []
    with open('/home/user/data/historical_context.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ts = int(row['timestamp'])
            val = float(row['value']) if row['value'] else None
            data.append([ts, val])

    # Linear interpolation
    for i in range(len(data)):
        if data[i][1] is None:
            prev_idx = i - 1
            while prev_idx >= 0 and data[prev_idx][1] is None:
                prev_idx -= 1
            next_idx = i + 1
            while next_idx < len(data) and data[next_idx][1] is None:
                next_idx += 1

            if prev_idx >= 0 and next_idx < len(data):
                x0 = data[prev_idx][0]
                y0 = data[prev_idx][1]
                x1 = data[next_idx][0]
                y1 = data[next_idx][1]
                x = data[i][0]
                y = y0 + (x - x0) * (y1 - y0) / (x1 - x0)
                data[i][1] = y
            elif prev_idx >= 0:
                data[i][1] = data[prev_idx][1]
            elif next_idx < len(data):
                data[i][1] = data[next_idx][1]

    return data

def compute_expected_response(new_points):
    data = get_historical_data()
    data.extend(new_points)
    data.sort(key=lambda x: x[0])

    buckets = {}
    for ts, val in data:
        bucket_ts = (ts // 15) * 15
        if bucket_ts not in buckets:
            buckets[bucket_ts] = []
        buckets[bucket_ts].append(val)

    bucket_means = {}
    sorted_buckets = sorted(buckets.keys())
    for b in sorted_buckets:
        bucket_means[b] = sum(buckets[b]) / len(buckets[b])

    new_bucket_timestamps = set((ts // 15) * 15 for ts, _ in new_points)

    results = []
    for i, b in enumerate(sorted_buckets):
        if b in new_bucket_timestamps:
            # compute rolling average of last 4 buckets (including this one)
            start_idx = max(0, i - 3)
            window = [bucket_means[sorted_buckets[j]] for j in range(start_idx, i + 1)]
            rolling_avg = sum(window) / len(window)
            mean_val = bucket_means[b]

            diff = abs(mean_val - rolling_avg) / rolling_avg if rolling_avg != 0 else 0
            is_anomaly = diff > 0.15

            iso_time = datetime.fromtimestamp(b, tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            results.append({
                "bucket_start_time": iso_time,
                "mean_value": mean_val,
                "rolling_avg": rolling_avg,
                "is_anomaly": is_anomaly
            })

    return results

def test_unauthorized():
    resp = requests.post(URL, json={"stream_id": "test", "payloads": []})
    assert resp.status_code == 401, f"Expected 401 Unauthorized, got {resp.status_code}"

def test_telemetry_processing():
    # Last timestamp in historical data is around 1715505300
    # Let's add some new points
    base_ts = 1715505310
    new_points = [
        [base_ts, 42.0],
        [base_ts + 1, 42.5],
        [base_ts + 16, 80.0] # Anomaly
    ]

    payloads = []
    for ts, val in new_points:
        csv_line = f"{ts},s1,{val}"
        hex_str = binascii.hexlify(csv_line.encode('ascii')).decode('ascii')
        payloads.append(hex_str)

    req_body = {
        "stream_id": "alpha-grid",
        "payloads": payloads
    }

    resp = requests.post(URL, headers=AUTH_HEADER, json=req_body)
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}. Body: {resp.text}"

    resp_data = resp.json()
    expected_data = compute_expected_response(new_points)

    assert len(resp_data) == len(expected_data), f"Expected {len(expected_data)} buckets, got {len(resp_data)}"

    for i in range(len(expected_data)):
        exp = expected_data[i]
        act = resp_data[i]

        assert act["bucket_start_time"] == exp["bucket_start_time"], f"Bucket time mismatch at index {i}"
        assert math.isclose(act["mean_value"], exp["mean_value"], rel_tol=1e-3), f"Mean value mismatch at index {i}: expected {exp['mean_value']}, got {act['mean_value']}"
        assert math.isclose(act["rolling_avg"], exp["rolling_avg"], rel_tol=1e-3), f"Rolling avg mismatch at index {i}: expected {exp['rolling_avg']}, got {act['rolling_avg']}"
        assert act["is_anomaly"] == exp["is_anomaly"], f"Anomaly mismatch at index {i}: expected {exp['is_anomaly']}, got {act['is_anomaly']}"