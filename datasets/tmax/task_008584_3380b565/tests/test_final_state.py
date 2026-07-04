# test_final_state.py

import os
import sqlite3
import pytest

def test_cpp_source_exists():
    """Check if the C++ source file exists."""
    cpp_path = "/home/user/calc_restore_size.cpp"
    assert os.path.isfile(cpp_path), f"C++ source file missing at {cpp_path}"

def test_restore_report_exists():
    """Check if the restore report file exists."""
    report_path = "/home/user/restore_report.txt"
    assert os.path.isfile(report_path), f"Restore report missing at {report_path}"

def get_expected_sizes(db_path, targets):
    """Compute the expected total size for each target using a recursive query."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    WITH RECURSIVE ancestor_backups AS (
        SELECT id, name, size_mb
        FROM backups
        WHERE name = ?

        UNION ALL

        SELECT b.id, b.name, b.size_mb
        FROM backups b
        INNER JOIN dependencies d ON b.id = d.parent_id
        INNER JOIN ancestor_backups ab ON ab.id = d.id
    )
    SELECT SUM(size_mb) FROM ancestor_backups;
    """

    expected_results = []
    for target in targets:
        cursor.execute(query, (target,))
        result = cursor.fetchone()
        if result and result[0] is not None:
            expected_results.append(f"{target}: {result[0]} MB")
        else:
            expected_results.append(f"{target}: 0 MB")

    conn.close()
    return expected_results

def test_restore_report_contents():
    """Check if the restore report has the correct computed contents."""
    db_path = "/home/user/backups.db"
    targets_path = "/home/user/targets.txt"
    report_path = "/home/user/restore_report.txt"

    assert os.path.isfile(db_path), f"Database file missing at {db_path}"
    assert os.path.isfile(targets_path), f"Targets file missing at {targets_path}"

    with open(targets_path, "r") as f:
        targets = [line.strip() for line in f if line.strip()]

    expected_lines = get_expected_sizes(db_path, targets)

    with open(report_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in report, found {len(actual_lines)}"

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch on line {i + 1}: expected '{expected}', got '{actual}'"