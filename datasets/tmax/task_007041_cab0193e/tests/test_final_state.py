# test_final_state.py
import os
import csv
import hashlib
import pytest

OUTPUT_DIR = "/home/user/output"
VALIDATION_TXT = os.path.join(OUTPUT_DIR, "validation.txt")
DAILY_CONFIGS_CSV = os.path.join(OUTPUT_DIR, "daily_configs.csv")

def test_validation_txt_exists_and_content():
    assert os.path.exists(VALIDATION_TXT), f"File {VALIDATION_TXT} is missing."
    with open(VALIDATION_TXT, 'r') as f:
        content = f.read().strip()
    expected_content = "Dropped count: 2"
    assert content == expected_content, f"Expected validation content '{expected_content}', but got '{content}'."

def test_daily_configs_csv_exists_and_content():
    assert os.path.exists(DAILY_CONFIGS_CSV), f"File {DAILY_CONFIGS_CSV} is missing."

    # Recompute expected state hashes based on truth data logic
    def compute_hash(configs):
        filtered = {k: v for k, v in configs.items() if v}
        sorted_keys = sorted(filtered.keys())
        formatted = "|".join(f"{k}:{filtered[k]}" for k in sorted_keys)
        return hashlib.sha256(formatted.encode('utf-8')).hexdigest()

    expected_rows = [
        {"date": "2023-10-01", "server_id": "srv1", "state_hash": compute_hash({"config_a": "v1", "config_b": "v2"})},
        {"date": "2023-10-01", "server_id": "srv2", "state_hash": compute_hash({"config_a": "on", "config_c": "yes"})},
        {"date": "2023-10-02", "server_id": "srv1", "state_hash": compute_hash({"config_b": "v2"})},
        {"date": "2023-10-02", "server_id": "srv1", "state_hash": compute_hash({"config_a": "v1", "config_c": "v3"})},
        {"date": "2023-10-02", "server_id": "srv2", "state_hash": compute_hash({"config_a": "on", "config_c": "yes"})},
        {"date": "2023-10-02", "server_id": "srv2", "state_hash": compute_hash({})},
    ]

    # Sort expected rows according to requirements: date, server_id, state_hash
    expected_rows.sort(key=lambda x: (x["date"], x["server_id"], x["state_hash"]))

    with open(DAILY_CONFIGS_CSV, 'r', newline='') as f:
        reader = csv.DictReader(f)
        actual_rows = list(reader)

    assert reader.fieldnames == ["date", "server_id", "state_hash"], \
        f"Expected CSV headers ['date', 'server_id', 'state_hash'], got {reader.fieldnames}"

    assert len(actual_rows) == len(expected_rows), \
        f"Expected {len(expected_rows)} rows in {DAILY_CONFIGS_CSV}, but got {len(actual_rows)}."

    for i, (expected, actual) in enumerate(zip(expected_rows, actual_rows)):
        assert actual["date"] == expected["date"], f"Row {i+1}: Expected date {expected['date']}, got {actual['date']}."
        assert actual["server_id"] == expected["server_id"], f"Row {i+1}: Expected server_id {expected['server_id']}, got {actual['server_id']}."
        assert actual["state_hash"] == expected["state_hash"], f"Row {i+1}: Expected state_hash {expected['state_hash']}, got {actual['state_hash']}."