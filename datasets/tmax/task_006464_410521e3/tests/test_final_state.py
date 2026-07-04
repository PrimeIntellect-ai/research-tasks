# test_final_state.py

import os
import csv
import math
import pytest

def get_expected_data():
    raw_file = "/home/user/raw_sensor_data.csv"
    assert os.path.exists(raw_file), f"Input file {raw_file} is missing."

    s1_data = {}
    s2_data = {}

    with open(raw_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            t = int(row[0])
            sensor = row[1]
            val = float(row[2])

            if sensor == 'S1':
                s1_data[t] = max(s1_data.get(t, val), val)
            elif sensor == 'S2':
                s2_data[t] = max(s2_data.get(t, val), val)

    all_timestamps = list(s1_data.keys()) + list(s2_data.keys())
    t_min = min(all_timestamps)
    t_max = max(all_timestamps)

    def interpolate(sensor_data):
        resampled = {}
        sorted_t = sorted(sensor_data.keys())

        if not sorted_t:
            return resampled

        first_t = sorted_t[0]
        last_t = sorted_t[-1]

        for t in range(t_min, t_max + 1):
            if t in sensor_data:
                resampled[t] = sensor_data[t]
            elif t < first_t:
                resampled[t] = sensor_data[first_t]
            elif t > last_t:
                resampled[t] = sensor_data[last_t]
            else:
                # Find nearest preceding and succeeding
                t_prev = max(k for k in sorted_t if k < t)
                t_next = min(k for k in sorted_t if k > t)

                v_prev = sensor_data[t_prev]
                v_next = sensor_data[t_next]

                # Linear interpolation
                slope = (v_next - v_prev) / (t_next - t_prev)
                resampled[t] = v_prev + slope * (t - t_prev)

        return resampled

    s1_resampled = interpolate(s1_data)
    s2_resampled = interpolate(s2_data)

    dist_sq = 0.0
    for t in range(t_min, t_max + 1):
        diff = s1_resampled[t] - s2_resampled[t]
        dist_sq += diff * diff

    distance = math.sqrt(dist_sq)

    return t_min, t_max, s1_resampled, s2_resampled, distance

def test_resampled_csv():
    resampled_file = "/home/user/resampled.csv"
    assert os.path.exists(resampled_file), f"Output file {resampled_file} is missing."

    t_min, t_max, s1_resampled, s2_resampled, _ = get_expected_data()

    with open(resampled_file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['timestamp', 'S1_value', 'S2_value'], f"Incorrect header in {resampled_file}."

        rows = list(reader)
        assert len(rows) == (t_max - t_min + 1), f"Expected {t_max - t_min + 1} rows, got {len(rows)}."

        for row in rows:
            assert len(row) == 3, f"Row {row} does not have 3 columns."
            t = int(row[0])
            v1_str, v2_str = row[1], row[2]

            # Check 4 decimal places formatting
            assert len(v1_str.split('.')[-1]) == 4, f"S1_value {v1_str} not formatted to 4 decimal places."
            assert len(v2_str.split('.')[-1]) == 4, f"S2_value {v2_str} not formatted to 4 decimal places."

            v1, v2 = float(v1_str), float(v2_str)

            assert t in s1_resampled, f"Unexpected timestamp {t}."
            assert abs(v1 - s1_resampled[t]) < 1e-3, f"S1 value at {t} is incorrect. Expected {s1_resampled[t]}, got {v1}."
            assert abs(v2 - s2_resampled[t]) < 1e-3, f"S2 value at {t} is incorrect. Expected {s2_resampled[t]}, got {v2}."

def test_distance_txt():
    distance_file = "/home/user/distance.txt"
    assert os.path.exists(distance_file), f"Output file {distance_file} is missing."

    _, _, _, _, expected_distance = get_expected_data()

    with open(distance_file, 'r') as f:
        content = f.read().strip()

    assert len(content.split('.')[-1]) == 4, f"Distance {content} not formatted to 4 decimal places."

    distance = float(content)
    assert abs(distance - expected_distance) < 1e-3, f"Distance is incorrect. Expected {expected_distance}, got {distance}."