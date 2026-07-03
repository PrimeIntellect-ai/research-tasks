# test_final_state.py

import os
import json
import csv
import re
import pytest
from collections import defaultdict

def test_hourly_summary_json():
    output_file = "/home/user/output/hourly_summary.json"
    assert os.path.exists(output_file), f"Output file {output_file} does not exist."

    with open(output_file, "r") as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Output file {output_file} is not valid JSON: {e}")

    # Compute expected data dynamically from inputs
    meta_file = "/home/user/data/server_meta.csv"
    assert os.path.exists(meta_file), f"Metadata file {meta_file} missing."

    server_env = {}
    with open(meta_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            server_env[row["ServerID"]] = row["Environment"]

    log_file = "/home/user/data/config_logs.txt"
    assert os.path.exists(log_file), f"Log file {log_file} missing."

    # Regex to extract Timestamp, ServerID, ConfigKey, NewValue
    log_pattern = re.compile(r"^\[(.*?)\] .*?: Server \{(.*?)\} updated config \[(.*?)\] -> (.*)$")

    unique_records = set()
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = log_pattern.match(line)
            if match:
                timestamp, server_id, config_key, new_value = match.groups()
                unique_records.add((timestamp, server_id, config_key, new_value))

    counts = defaultdict(int)
    for timestamp, server_id, config_key, new_value in unique_records:
        if server_id not in server_env:
            continue
        env = server_env[server_id]
        # Truncate to hour (e.g., 2023-10-24T08:15:32Z -> 2023-10-24T08:00:00Z)
        hour = timestamp[:13] + ":00:00Z"
        counts[(hour, env)] += 1

    expected_data = []
    for (hour, env), count in counts.items():
        expected_data.append({
            "change_count": count,
            "environment": env,
            "hour": hour
        })

    # Sort chronologically by hour, then alphabetically by environment
    expected_data.sort(key=lambda x: (x["hour"], x["environment"]))

    assert actual_data == expected_data, (
        f"Data mismatch in {output_file}.\n"
        f"Expected:\n{json.dumps(expected_data, indent=4)}\n"
        f"Got:\n{json.dumps(actual_data, indent=4)}"
    )

def test_source_code_exists():
    src_file = "/home/user/src/aggregator.cpp"
    assert os.path.exists(src_file), f"Source file {src_file} does not exist."

def test_binary_exists():
    bin_file = "/home/user/bin/aggregator"
    assert os.path.exists(bin_file), f"Binary file {bin_file} does not exist."
    assert os.access(bin_file, os.X_OK), f"File {bin_file} is not executable."