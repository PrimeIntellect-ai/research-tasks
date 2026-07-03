# test_final_state.py

import os
import csv
import math
import pytest
from collections import defaultdict

OUTPUT_FILE = '/home/user/output/final_stats.csv'
RAW_DATA_DIR = '/home/user/raw_data'

def get_expected_data():
    raw_rows = []
    for filename in os.listdir(RAW_DATA_DIR):
        if filename.endswith('.csv'):
            filepath = os.path.join(RAW_DATA_DIR, filename)
            with open(filepath, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    config_diff = row['config_diff']
                    diff_line_count = len(config_diff.split('\n')) if config_diff else 0
                    raw_rows.append({
                        'event_id': row['event_id'],
                        'timestamp': row['timestamp'],
                        'server_id': row['server_id'],
                        'service_name': row['service_name'],
                        'diff_line_count': diff_line_count
                    })

    # Sort by timestamp, then event_id
    raw_rows.sort(key=lambda x: (x['timestamp'], x['event_id']))

    # Compute rolling average per service
    service_history = defaultdict(list)
    expected_rows = []

    for row in raw_rows:
        svc = row['service_name']
        history = service_history[svc]
        history.append(row['diff_line_count'])
        if len(history) > 3:
            history.pop(0)

        rolling_avg = sum(history) / len(history)
        row['rolling_avg_diff'] = f"{rolling_avg:.2f}"
        expected_rows.append(row)

    return expected_rows

@pytest.fixture(scope="module")
def expected_data():
    return get_expected_data()

@pytest.fixture(scope="module")
def actual_data():
    assert os.path.isfile(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"

    with open(OUTPUT_FILE, 'r', newline='') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        expected_headers = ['event_id', 'timestamp', 'server_id', 'service_name', 'diff_line_count', 'rolling_avg_diff']
        assert headers == expected_headers, f"Expected headers {expected_headers}, got {headers}"

        rows = list(reader)
    return rows

def test_output_file_exists():
    assert os.path.isfile(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"

def test_no_missing_values_and_non_negative(actual_data):
    for i, row in enumerate(actual_data):
        for key, val in row.items():
            assert val is not None and val.strip() != '', f"Missing value in row {i+1} for column {key}"

        rolling_avg = float(row['rolling_avg_diff'])
        assert rolling_avg >= 0, f"rolling_avg_diff must be >= 0, got {rolling_avg} in row {i+1}"

def test_sorting(actual_data, expected_data):
    actual_events = [row['event_id'] for row in actual_data]
    expected_events = [row['event_id'] for row in expected_data]
    assert actual_events == expected_events, f"Output is not sorted correctly. Expected order: {expected_events}, Actual: {actual_events}"

def test_diff_line_count_and_rolling_avg(actual_data, expected_data):
    actual_dict = {row['event_id']: row for row in actual_data}

    for expected_row in expected_data:
        event_id = expected_row['event_id']
        assert event_id in actual_dict, f"Missing event_id {event_id} in output"
        actual_row = actual_dict[event_id]

        assert int(actual_row['diff_line_count']) == expected_row['diff_line_count'], \
            f"Incorrect diff_line_count for event {event_id}. Expected {expected_row['diff_line_count']}, got {actual_row['diff_line_count']}"

        expected_avg = float(expected_row['rolling_avg_diff'])
        actual_avg = float(actual_row['rolling_avg_diff'])

        assert math.isclose(actual_avg, expected_avg, abs_tol=0.01), \
            f"Incorrect rolling_avg_diff for event {event_id}. Expected {expected_avg}, got {actual_avg}"