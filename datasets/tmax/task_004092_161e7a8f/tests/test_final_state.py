# test_final_state.py

import os
import json
import pytest

LOG_PATH = "/home/user/etl/pipeline.log"
OUTPUT_PATH = "/home/user/etl/output/clean_transactions.jsonl"

def test_pipeline_log_exists_and_correct():
    assert os.path.isfile(LOG_PATH), f"Log file missing at {LOG_PATH}"

    with open(LOG_PATH, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # We expect the last 3 lines to match the required format exactly
    assert len(lines) >= 3, "Log file does not contain enough lines"

    last_three = lines[-3:]
    assert last_three[0] == "[EXTRACT] records_read=8", f"Expected '[EXTRACT] records_read=8', got '{last_three[0]}'"
    assert last_three[1] == "[TRANSFORM] duplicates_dropped=3", f"Expected '[TRANSFORM] duplicates_dropped=3', got '{last_three[1]}'"
    assert last_three[2] == "[LOAD] records_written=5", f"Expected '[LOAD] records_written=5', got '{last_three[2]}'"

def test_output_file_exists_and_valid_jsonl():
    assert os.path.isfile(OUTPUT_PATH), f"Output file missing at {OUTPUT_PATH}"

    records = []
    with open(OUTPUT_PATH, "r") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                records.append(record)
            except json.JSONDecodeError:
                pytest.fail(f"Line {i+1} in {OUTPUT_PATH} is not valid JSON: {line}")

    assert len(records) == 5, f"Expected exactly 5 records in output, found {len(records)}"

    # Check fields
    required_fields = {"delivery_id", "user_id", "timestamp", "amount", "currency"}
    for i, record in enumerate(records):
        assert set(record.keys()) == required_fields, f"Record {i+1} missing or has extra fields: {record.keys()}"
        assert isinstance(record["amount"], float) or isinstance(record["amount"], int), f"Record {i+1} amount must be a number"

def test_output_records_correctness_and_sorting():
    assert os.path.isfile(OUTPUT_PATH), f"Output file missing at {OUTPUT_PATH}"

    records = []
    with open(OUTPUT_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    # Check sorting by timestamp
    timestamps = [r["timestamp"] for r in records]
    assert timestamps == sorted(timestamps), "Records in output file are not sorted chronologically by timestamp"

    # Expected truth data based on deduplication logic (CSV -> JSON -> XML)
    expected_records = [
        {"delivery_id": "d_1001", "user_id": "u_abc", "timestamp": "2023-10-01T10:00:00Z", "amount": 150.0, "currency": "USD"},
        {"delivery_id": "d_1002", "user_id": "u_xyz", "timestamp": "2023-10-01T10:05:00Z", "amount": 20.5, "currency": "EUR"},
        {"delivery_id": "d_2001", "user_id": "u_def", "timestamp": "2023-10-01T10:10:00Z", "amount": 99.99, "currency": "USD"},
        {"delivery_id": "d_2003", "user_id": "u_ghi", "timestamp": "2023-10-01T10:15:00Z", "amount": 50.0, "currency": "GBP"},
        {"delivery_id": "d_3002", "user_id": "u_jkl", "timestamp": "2023-10-01T10:20:00Z", "amount": 200.0, "currency": "JPY"}
    ]

    assert len(records) == len(expected_records), "Mismatch in number of output records"

    for i, (actual, expected) in enumerate(zip(records, expected_records)):
        assert actual["delivery_id"] == expected["delivery_id"], f"Record {i+1} delivery_id mismatch: {actual['delivery_id']} != {expected['delivery_id']}"
        assert actual["user_id"] == expected["user_id"], f"Record {i+1} user_id mismatch"
        assert actual["timestamp"] == expected["timestamp"], f"Record {i+1} timestamp mismatch"
        assert actual["currency"] == expected["currency"], f"Record {i+1} currency mismatch"
        assert float(actual["amount"]) == float(expected["amount"]), f"Record {i+1} amount mismatch: {actual['amount']} != {expected['amount']}"