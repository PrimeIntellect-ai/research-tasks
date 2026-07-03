# test_final_state.py

import os
import sqlite3
import csv
import math
import pytest

DB_PATH = "/home/user/backup_metadata.db"
SCRIPT_PATH = "/home/user/analyze_backups.py"
PLAN_PATH = "/home/user/plan.txt"
CSV_PATH = "/home/user/anomalies.csv"

def test_script_exists():
    """Test that the analyze_backups.py script exists."""
    assert os.path.exists(SCRIPT_PATH), f"Script missing at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"Expected a file at {SCRIPT_PATH}"

def test_index_created():
    """Test that a new index was created on the backup_logs table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name 
        FROM sqlite_master 
        WHERE type='index' AND tbl_name='backup_logs' AND name NOT LIKE 'sqlite_autoindex%';
    """)
    indexes = cursor.fetchall()
    conn.close()

    assert len(indexes) > 0, "No custom index was created on the backup_logs table."

def test_plan_txt_contains_using_index():
    """Test that the EXPLAIN QUERY PLAN output mentions USING INDEX."""
    assert os.path.exists(PLAN_PATH), f"Execution plan output missing at {PLAN_PATH}"

    with open(PLAN_PATH, "r") as f:
        content = f.read().upper()

    assert "USING INDEX" in content or "USING COVERING INDEX" in content, \
        "The execution plan in plan.txt does not indicate that an index was used."

def test_anomalies_csv_content():
    """Test that the anomalies.csv contains the expected anomaly data."""
    assert os.path.exists(CSV_PATH), f"Anomalies CSV missing at {CSV_PATH}"

    with open(CSV_PATH, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) >= 2, "The anomalies.csv file must contain a header and at least one data row."

    header = rows[0]
    expected_header = ['server_name', 'latest_size', 'avg_recent_size']
    assert header == expected_header, f"Expected header {expected_header}, but got {header}"

    # Extract data rows
    data_rows = rows[1:]

    # Filter out empty rows if any
    data_rows = [row for row in data_rows if row]

    assert len(data_rows) == 1, f"Expected exactly 1 anomaly row, but got {len(data_rows)}"

    anomaly = data_rows[0]
    assert anomaly[0] == "db-server-04", f"Expected server_name 'db-server-04', got '{anomaly[0]}'"

    latest_size = float(anomaly[1])
    avg_recent_size = float(anomaly[2])

    assert latest_size == 100000000, f"Expected latest_size 100000000, got {latest_size}"
    assert math.isclose(avg_recent_size, 46666666.67, rel_tol=1e-5), \
        f"Expected avg_recent_size around 46666666.67, got {avg_recent_size}"