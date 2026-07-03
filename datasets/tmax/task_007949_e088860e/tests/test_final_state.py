# test_final_state.py
import os
import csv
import math
import pytest

def compute_expected_data(raw_file):
    expected_rejected = []
    expected_cleaned = []

    window = []

    with open(raw_file, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            temp = float(row['temperature'])
            hum = float(row['humidity'])

            temp_invalid = not (-50.0 <= temp <= 50.0)
            hum_invalid = not (0.0 <= hum <= 100.0)

            if temp_invalid or hum_invalid:
                if temp_invalid and hum_invalid:
                    reason = "invalid_temp_and_humidity"
                elif temp_invalid:
                    reason = "invalid_temp"
                else:
                    reason = "invalid_humidity"

                expected_rejected.append({
                    'timestamp': row['timestamp'],
                    'sensor_id': row['sensor_id'],
                    'temperature': row['temperature'],
                    'humidity': row['humidity'],
                    'error_reason': reason
                })
            else:
                window.append(temp)
                if len(window) > 5:
                    window.pop(0)

                n = len(window)
                if n < 2:
                    mean = temp
                    stddev = 0.0
                    z = 0.0
                else:
                    mean = sum(window) / n
                    variance = sum((x - mean) ** 2 for x in window) / (n - 1)
                    stddev = math.sqrt(variance)
                    if stddev == 0.0:
                        z = 0.0
                    else:
                        z = (temp - mean) / stddev

                expected_cleaned.append({
                    'timestamp': row['timestamp'],
                    'sensor_id': row['sensor_id'],
                    'temperature': row['temperature'],
                    'humidity': row['humidity'],
                    'rolling_mean': f"{mean:.4f}",
                    'rolling_stddev': f"{stddev:.4f}",
                    'normalized_temp': f"{z:.4f}"
                })

    return expected_rejected, expected_cleaned

def test_source_and_executable_exist():
    assert os.path.exists("/home/user/process_data.cpp"), "C++ source file /home/user/process_data.cpp is missing."
    assert os.path.exists("/home/user/process_data"), "Executable /home/user/process_data is missing. Did it compile successfully?"
    assert os.access("/home/user/process_data", os.X_OK), "/home/user/process_data is not executable."

def test_rejected_data():
    raw_file = "/home/user/raw_sensor_data.csv"
    rej_file = "/home/user/rejected_data.csv"

    assert os.path.exists(raw_file), f"Raw data file {raw_file} is missing."
    assert os.path.exists(rej_file), f"Rejected data file {rej_file} is missing."

    expected_rejected, _ = compute_expected_data(raw_file)

    with open(rej_file, 'r', newline='') as f:
        reader = csv.DictReader(f)
        actual_rejected = list(reader)

    assert reader.fieldnames == ['timestamp', 'sensor_id', 'temperature', 'humidity', 'error_reason'], \
        f"Rejected data header is incorrect. Got: {reader.fieldnames}"

    assert len(actual_rejected) == len(expected_rejected), \
        f"Expected {len(expected_rejected)} rejected rows, but got {len(actual_rejected)}."

    for i, (actual, expected) in enumerate(zip(actual_rejected, expected_rejected)):
        assert actual['timestamp'] == expected['timestamp'], f"Row {i} timestamp mismatch."
        assert actual['error_reason'] == expected['error_reason'], f"Row {i} error_reason mismatch. Expected {expected['error_reason']}, got {actual['error_reason']}."

def test_cleaned_data():
    raw_file = "/home/user/raw_sensor_data.csv"
    clean_file = "/home/user/cleaned_data.csv"

    assert os.path.exists(clean_file), f"Cleaned data file {clean_file} is missing."

    _, expected_cleaned = compute_expected_data(raw_file)

    with open(clean_file, 'r', newline='') as f:
        reader = csv.DictReader(f)
        actual_cleaned = list(reader)

    expected_header = ['timestamp', 'sensor_id', 'temperature', 'humidity', 'rolling_mean', 'rolling_stddev', 'normalized_temp']
    assert reader.fieldnames == expected_header, \
        f"Cleaned data header is incorrect. Expected {expected_header}, got {reader.fieldnames}"

    assert len(actual_cleaned) == len(expected_cleaned), \
        f"Expected {len(expected_cleaned)} cleaned rows, but got {len(actual_cleaned)}."

    for i, (actual, expected) in enumerate(zip(actual_cleaned, expected_cleaned)):
        assert actual['timestamp'] == expected['timestamp'], f"Row {i} timestamp mismatch."

        # Check floating point values with a small tolerance due to potential string differences (e.g., 20.0 vs 20)
        assert abs(float(actual['rolling_mean']) - float(expected['rolling_mean'])) < 1e-3, \
            f"Row {i} rolling_mean mismatch. Expected {expected['rolling_mean']}, got {actual['rolling_mean']}."
        assert abs(float(actual['rolling_stddev']) - float(expected['rolling_stddev'])) < 1e-3, \
            f"Row {i} rolling_stddev mismatch. Expected {expected['rolling_stddev']}, got {actual['rolling_stddev']}."
        assert abs(float(actual['normalized_temp']) - float(expected['normalized_temp'])) < 1e-3, \
            f"Row {i} normalized_temp mismatch. Expected {expected['normalized_temp']}, got {actual['normalized_temp']}."

        # Verify exact 4 decimal places format by checking string length after decimal
        for col in ['rolling_mean', 'rolling_stddev', 'normalized_temp']:
            val_str = actual[col].strip()
            if '.' in val_str:
                decimals = len(val_str.split('.')[1])
                assert decimals == 4, f"Row {i} {col} does not have exactly 4 decimal places: '{val_str}'"
            else:
                pytest.fail(f"Row {i} {col} is missing decimal point: '{val_str}'")