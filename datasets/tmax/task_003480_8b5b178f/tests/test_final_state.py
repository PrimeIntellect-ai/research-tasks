# test_final_state.py

import os
import json
import sqlite3
import pytest

RAW_BACKUPS_PATH = "/home/user/raw_backups.jsonl"
DB_PATH = "/home/user/backups.db"
ANOMALIES_PATH = "/home/user/anomalies.json"

def get_normalized_data():
    if not os.path.exists(RAW_BACKUPS_PATH):
        pytest.fail(f"Raw backups file missing at {RAW_BACKUPS_PATH}")

    records = []
    with open(RAW_BACKUPS_PATH, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)

            db_name = data.get('database') or data.get('db')

            status = data.get('status') or data.get('state')
            if status == "ok":
                status = "success"

            if 'size' in data:
                size_bytes = data['size']
            else:
                size_bytes = data['metrics']['bytes']

            timestamp = data.get('ts') or data.get('time')

            records.append({
                "database_name": db_name,
                "status": status,
                "size_bytes": size_bytes,
                "timestamp": timestamp
            })
    return records

def compute_expected_anomalies(records):
    # Sort chronologically to compute rolling averages
    records.sort(key=lambda x: x['timestamp'])

    history = {}
    anomalies = []

    for r in records:
        db_name = r['database_name']
        status = r['status']
        size = r['size_bytes']
        ts = r['timestamp']

        if db_name not in history:
            history[db_name] = []

        if status == "success":
            prev_successes = history[db_name][-3:]
            if len(prev_successes) > 0:
                rolling_avg = sum(prev_successes) / len(prev_successes)
                if size > 1.2 * rolling_avg:
                    anomalies.append({
                        "database_name": db_name,
                        "timestamp": ts,
                        "size_bytes": size,
                        "rolling_avg": round(rolling_avg, 1)
                    })
            history[db_name].append(size)

    # Sort globally by timestamp descending
    anomalies.sort(key=lambda x: x['timestamp'], reverse=True)
    return anomalies

def test_sqlite_database_created_and_populated():
    assert os.path.exists(DB_PATH), f"SQLite database not found at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='backup_runs'")
    table_exists = cursor.fetchone()
    assert table_exists, "Table 'backup_runs' does not exist in the SQLite database."

    cursor.execute("SELECT COUNT(*) FROM backup_runs")
    count = cursor.fetchone()[0]

    expected_records = get_normalized_data()
    assert count == len(expected_records), f"Expected {len(expected_records)} rows in backup_runs, got {count}."

    conn.close()

def test_anomalies_json_output():
    assert os.path.exists(ANOMALIES_PATH), f"Anomalies JSON output not found at {ANOMALIES_PATH}"

    with open(ANOMALIES_PATH, 'r') as f:
        try:
            output = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {ANOMALIES_PATH} is not valid JSON.")

    expected_records = get_normalized_data()
    all_anomalies = compute_expected_anomalies(expected_records)

    assert "page" in output, "Missing 'page' key in JSON output."
    assert output["page"] == 1, f"Expected page 1, got {output['page']}."

    assert "page_size" in output, "Missing 'page_size' key in JSON output."
    assert output["page_size"] == 2, f"Expected page_size 2, got {output['page_size']}."

    assert "total_anomalies" in output, "Missing 'total_anomalies' key in JSON output."
    assert output["total_anomalies"] == len(all_anomalies), f"Expected total_anomalies {len(all_anomalies)}, got {output['total_anomalies']}."

    assert "data" in output, "Missing 'data' key in JSON output."
    assert isinstance(output["data"], list), "'data' should be a list."

    expected_page_data = all_anomalies[:2]

    assert len(output["data"]) == len(expected_page_data), f"Expected {len(expected_page_data)} items in 'data', got {len(output['data'])}."

    for i, (actual, expected) in enumerate(zip(output["data"], expected_page_data)):
        assert actual.get("database_name") == expected["database_name"], f"Mismatch in database_name at index {i}"
        assert actual.get("timestamp") == expected["timestamp"], f"Mismatch in timestamp at index {i}"
        assert actual.get("size_bytes") == expected["size_bytes"], f"Mismatch in size_bytes at index {i}"

        actual_avg = actual.get("rolling_avg")
        expected_avg = expected["rolling_avg"]
        assert actual_avg == expected_avg, f"Mismatch in rolling_avg at index {i}. Expected {expected_avg}, got {actual_avg}"