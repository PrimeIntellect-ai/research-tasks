# test_final_state.py

import os
import csv
import json
import math
import pytest

RAW_DATA_DIR = "/home/user/raw_data"
OUTPUT_DIR = "/home/user/output"
REJECTED_LOG = os.path.join(OUTPUT_DIR, "rejected.log")
CLEANED_DIR = os.path.join(OUTPUT_DIR, "cleaned")
SIMILAR_JSON = os.path.join(OUTPUT_DIR, "similar_sensors.json")

def get_sensor_data():
    """Reads all sensor data from raw_data and returns a dictionary of sensor_id -> data."""
    sensors = {}
    if not os.path.exists(RAW_DATA_DIR):
        return sensors

    for filename in os.listdir(RAW_DATA_DIR):
        if filename.endswith(".csv") and filename.startswith("sensor_"):
            filepath = os.path.join(RAW_DATA_DIR, filename)
            sensor_id = filename.replace(".csv", "")

            data = []
            with open(filepath, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
            sensors[sensor_id] = {'filename': filename, 'data': data}
    return sensors

def compute_missing_stats(data):
    total = len(data)
    missing = sum(1 for row in data if not row['temperature'].strip())
    return missing / total if total > 0 else 0

def impute_temperature(data):
    """Imputes missing temperature values using linear interpolation, then bfill/ffill."""
    temps = []
    for row in data:
        val = row['temperature'].strip()
        temps.append(float(val) if val else None)

    # Linear interpolation
    for i in range(len(temps)):
        if temps[i] is None:
            # Find previous valid
            prev_idx = i - 1
            while prev_idx >= 0 and temps[prev_idx] is None:
                prev_idx -= 1

            # Find next valid
            next_idx = i + 1
            while next_idx < len(temps) and temps[next_idx] is None:
                next_idx += 1

            if prev_idx >= 0 and next_idx < len(temps):
                # Interpolate
                prev_val = temps[prev_idx]
                next_val = temps[next_idx]
                temps[i] = prev_val + (next_val - prev_val) * (i - prev_idx) / (next_idx - prev_idx)

    # bfill
    for i in range(len(temps)):
        if temps[i] is None:
            next_idx = i + 1
            while next_idx < len(temps) and temps[next_idx] is None:
                next_idx += 1
            if next_idx < len(temps):
                temps[i] = temps[next_idx]

    # ffill
    for i in range(len(temps)):
        if temps[i] is None:
            prev_idx = i - 1
            if prev_idx >= 0:
                temps[i] = temps[prev_idx]

    return temps

def euclidean_distance(v1, v2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))

@pytest.fixture(scope="module")
def expected_state():
    sensors = get_sensor_data()
    rejected = []
    valid_sensors = {}

    for sensor_id, s_info in sensors.items():
        missing_rate = compute_missing_stats(s_info['data'])
        if missing_rate > 0.30:
            rejected.append(s_info['filename'])
        else:
            # Sort chronologically by timestamp
            sorted_data = sorted(s_info['data'], key=lambda x: float(x['timestamp']))
            imputed_temps = impute_temperature(sorted_data)
            valid_sensors[sensor_id] = imputed_temps

    rejected.sort()

    similar_pairs = []
    valid_ids = sorted(valid_sensors.keys())
    for i in range(len(valid_ids)):
        for j in range(i + 1, len(valid_ids)):
            id1 = valid_ids[i]
            id2 = valid_ids[j]
            dist = euclidean_distance(valid_sensors[id1], valid_sensors[id2])
            if dist < 15.0:
                pair = sorted([id1, id2])
                similar_pairs.append(pair)

    similar_pairs.sort(key=lambda x: x[0])

    return {
        'rejected': rejected,
        'valid_ids': valid_ids,
        'similar_pairs': similar_pairs
    }

def test_rejected_log(expected_state):
    """Validate that the rejected.log contains exactly the expected filenames."""
    assert os.path.exists(REJECTED_LOG), f"Rejected log file not found at {REJECTED_LOG}"

    with open(REJECTED_LOG, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert sorted(lines) == expected_state['rejected'], (
        f"Rejected log contents incorrect. Expected {expected_state['rejected']}, got {sorted(lines)}"
    )

def test_cleaned_parquets(expected_state):
    """Validate that parquet files exist for all valid sensors and only valid sensors."""
    assert os.path.exists(CLEANED_DIR), f"Cleaned directory not found at {CLEANED_DIR}"

    actual_files = [f for f in os.listdir(CLEANED_DIR) if f.endswith('.parquet')]
    actual_ids = sorted([f.replace('.parquet', '') for f in actual_files])

    expected_ids = expected_state['valid_ids']
    assert actual_ids == expected_ids, (
        f"Cleaned parquet files incorrect. Expected sensors {expected_ids}, got {actual_ids}"
    )

def test_similar_sensors_json(expected_state):
    """Validate that similar_sensors.json contains the correct pairs."""
    assert os.path.exists(SIMILAR_JSON), f"Similar sensors JSON not found at {SIMILAR_JSON}"

    with open(SIMILAR_JSON, 'r') as f:
        try:
            actual_pairs = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("similar_sensors.json is not a valid JSON file.")

    # Normalize actual pairs
    normalized_actual = sorted([sorted(pair) for pair in actual_pairs], key=lambda x: x[0])

    assert normalized_actual == expected_state['similar_pairs'], (
        f"Similar sensors JSON contents incorrect. Expected {expected_state['similar_pairs']}, got {normalized_actual}"
    )