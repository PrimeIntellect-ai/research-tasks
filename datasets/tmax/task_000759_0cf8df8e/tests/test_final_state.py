# test_final_state.py

import os
import sqlite3
import csv
import pytest

def test_error_log_verification():
    log_path = "/home/user/etl_errors.log"
    assert os.path.isfile(log_path), f"Error log file {log_path} is missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {log_path}, found {len(lines)}."
    assert "evt_004" in lines, "evt_004 is missing from the error log."
    assert "evt_008" in lines, "evt_008 is missing from the error log."

def test_database_state_verification():
    db_path = "/home/user/data.db"
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check total count
    cursor.execute("SELECT count(*) FROM events;")
    count = cursor.fetchone()[0]
    assert count == 5, f"Expected exactly 5 rows in events table, found {count}."

    # Check specific feature extraction logic
    expected_data = {
        "evt_001": {"hour": 14, "is_weekend": 0},
        "evt_003": {"hour": 9, "is_weekend": 1},
        "evt_005": {"hour": 23, "is_weekend": 1},
        "evt_006": {"hour": 10, "is_weekend": 0},
        "evt_009": {"hour": 2, "is_weekend": 1},
    }

    cursor.execute("SELECT event_id, hour, is_weekend FROM events;")
    rows = cursor.fetchall()

    for event_id, hour, is_weekend in rows:
        assert event_id in expected_data, f"Unexpected event_id {event_id} found in database."
        expected_hour = expected_data[event_id]["hour"]
        expected_weekend = expected_data[event_id]["is_weekend"]

        assert hour == expected_hour, f"Expected hour {expected_hour} for {event_id}, got {hour}."

        # SQLite boolean can be returned as 0/1 or False/True depending on driver/insert, handle both
        is_weekend_int = 1 if is_weekend in (1, '1', 'true', 'True', True) else 0
        assert is_weekend_int == expected_weekend, f"Expected is_weekend={expected_weekend} for {event_id}, got {is_weekend}."

    conn.close()

def test_csv_export_verification():
    csv_path = "/home/user/final_export.csv"
    assert os.path.isfile(csv_path), f"Exported CSV file {csv_path} is missing."

    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == 6, f"Expected 6 rows (1 header + 5 data) in {csv_path}, found {len(rows)}."

    header = rows[0]
    assert "event_id" in header, "Header row is missing 'event_id' column."

    # Check that we exported the correct 5 events
    event_ids = {row[0] for row in rows[1:]}
    expected_event_ids = {"evt_001", "evt_003", "evt_005", "evt_006", "evt_009"}
    assert event_ids == expected_event_ids, f"Exported CSV does not contain the expected event IDs. Got {event_ids}."