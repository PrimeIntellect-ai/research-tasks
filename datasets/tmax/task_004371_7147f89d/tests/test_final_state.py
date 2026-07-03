# test_final_state.py

import os
import json
import pytest

CLEAN_DATA_PATH = "/home/user/clean_data.jsonl"
ANOMALIES_PATH = "/home/user/anomalies.csv"

def test_clean_data_exists_and_valid():
    """
    Validates that clean_data.jsonl exists, is properly formatted JSONL,
    and contains the exact expected valid records in order.
    """
    assert os.path.exists(CLEAN_DATA_PATH), f"Output file {CLEAN_DATA_PATH} is missing."
    assert os.path.isfile(CLEAN_DATA_PATH), f"{CLEAN_DATA_PATH} is not a file."

    with open(CLEAN_DATA_PATH, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    clean_records = []
    for i, line in enumerate(lines):
        try:
            record = json.loads(line)
            clean_records.append(record)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in {CLEAN_DATA_PATH} is not valid JSON: {line}")

    # Expected users based on the filtering rules:
    # alice (valid), bob (valid), sys (ERROR -> dropped), charlie (valid), dave (valid),
    # eve (len mismatch -> dropped), frank (valid), grace (valid)
    expected_users = ["alice", "bob", "charlie", "dave", "frank", "grace"]
    actual_users = [record.get("user") for record in clean_records]

    assert actual_users == expected_users, (
        f"Clean data does not contain the correct users in the correct order. "
        f"Expected {expected_users}, got {actual_users}."
    )

def test_anomalies_exists_and_valid():
    """
    Validates that anomalies.csv exists, has the correct header,
    and contains the expected anomaly records.
    """
    assert os.path.exists(ANOMALIES_PATH), f"Output file {ANOMALIES_PATH} is missing."
    assert os.path.isfile(ANOMALIES_PATH), f"{ANOMALIES_PATH} is not a file."

    with open(ANOMALIES_PATH, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) > 0, f"{ANOMALIES_PATH} is empty."

    expected_header = "timestamp,user,declared_len"
    assert lines[0] == expected_header, (
        f"Incorrect CSV header in {ANOMALIES_PATH}. "
        f"Expected '{expected_header}', got '{lines[0]}'."
    )

    # Frank is the only anomaly expected
    expected_anomalies = [
        "2023-10-01T10:00:07Z,frank,118"
    ]

    actual_anomalies = lines[1:]
    assert actual_anomalies == expected_anomalies, (
        f"Anomalies data mismatch. "
        f"Expected {expected_anomalies}, got {actual_anomalies}."
    )