# test_final_state.py

import os
import json
import sqlite3
from datetime import datetime

def test_transformed_events_exists():
    output_path = "/home/user/transformed_events.jsonl"
    assert os.path.exists(output_path), f"Output file {output_path} is missing."
    assert os.path.isfile(output_path), f"Path {output_path} is not a file."

def test_transformed_events_content():
    output_path = "/home/user/transformed_events.jsonl"
    assert os.path.exists(output_path), "Output file is missing."

    with open(output_path, "r") as f:
        lines = f.read().strip().splitlines()

    actual_records = []
    for line in lines:
        if not line.strip():
            continue
        try:
            actual_records.append(json.loads(line))
        except json.JSONDecodeError:
            assert False, f"Output file contains invalid JSON line: {line}"

    # Derive expected records directly from the database
    db_path = "/home/user/telemetry.db"
    assert os.path.exists(db_path), "Database file missing."

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
        SELECT id, uid, action, created_at
        FROM activity_logs
        ORDER BY uid, created_at
    """)
    rows = cur.fetchall()
    conn.close()

    user_prev_time = {}
    expected_records = []

    for row in rows:
        event_id, uid, action, created_at = row

        diff = None
        if uid in user_prev_time:
            fmt = '%Y-%m-%d %H:%M:%S'
            # Some timestamps might have fractional seconds, but the mock data is exact.
            # We handle standard ISO-8601-like formats found in the DB.
            try:
                t1 = datetime.strptime(created_at, fmt)
                t2 = datetime.strptime(user_prev_time[uid], fmt)
                diff = int((t1 - t2).total_seconds())
            except ValueError:
                pass

        user_prev_time[uid] = created_at

        if action == 'checkout':
            # Schema validation: user_id must be an integer
            if not isinstance(uid, int):
                continue

            expected_records.append({
                "user_id": uid,
                "event_id": event_id,
                "timestamp": created_at,
                "seconds_since_last_event": diff
            })

    # Sort both lists by event_id to ensure order independence
    def sort_key(r):
        return r.get("event_id", 0)

    actual_records.sort(key=sort_key)
    expected_records.sort(key=sort_key)

    assert len(actual_records) == len(expected_records), (
        f"Expected {len(expected_records)} valid checkout records, "
        f"but got {len(actual_records)} in the output file."
    )

    for actual, expected in zip(actual_records, expected_records):
        assert actual == expected, (
            f"Record mismatch.\nExpected: {expected}\nActual: {actual}\n"
            "Ensure that you are calculating the time difference correctly using Window functions, "
            "and that invalid records are discarded based on the JSON schema."
        )