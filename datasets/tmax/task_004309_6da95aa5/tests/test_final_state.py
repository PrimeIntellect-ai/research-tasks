# test_final_state.py

import os
import sqlite3

def test_c_program_exists():
    """Verify that the C source and compiled executable exist."""
    assert os.path.isfile('/home/user/process.c'), "/home/user/process.c is missing."
    assert os.path.isfile('/home/user/process'), "/home/user/process executable is missing."
    assert os.access('/home/user/process', os.X_OK), "/home/user/process is not executable."

def test_pipeline_log_content():
    """Verify the pipeline.log contains the exact expected lines."""
    log_path = '/home/user/pipeline.log'
    assert os.path.isfile(log_path), f"{log_path} is missing."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "[INFO] Starting processing",
        "[INFO] Processed 7 rows",
        "[INFO] Output written to summary.csv"
    ]

    for expected in expected_lines:
        assert expected in lines, f"Expected log line '{expected}' not found in {log_path}."

def test_summary_csv_content():
    """Verify the summary.csv contains the correct aggregated statistics."""
    csv_path = '/home/user/summary.csv'
    assert os.path.isfile(csv_path), f"{csv_path} is missing."

    with open(csv_path, 'r') as f:
        content = f.read().strip()

    expected_content = (
        "1,370.75,165,150.25\n"
        "2,390.00,155,200.00\n"
        "3,650.50,210,350.50"
    )

    assert content == expected_content, f"Content of {csv_path} does not match expected output exactly."

def test_sqlite_database():
    """Verify the analytics.db SQLite database exists and contains the correct data."""
    db_path = '/home/user/analytics.db'
    assert os.path.isfile(db_path), f"{db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='store_stats';")
    assert cursor.fetchone() is not None, "Table 'store_stats' does not exist in analytics.db."

    # Check data
    cursor.execute("SELECT store_id, total_revenue, total_visitors, max_revenue FROM store_stats ORDER BY store_id;")
    rows = cursor.fetchall()
    conn.close()

    expected_rows = [
        (1, 370.75, 165, 150.25),
        (2, 390.0, 155, 200.0),
        (3, 650.5, 210, 350.5)
    ]

    assert len(rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in store_stats, found {len(rows)}."

    for row, expected in zip(rows, expected_rows):
        assert row[0] == expected[0], f"Expected store_id {expected[0]}, got {row[0]}."
        assert abs(row[1] - expected[1]) < 0.01, f"Expected total_revenue {expected[1]}, got {row[1]}."
        assert row[2] == expected[2], f"Expected total_visitors {expected[2]}, got {row[2]}."
        assert abs(row[3] - expected[3]) < 0.01, f"Expected max_revenue {expected[3]}, got {row[3]}."