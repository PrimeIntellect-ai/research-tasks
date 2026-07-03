# test_final_state.py

import os
import json
import sqlite3
import pytest

def test_index_exists_and_correct():
    db_path = "/home/user/backups.db"
    assert os.path.isfile(db_path), f"Database file missing: {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA index_info('idx_shard_status_date');")
    index_info = cursor.fetchall()

    assert len(index_info) > 0, "Index 'idx_shard_status_date' does not exist in backups.db"

    # PRAGMA index_info returns columns: (seqno, cid, name)
    columns = [row[2] for row in index_info]
    expected_columns = ["shard_id", "status", "backup_date"]

    assert columns == expected_columns, f"Index columns are incorrect. Expected {expected_columns}, got {columns}"
    conn.close()

def test_report_json_correctness():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"Report file missing: {report_path}"

    with open(report_path, 'r') as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{report_path} is not valid JSON.")

    assert isinstance(report_data, list), "Report JSON must be an array."

    # Based on the truth database, only 'shard-01' meets the criteria:
    # avg_duration > 300.0 AND failure_count >= 1
    # shard-01: last 3 successful durations are 310, 320, 330 -> avg = 320.0. Failed count = 1.
    # shard-02: avg = 400.0, Failed count = 0 (filtered out).
    # shard-03: avg = 100.0, Failed count = 2 (filtered out).

    assert len(report_data) == 1, f"Expected exactly 1 result in report.json, got {len(report_data)}"

    record = report_data[0]
    assert record.get("shard_id") == "shard-01", f"Expected shard_id 'shard-01', got {record.get('shard_id')}"
    assert record.get("avg_duration") == 320.0, f"Expected avg_duration 320.0, got {record.get('avg_duration')}"
    assert record.get("failure_count") == 1, f"Expected failure_count 1, got {record.get('failure_count')}"