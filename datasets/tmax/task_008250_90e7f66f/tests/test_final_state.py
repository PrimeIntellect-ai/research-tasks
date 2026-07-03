# test_final_state.py

import os
import csv
import sqlite3
import pytest

def get_expected_clusters(db_path):
    """Compute the expected at-risk clusters directly from the database."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM clusters")
    clusters = cursor.fetchall()

    at_risk = []
    for cluster in clusters:
        c_id = cluster['id']
        c_name = cluster['name']

        # Get all backups for this cluster ordered by timestamp DESC
        cursor.execute(
            "SELECT timestamp, duration_sec, status FROM backups WHERE cluster_id = ? ORDER BY timestamp DESC", 
            (c_id,)
        )
        backups = cursor.fetchall()

        if not backups:
            continue

        # Criterion 1: most recent backup is FAILED
        if backups[0]['status'] == 'FAILED':
            at_risk.append(c_name)
            continue

        # Criterion 2: duration of most recent SUCCESS > 1.5 * avg of 3 preceding SUCCESS
        success_backups = [b for b in backups if b['status'] == 'SUCCESS']
        if len(success_backups) >= 4:
            latest_success = success_backups[0]['duration_sec']
            prev_3_success = success_backups[1:4]
            avg_prev_3 = sum(b['duration_sec'] for b in prev_3_success) / 3.0
            if latest_success > 1.5 * avg_prev_3:
                at_risk.append(c_name)

    conn.close()
    return sorted(at_risk)

def test_analyze_backups_cpp_exists():
    """Verify the C++ source file exists and includes sqlite3.h."""
    cpp_path = "/home/user/analyze_backups.cpp"
    assert os.path.isfile(cpp_path), f"Source file {cpp_path} does not exist."

    with open(cpp_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "#include <sqlite3.h>" in content, f"Source file {cpp_path} does not contain '#include <sqlite3.h>'."

def test_analyze_backups_binary_exists():
    """Verify the compiled binary exists and is executable."""
    bin_path = "/home/user/analyze_backups"
    assert os.path.isfile(bin_path), f"Compiled binary {bin_path} does not exist."
    assert os.access(bin_path, os.X_OK), f"File {bin_path} is not executable."

def test_at_risk_clusters_csv_correct():
    """Verify the CSV output matches the expected at-risk clusters."""
    csv_path = "/home/user/at_risk_clusters.csv"
    assert os.path.isfile(csv_path), f"Output file {csv_path} does not exist."

    db_path = "/home/user/backup_metadata.db"
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    expected_clusters = get_expected_clusters(db_path)

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"CSV file {csv_path} is empty."

    # Check header
    header = [col.strip() for col in rows[0]]
    assert header == ["cluster_name"], f"CSV header is incorrect. Expected ['cluster_name'], got {header}."

    # Check data rows
    actual_clusters = []
    for row in rows[1:]:
        if not row:
            continue
        actual_clusters.append(row[0].strip())

    assert actual_clusters == expected_clusters, (
        f"CSV contents do not match expected clusters.\n"
        f"Expected: {expected_clusters}\n"
        f"Actual: {actual_clusters}"
    )