# test_final_state.py

import os
import json
import re
import math
from datetime import datetime
import pytest

def compute_expected_distances(log_path):
    with open(log_path, 'r') as f:
        lines = f.readlines()

    # Regex patterns
    line_pattern = re.compile(
        r'^\[(.*?)\].*?sensor_id:\s*(SN-\d{4})\b.*?payload:\s*(\{.*\})'
    )

    sensor_data = {}

    for line in lines:
        # Try to match valid sensor_id format directly in regex or check later
        # We'll extract timestamp, sensor_id, payload
        match = re.search(r'^\[(.*?)\]', line)
        if not match: continue
        timestamp_str = match.group(1)

        sensor_match = re.search(r'sensor_id:\s*([A-Za-z0-9\-]+)', line)
        if not sensor_match: continue
        sensor_id = sensor_match.group(1)

        # Filter strictly SN- followed by exactly 4 digits
        if not re.match(r'^SN-\d{4}$', sensor_id):
            continue

        payload_match = re.search(r'payload:\s*(\{.*?\})', line)
        if not payload_match: continue
        payload_str = payload_match.group(1)

        try:
            payload = json.loads(payload_str)
        except json.JSONDecodeError:
            continue

        dt = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
        ts = dt.timestamp()

        x = payload.get('x')
        y = payload.get('y')

        if sensor_id not in sensor_data:
            sensor_data[sensor_id] = []

        sensor_data[sensor_id].append({
            'ts': ts,
            'x': x,
            'y': y
        })

    distances = {}
    for sensor_id, records in sensor_data.items():
        records.sort(key=lambda r: r['ts'])

        # Time-based linear interpolation for x and y
        for axis in ['x', 'y']:
            for i, rec in enumerate(records):
                if rec[axis] is None:
                    # Find previous valid
                    prev_valid = None
                    for j in range(i-1, -1, -1):
                        if records[j][axis] is not None:
                            prev_valid = records[j]
                            break
                    # Find next valid
                    next_valid = None
                    for j in range(i+1, len(records)):
                        if records[j][axis] is not None:
                            next_valid = records[j]
                            break

                    if prev_valid and next_valid:
                        t0, v0 = prev_valid['ts'], prev_valid[axis]
                        t1, v1 = next_valid['ts'], next_valid[axis]
                        t = rec['ts']
                        if t1 != t0:
                            rec[axis] = v0 + (v1 - v0) * (t - t0) / (t1 - t0)
                        else:
                            rec[axis] = v0

        # Compute distance
        total_dist = 0.0
        for i in range(1, len(records)):
            dx = records[i]['x'] - records[i-1]['x']
            dy = records[i]['y'] - records[i-1]['y']
            total_dist += math.hypot(dx, dy)

        distances[sensor_id] = round(total_dist, 2)

    return distances

def test_distances_json_exists():
    assert os.path.exists("/home/user/distances.json"), "The file /home/user/distances.json does not exist."
    assert os.path.isfile("/home/user/distances.json"), "/home/user/distances.json is not a file."

def test_distances_json_content():
    log_path = "/home/user/sensor_stream.log"
    assert os.path.exists(log_path), f"Log file {log_path} is missing, cannot compute expected results."

    expected_distances = compute_expected_distances(log_path)

    with open("/home/user/distances.json", "r") as f:
        try:
            student_distances = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/home/user/distances.json is not valid JSON.")

    assert isinstance(student_distances, dict), "The top-level JSON structure should be an object (dictionary)."

    for sensor_id, expected_dist in expected_distances.items():
        assert sensor_id in student_distances, f"Missing sensor_id '{sensor_id}' in output JSON."
        student_dist = student_distances[sensor_id]
        assert isinstance(student_dist, (int, float)), f"Distance for '{sensor_id}' must be a number."
        assert math.isclose(student_dist, expected_dist, abs_tol=0.01), \
            f"Expected distance for '{sensor_id}' to be {expected_dist}, but got {student_dist}."

    for sensor_id in student_distances:
        assert sensor_id in expected_distances, f"Unexpected sensor_id '{sensor_id}' found in output JSON."