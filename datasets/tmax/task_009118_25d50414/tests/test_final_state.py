# test_final_state.py

import os
import csv
import json

def get_expected_data():
    input_file = '/home/user/sensor_data.csv'
    invalid_count = 0
    clean_data = []
    anomalies = []

    if not os.path.exists(input_file):
        return 0, [], []

    with open(input_file, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                voltage = float(row['voltage'])
                current = float(row['current'])
                sensor_id = row['sensor_id'].strip()
                timestamp = row['timestamp']

                if not timestamp or not sensor_id or voltage < 0.0 or current < 0.0:
                    invalid_count += 1
                    continue

                power = voltage * current
                record = {
                    "timestamp": timestamp,
                    "sensor_id": sensor_id,
                    "voltage": voltage,
                    "current": current,
                    "power": power
                }

                if power > 5000.0:
                    anomalies.append(record)
                else:
                    clean_data.append(record)

            except (ValueError, KeyError, TypeError):
                invalid_count += 1

    return invalid_count, clean_data, anomalies


def test_invalid_count_file():
    expected_invalid_count, _, _ = get_expected_data()
    file_path = '/home/user/invalid_count.txt'

    assert os.path.exists(file_path), f"File missing: {file_path}"

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content.isdigit(), f"Content of {file_path} is not a valid integer: '{content}'"
    assert int(content) == expected_invalid_count, f"Expected {expected_invalid_count} invalid rows, found {content}"


def test_clean_data_jsonl():
    _, expected_clean_data, _ = get_expected_data()
    file_path = '/home/user/clean_data.jsonl'

    assert os.path.exists(file_path), f"File missing: {file_path}"

    actual_clean_data = []
    with open(file_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                actual_clean_data.append(record)
            except json.JSONDecodeError:
                assert False, f"Invalid JSON on line {line_num} in {file_path}"

    assert len(actual_clean_data) == len(expected_clean_data), \
        f"Expected {len(expected_clean_data)} clean rows, found {len(actual_clean_data)}"

    for i, record in enumerate(actual_clean_data):
        assert "timestamp" in record, "Missing 'timestamp' in clean_data.jsonl"
        assert "sensor_id" in record, "Missing 'sensor_id' in clean_data.jsonl"
        assert "voltage" in record, "Missing 'voltage' in clean_data.jsonl"
        assert "current" in record, "Missing 'current' in clean_data.jsonl"
        assert "power" in record, "Missing 'power' in clean_data.jsonl"

        power = record["power"]
        assert power <= 5000.0, f"Found power > 5000.0 in clean_data.jsonl: {power}"

        expected_power = record["voltage"] * record["current"]
        assert abs(power - expected_power) < 1e-6, f"Incorrect power calculation in clean_data.jsonl: {power} != {expected_power}"


def test_anomalies_jsonl():
    _, _, expected_anomalies = get_expected_data()
    file_path = '/home/user/anomalies.jsonl'

    assert os.path.exists(file_path), f"File missing: {file_path}"

    actual_anomalies = []
    with open(file_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                actual_anomalies.append(record)
            except json.JSONDecodeError:
                assert False, f"Invalid JSON on line {line_num} in {file_path}"

    assert len(actual_anomalies) == len(expected_anomalies), \
        f"Expected {len(expected_anomalies)} anomalous rows, found {len(actual_anomalies)}"

    for i, record in enumerate(actual_anomalies):
        assert "timestamp" in record, "Missing 'timestamp' in anomalies.jsonl"
        assert "sensor_id" in record, "Missing 'sensor_id' in anomalies.jsonl"
        assert "voltage" in record, "Missing 'voltage' in anomalies.jsonl"
        assert "current" in record, "Missing 'current' in anomalies.jsonl"
        assert "power" in record, "Missing 'power' in anomalies.jsonl"

        power = record["power"]
        assert power > 5000.0, f"Found power <= 5000.0 in anomalies.jsonl: {power}"

        expected_power = record["voltage"] * record["current"]
        assert abs(power - expected_power) < 1e-6, f"Incorrect power calculation in anomalies.jsonl: {power} != {expected_power}"


def test_total_row_count():
    expected_invalid, expected_clean, expected_anomalies = get_expected_data()

    invalid_path = '/home/user/invalid_count.txt'
    clean_path = '/home/user/clean_data.jsonl'
    anomalies_path = '/home/user/anomalies.jsonl'

    invalid_count = 0
    if os.path.exists(invalid_path):
        with open(invalid_path, 'r') as f:
            content = f.read().strip()
            if content.isdigit():
                invalid_count = int(content)

    clean_count = 0
    if os.path.exists(clean_path):
        with open(clean_path, 'r') as f:
            clean_count = sum(1 for line in f if line.strip())

    anomalies_count = 0
    if os.path.exists(anomalies_path):
        with open(anomalies_path, 'r') as f:
            anomalies_count = sum(1 for line in f if line.strip())

    total_processed = invalid_count + clean_count + anomalies_count

    input_file = '/home/user/sensor_data.csv'
    total_input = 0
    if os.path.exists(input_file):
        with open(input_file, 'r') as f:
            total_input = sum(1 for _ in f) - 1 # exclude header

    assert total_processed == total_input, \
        f"Sum of processed rows ({total_processed}) does not match total input rows ({total_input})."