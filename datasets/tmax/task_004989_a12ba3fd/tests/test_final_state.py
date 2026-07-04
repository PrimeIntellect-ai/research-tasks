# test_final_state.py
import os
import json
import sqlite3
import pytest

DB_PATH = "/home/user/backups_meta.db"
OPTIMIZE_SQL_PATH = "/home/user/optimize.sql"
ANALYZE_PY_PATH = "/home/user/analyze_backups.py"
REPORT_JSON_PATH = "/home/user/report.json"

def test_optimize_sql_exists():
    """Check if the SQL optimization script exists."""
    assert os.path.exists(OPTIMIZE_SQL_PATH), f"{OPTIMIZE_SQL_PATH} does not exist."
    assert os.path.isfile(OPTIMIZE_SQL_PATH), f"{OPTIMIZE_SQL_PATH} is not a file."

def test_analyze_script_exists():
    """Check if the Python analysis script exists."""
    assert os.path.exists(ANALYZE_PY_PATH), f"{ANALYZE_PY_PATH} does not exist."
    assert os.path.isfile(ANALYZE_PY_PATH), f"{ANALYZE_PY_PATH} is not a file."

def test_database_indexes_applied():
    """Verify that an index on backups including server_id was created."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Get all indexes on the backups table
    cur.execute("PRAGMA index_list('backups');")
    indexes = cur.fetchall()

    found_valid_index = False
    for idx in indexes:
        idx_name = idx[1]
        cur.execute(f"PRAGMA index_info('{idx_name}');")
        columns = [row[2] for row in cur.fetchall()]
        if "server_id" in columns:
            found_valid_index = True
            break

    conn.close()
    assert found_valid_index, "No index found on 'backups' table that includes 'server_id'. The optimization script was either not written correctly or not executed."

def test_report_json_correctness():
    """Verify that report.json exists and contains the correct data."""
    assert os.path.exists(REPORT_JSON_PATH), f"{REPORT_JSON_PATH} does not exist."

    with open(REPORT_JSON_PATH, "r") as f:
        try:
            student_report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{REPORT_JSON_PATH} is not valid JSON.")

    assert isinstance(student_report, list), "The JSON report must be a list of objects."

    # Derive truth from the database
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        WITH running AS (
            SELECT 
                b.server_id,
                b.timestamp,
                SUM(b.size_bytes) OVER (PARTITION BY b.server_id ORDER BY b.timestamp ASC) as running_total
            FROM backups b
            WHERE b.status = 'SUCCESS'
        ),
        thresholds AS (
            SELECT 
                s.hostname,
                r.timestamp as crossing_timestamp,
                r.running_total as running_total_bytes,
                ROW_NUMBER() OVER (PARTITION BY r.server_id ORDER BY r.timestamp ASC) as rn
            FROM running r
            JOIN servers s ON r.server_id = s.id
            WHERE r.running_total > 500000000
        )
        SELECT hostname, crossing_timestamp, running_total_bytes
        FROM thresholds
        WHERE rn = 1
        ORDER BY hostname ASC
    ''')
    rows = cur.fetchall()
    conn.close()

    expected_report = [
        {
            "hostname": r[0],
            "crossing_timestamp": r[1],
            "running_total_bytes": r[2]
        }
        for r in rows
    ]

    assert len(student_report) == len(expected_report), f"Expected {len(expected_report)} records, got {len(student_report)}."

    for i, (student_row, expected_row) in enumerate(zip(student_report, expected_report)):
        assert isinstance(student_row, dict), f"Item at index {i} is not a JSON object."
        assert student_row.get("hostname") == expected_row["hostname"], f"Mismatch in hostname at index {i}. Expected {expected_row['hostname']}, got {student_row.get('hostname')}."
        assert student_row.get("crossing_timestamp") == expected_row["crossing_timestamp"], f"Mismatch in crossing_timestamp for {expected_row['hostname']}. Expected {expected_row['crossing_timestamp']}, got {student_row.get('crossing_timestamp')}."
        assert student_row.get("running_total_bytes") == expected_row["running_total_bytes"], f"Mismatch in running_total_bytes for {expected_row['hostname']}. Expected {expected_row['running_total_bytes']}, got {student_row.get('running_total_bytes')}."