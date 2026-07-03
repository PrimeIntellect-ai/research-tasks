# test_final_state.py

import os
import csv
import json
from datetime import datetime, timedelta
import pytest

INPUT_FILE = '/home/user/raw_config_events.jsonl'
OUTPUT_FILE = '/home/user/hourly_config_drift.csv'

def compute_expected_results():
    server_events = {}
    seen_events = set()

    with open(INPUT_FILE, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)
            event_id = data['event_id']
            if event_id in seen_events:
                continue
            seen_events.add(event_id)

            srv = data['server_id']
            if srv not in server_events:
                server_events[srv] = []

            dt = datetime.strptime(data['timestamp'], "%Y-%m-%dT%H:%M:%SZ")
            server_events[srv].append((dt, data['config_hash']))

    for srv in server_events:
        server_events[srv].sort(key=lambda x: x[0])

    start_hour = datetime(2023, 10, 1, 0, 0, 0)
    end_hour = datetime(2023, 10, 7, 23, 0, 0)

    expected_results = []

    current_hour = start_hour
    while current_hour <= end_hour:
        active_hashes = set()
        for srv, evts in server_events.items():
            last_hash = None
            for dt, h in evts:
                if dt <= current_hour:
                    last_hash = h
                else:
                    break
            if last_hash is not None:
                active_hashes.add(last_hash)

        expected_results.append((current_hour.strftime("%Y-%m-%dT%H:%M:%SZ"), len(active_hashes)))
        current_hour += timedelta(hours=1)

    return expected_results

def test_output_file_exists():
    assert os.path.exists(OUTPUT_FILE), f"Output file {OUTPUT_FILE} does not exist."
    assert os.path.isfile(OUTPUT_FILE), f"Path {OUTPUT_FILE} is not a file."

def test_output_csv_content():
    assert os.path.exists(OUTPUT_FILE), f"Output file {OUTPUT_FILE} does not exist."

    expected_results = compute_expected_results()

    agent_results = []
    with open(OUTPUT_FILE, 'r') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail(f"Output file {OUTPUT_FILE} is empty.")

        assert header == ['hour', 'unique_configs'], f"Header mismatch. Expected ['hour', 'unique_configs'], got {header}"

        for row in reader:
            if not row:
                continue
            assert len(row) == 2, f"Row {row} does not have exactly 2 columns."
            agent_results.append((row[0], int(row[1])))

    assert len(agent_results) == len(expected_results), (
        f"Row count mismatch. Expected {len(expected_results)} rows, got {len(agent_results)}."
    )

    for exp, agt in zip(expected_results, agent_results):
        assert agt == exp, f"Mismatch at hour {exp[0]}: expected {exp[1]} unique configs, got {agt[1]}."