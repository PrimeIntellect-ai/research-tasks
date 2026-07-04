# test_final_state.py

import os
import json
import sqlite3
import pytest

def test_telemetry_db_exists():
    """Test that the SQLite database file was created."""
    assert os.path.exists("/home/user/telemetry.db"), "The database file /home/user/telemetry.db was not created."

def test_telemetry_db_contents():
    """Test that the database contains the correctly processed es-MX records."""
    db_path = "/home/user/telemetry.db"
    jsonl_path = "/home/user/telemetry.jsonl"

    assert os.path.exists(db_path), f"{db_path} is missing."
    assert os.path.exists(jsonl_path), f"{jsonl_path} is missing."

    # Recompute expected values based on the actual telemetry.jsonl contents
    expected_records = []
    window = []

    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                # Skip malformed lines as per requirements
                continue

            if data.get("locale") == "es-MX":
                latency = float(data.get("latency_ms", 0))
                window.append(latency)
                if len(window) > 5:
                    window.pop(0)

                rolling_avg = sum(window) / len(window)
                expected_records.append({
                    "id": str(data.get("id")),
                    "timestamp": data.get("timestamp"),
                    "latency_ms": latency,
                    "rolling_avg_latency": rolling_avg
                })

    # Query the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check table existence
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='es_mx_stats'")
    assert cursor.fetchone() is not None, "Table 'es_mx_stats' does not exist in the database."

    # Fetch records
    cursor.execute("SELECT id, timestamp, latency_ms, rolling_avg_latency FROM es_mx_stats ORDER BY id ASC")
    db_records = cursor.fetchall()
    conn.close()

    # Sort expected records by ID as well to ensure matching order
    expected_records.sort(key=lambda x: str(x["id"]))

    assert len(db_records) == len(expected_records), f"Expected {len(expected_records)} valid es-MX records in DB, found {len(db_records)}."

    for db_rec, exp_rec in zip(db_records, expected_records):
        db_id, db_ts, db_lat, db_avg = db_rec
        assert str(db_id) == exp_rec["id"], f"Expected ID {exp_rec['id']}, got {db_id}."
        assert db_ts == exp_rec["timestamp"], f"Expected timestamp {exp_rec['timestamp']} for ID {db_id}, got {db_ts}."
        assert abs(float(db_lat) - exp_rec["latency_ms"]) < 1e-5, f"Expected latency {exp_rec['latency_ms']} for ID {db_id}, got {db_lat}."
        assert abs(float(db_avg) - exp_rec["rolling_avg_latency"]) < 1e-5, f"Expected rolling avg {exp_rec['rolling_avg_latency']} for ID {db_id}, got {db_avg}."