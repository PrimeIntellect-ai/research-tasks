# test_final_state.py

import os
import json
import csv
from collections import defaultdict

def test_invalid_changes_csv():
    input_file = "/home/user/config_events.jsonl"
    output_file = "/home/user/invalid_changes.csv"

    assert os.path.exists(input_file), f"Input file {input_file} is missing."
    assert os.path.exists(output_file), f"Output file {output_file} is missing."

    # Read and parse input events
    events_by_service = defaultdict(list)
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            event = json.loads(line)
            events_by_service[event["service"]].append(event)

    # Compute expected violations
    expected_violations = []
    for service, events in events_by_service.items():
        events.sort(key=lambda x: x["timestamp"])
        for i in range(1, len(events)):
            if events[i]["timestamp"] - events[i-1]["timestamp"] < 1000:
                expected_violations.append(events[i])

    # Sort violations as required: primarily by service (ascending), secondarily by timestamp (ascending)
    expected_violations.sort(key=lambda x: (x["service"], x["timestamp"]))

    # Read actual CSV
    actual_rows = []
    with open(output_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            header = []
        assert header == ["service", "timestamp", "change_id"], f"CSV header is incorrect: {header}"

        for row in reader:
            if row:
                actual_rows.append(row)

    # Format expected rows
    expected_rows = [
        [v["service"], str(v["timestamp"]), v["change_id"]]
        for v in expected_violations
    ]

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} violation rows, but found {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch: expected {expected}, got {actual}."

def test_rust_project_exists():
    project_dir = "/home/user/config_tracker"
    assert os.path.isdir(project_dir), f"Rust project directory {project_dir} is missing."
    assert os.path.isfile(os.path.join(project_dir, "Cargo.toml")), "Cargo.toml is missing in the Rust project."