# test_final_state.py

import os
import re
import csv
from datetime import datetime, timedelta
import pytest

LOG_DIR = "/home/user/config_logs"
OUTPUT_CSV = "/home/user/anomalies.csv"

def compute_expected_anomalies(log_dir):
    anomalies = []
    pattern = re.compile(r"\[(.*?)\]\s+.*current_load=([0-9.]+)")

    if not os.path.exists(log_dir):
        return anomalies

    for filename in os.listdir(log_dir):
        if not filename.endswith(".log"):
            continue
        server = filename[:-4]
        filepath = os.path.join(log_dir, filename)

        data = {}
        with open(filepath, 'r') as f:
            for line in f:
                match = pattern.search(line)
                if match:
                    dt = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
                    dt = dt.replace(second=0, microsecond=0)
                    load = float(match.group(2))
                    data[dt] = load

        if not data:
            continue

        sorted_dts = sorted(data.keys())
        min_dt = sorted_dts[0]
        max_dt = sorted_dts[-1]

        current_dt = min_dt
        last_load = data[min_dt]
        prev_load = None

        while current_dt <= max_dt:
            if current_dt in data:
                current_load = data[current_dt]
                last_load = current_load
            else:
                current_load = last_load

            if prev_load is not None:
                increase = current_load - prev_load
                if increase > 45.0:
                    anomalies.append({
                        'Timestamp': current_dt.strftime("%Y-%m-%d %H:%M:%S"),
                        'Server': server,
                        'Increase': round(increase, 1)
                    })
            prev_load = current_load
            current_dt += timedelta(minutes=1)

    anomalies.sort(key=lambda x: (x['Timestamp'], x['Server']))
    return anomalies

def test_output_csv_exists():
    assert os.path.exists(OUTPUT_CSV), f"Output file {OUTPUT_CSV} was not created."
    assert os.path.isfile(OUTPUT_CSV), f"{OUTPUT_CSV} is not a file."

def test_output_csv_content():
    assert os.path.exists(OUTPUT_CSV), f"Output file {OUTPUT_CSV} does not exist."

    expected_anomalies = compute_expected_anomalies(LOG_DIR)

    actual_anomalies = []
    with open(OUTPUT_CSV, 'r') as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ['Timestamp', 'Server', 'Increase'], \
            f"CSV header is incorrect. Expected ['Timestamp', 'Server', 'Increase'], got {reader.fieldnames}"

        for row in reader:
            try:
                row['Increase'] = float(row['Increase'])
                actual_anomalies.append(row)
            except ValueError:
                pytest.fail(f"Invalid Increase value in CSV: {row['Increase']}")

    # Format expected for comparison
    for exp in expected_anomalies:
        exp['Increase'] = float(exp['Increase'])

    assert len(actual_anomalies) == len(expected_anomalies), \
        f"Expected {len(expected_anomalies)} anomalies, but found {len(actual_anomalies)}."

    for i, (actual, expected) in enumerate(zip(actual_anomalies, expected_anomalies)):
        assert actual['Timestamp'] == expected['Timestamp'], \
            f"Row {i+1}: Expected Timestamp {expected['Timestamp']}, got {actual['Timestamp']}"
        assert actual['Server'] == expected['Server'], \
            f"Row {i+1}: Expected Server {expected['Server']}, got {actual['Server']}"
        assert actual['Increase'] == expected['Increase'], \
            f"Row {i+1}: Expected Increase {expected['Increase']}, got {actual['Increase']}"