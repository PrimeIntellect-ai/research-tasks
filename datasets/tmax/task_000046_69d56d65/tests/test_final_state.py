# test_final_state.py

import os
import csv
import json
from datetime import datetime, timedelta
import pytest

PROCESSED_FILE = "/home/user/processed_full.csv"
SAMPLED_FILE = "/home/user/sampled_configs.csv"
INPUT_FILE = "/home/user/config_changes.jsonl"

def get_expected_resampled_data():
    if not os.path.exists(INPUT_FILE):
        return []

    with open(INPUT_FILE, "r") as f:
        data = [json.loads(line) for line in f]

    servers = {}
    for row in data:
        sid = row["server_id"]
        if sid not in servers:
            servers[sid] = []
        servers[sid].append(row)

    expected_rows = []
    for sid, rows in servers.items():
        rows.sort(key=lambda x: x["timestamp"])
        min_dt = datetime.fromisoformat(rows[0]["timestamp"])
        max_dt = datetime.fromisoformat(rows[-1]["timestamp"])

        current_dt = min_dt
        while current_dt <= max_dt:
            # Find the most recent record <= current_dt
            past_records = [r for r in rows if datetime.fromisoformat(r["timestamp"]) <= current_dt]
            if past_records:
                record = past_records[-1]
            else:
                record = rows[0]

            ip = record["ip_address"]
            ip_parts = ip.split(".")
            ip_parts[-1] = "XXX"
            masked_ip = ".".join(ip_parts)

            expected_rows.append({
                "timestamp": current_dt.isoformat(),
                "server_id": sid,
                "role": record["role"],
                "ip_address": masked_ip,
                "config_val": str(record["config_val"])
            })
            current_dt += timedelta(hours=1)

    return expected_rows

def test_processed_full_exists():
    assert os.path.exists(PROCESSED_FILE), f"The file {PROCESSED_FILE} does not exist."

def test_processed_full_content():
    assert os.path.exists(PROCESSED_FILE), f"The file {PROCESSED_FILE} does not exist."

    with open(PROCESSED_FILE, "r") as f:
        reader = csv.DictReader(f)
        actual_rows = list(reader)

    expected_rows = get_expected_resampled_data()

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in {PROCESSED_FILE}, found {len(actual_rows)}."

    # Check columns
    expected_columns = ["timestamp", "server_id", "role", "ip_address", "config_val"]
    assert reader.fieldnames == expected_columns, f"Expected columns {expected_columns}, found {reader.fieldnames}."

    # Check masking
    for row in actual_rows:
        assert row["ip_address"].endswith(".XXX"), f"IP address {row['ip_address']} is not properly masked."

    # Check data content
    for expected in expected_rows:
        # Find matching row
        match = next((r for r in actual_rows if r["server_id"] == expected["server_id"] and r["timestamp"] == expected["timestamp"]), None)
        assert match is not None, f"Missing expected row for server {expected['server_id']} at {expected['timestamp']}."
        assert match["role"] == expected["role"], f"Expected role {expected['role']} for {expected['server_id']} at {expected['timestamp']}, found {match['role']}."
        assert match["config_val"] == expected["config_val"], f"Expected config_val {expected['config_val']} for {expected['server_id']} at {expected['timestamp']}, found {match['config_val']}."

def test_sampled_configs_exists():
    assert os.path.exists(SAMPLED_FILE), f"The file {SAMPLED_FILE} does not exist."

def test_sampled_configs_content():
    assert os.path.exists(SAMPLED_FILE), f"The file {SAMPLED_FILE} does not exist."
    assert os.path.exists(PROCESSED_FILE), f"The file {PROCESSED_FILE} does not exist."

    with open(PROCESSED_FILE, "r") as f:
        full_rows = list(csv.DictReader(f))

    with open(SAMPLED_FILE, "r") as f:
        reader = csv.DictReader(f)
        sampled_rows = list(reader)

    expected_columns = ["timestamp", "server_id", "role", "ip_address", "config_val"]
    assert reader.fieldnames == expected_columns, f"Expected columns {expected_columns} in {SAMPLED_FILE}, found {reader.fieldnames}."

    # Check that sampled rows are roughly 25% of full rows
    expected_sample_size = round(len(full_rows) * 0.25)
    # Allow a small margin of error due to different rounding in stratified sampling implementations
    assert abs(len(sampled_rows) - expected_sample_size) <= 2, f"Expected around {expected_sample_size} rows in {SAMPLED_FILE}, found {len(sampled_rows)}."

    # Check that all sampled rows exist in the full dataset
    for row in sampled_rows:
        assert row in full_rows, f"Row {row} in {SAMPLED_FILE} is not in {PROCESSED_FILE}."