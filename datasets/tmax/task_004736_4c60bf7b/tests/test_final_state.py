# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = '/home/user/audit_logs.db'
LOG_PATH = '/home/user/suspicious_users.log'
CPP_PATH = '/home/user/audit_analyzer.cpp'

def test_cpp_file_exists():
    """Test that the C++ source file was created."""
    assert os.path.exists(CPP_PATH), f"C++ source file missing at {CPP_PATH}"
    assert os.path.isfile(CPP_PATH), f"Path {CPP_PATH} exists but is not a file"

def test_log_file_exists():
    """Test that the output log file was generated."""
    assert os.path.exists(LOG_PATH), f"Log file missing at {LOG_PATH}"
    assert os.path.isfile(LOG_PATH), f"Path {LOG_PATH} exists but is not a file"

def test_log_file_contents():
    """Test that the log file contains the correct output computed from the database."""
    assert os.path.exists(DB_PATH), f"Database file missing at {DB_PATH}"

    # Recompute the expected results directly from the database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        WITH rolling AS (
            SELECT actor, SUM(risk) OVER (
                PARTITION BY actor 
                ORDER BY action_time 
                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
            ) as rolling_risk
            FROM system_access
            WHERE context_tag = 'PROD'
        )
        SELECT actor, MAX(rolling_risk) as max_risk
        FROM rolling
        GROUP BY actor
        ORDER BY max_risk DESC, actor ASC
        LIMIT 5;
    ''')
    rows = c.fetchall()
    conn.close()

    expected_lines = []
    for row in rows:
        expected_lines.append(f"Actor: {row[0]}, Max Rolling Risk: {row[1]:.2f}")

    # Read the actual log file contents
    with open(LOG_PATH, 'r') as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    # Compare lengths
    assert len(actual_lines) == len(expected_lines), (
        f"Expected {len(expected_lines)} lines in the log file, but found {len(actual_lines)}."
    )

    # Compare each line exactly
    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, (
            f"Line {i+1} mismatch.\n"
            f"Expected: '{expected}'\n"
            f"Actual:   '{actual}'"
        )