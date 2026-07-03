# test_final_state.py
import os
import csv
import json
import math
from collections import defaultdict
import pytest

RAW_DIR = "/home/user/raw_sensors"
PROCESSED_DIR = "/home/user/processed"
SCRIPTS_DIR = "/home/user/scripts"
SUMMARY_FILE = "/home/user/summary.json"

def compute_expected_summary():
    """Dynamically compute the expected summary based on the raw data."""
    if not os.path.exists(RAW_DIR):
        return {}

    all_values = defaultdict(list)

    for filename in os.listdir(RAW_DIR):
        if not filename.endswith('.csv'):
            continue
        filepath = os.path.join(RAW_DIR, filename)

        long_data = []
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ts = row['timestamp']
                for col, val in row.items():
                    if col == 'timestamp': 
                        continue
                    sensor, metric = col.split('_', 1)
                    long_data.append({'timestamp': ts, 'sensor': sensor, 'metric': metric, 'value': float(val)})

        # Group by metric
        metric_groups = defaultdict(list)
        for item in long_data:
            metric_groups[item['metric']].append(item)

        # Stratified sampling
        for metric, items in metric_groups.items():
            # Sort strictly by timestamp
            items.sort(key=lambda x: x['timestamp'])
            keep_n = math.ceil(len(items) / 2)
            kept = items[:keep_n]
            for k in kept:
                all_values[metric].append(k['value'])

    summary = {}
    for metric, vals in all_values.items():
        summary[metric] = round(sum(vals) / len(vals), 2)

    return summary

def test_scripts_exist():
    """Verify that the required scripts have been created."""
    assert os.path.isdir(SCRIPTS_DIR), f"Directory {SCRIPTS_DIR} is missing."

    process_script = os.path.join(SCRIPTS_DIR, "process_sensor.py")
    run_script = os.path.join(SCRIPTS_DIR, "run_pipeline.sh")

    assert os.path.isfile(process_script), f"File {process_script} is missing."
    assert os.path.isfile(run_script), f"File {run_script} is missing."

    # Check for aggregate script (can be any extension)
    aggregate_scripts = [f for f in os.listdir(SCRIPTS_DIR) if f.startswith("aggregate.")]
    assert len(aggregate_scripts) > 0, "No aggregate script found in /home/user/scripts/"

def test_processed_files_exist_and_format():
    """Verify that processed files exist and have the correct format."""
    assert os.path.isdir(PROCESSED_DIR), f"Directory {PROCESSED_DIR} is missing."

    raw_files = [f for f in os.listdir(RAW_DIR) if f.endswith('.csv')]
    processed_files = [f for f in os.listdir(PROCESSED_DIR) if f.endswith('.csv')]

    assert set(raw_files) == set(processed_files), "Processed files do not match raw files."

    expected_header = ["timestamp", "sensor", "metric", "value"]

    for filename in processed_files:
        filepath = os.path.join(PROCESSED_DIR, filename)
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            try:
                header = next(reader)
            except StopIteration:
                pytest.fail(f"Processed file {filename} is empty.")

            assert header == expected_header, f"Header in {filename} is incorrect. Expected {expected_header}, got {header}"

def test_summary_json_content():
    """Verify that the summary.json contains the correctly computed averages."""
    assert os.path.isfile(SUMMARY_FILE), f"File {SUMMARY_FILE} is missing."

    with open(SUMMARY_FILE, 'r') as f:
        try:
            actual_summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {SUMMARY_FILE} does not contain valid JSON.")

    expected_summary = compute_expected_summary()

    assert isinstance(actual_summary, dict), "The summary.json should contain a JSON object."

    for metric, expected_val in expected_summary.items():
        assert metric in actual_summary, f"Metric '{metric}' is missing from summary.json."
        actual_val = actual_summary[metric]
        assert isinstance(actual_val, (int, float)), f"Value for '{metric}' must be a number."
        assert math.isclose(actual_val, expected_val, rel_tol=1e-5), \
            f"Value for '{metric}' is incorrect. Expected {expected_val}, got {actual_val}"

    # Check for unexpected extra keys
    for metric in actual_summary.keys():
        assert metric in expected_summary, f"Unexpected metric '{metric}' found in summary.json."