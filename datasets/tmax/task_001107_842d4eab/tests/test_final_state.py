# test_final_state.py
import os
import csv
import sqlite3
import pytest

DB_PATH = "/home/user/audit.db"
CPP_PATH = "/home/user/audit_checker.cpp"
EXE_PATH = "/home/user/audit_checker"
CSV_PATH = "/home/user/unauthorized_report.csv"

def get_expected_results(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
    WITH valid_access AS (
        SELECT source_id AS user_id, target_id AS server_id 
        FROM relationships 
        WHERE rel_type = 'HAS_ACCESS'
        UNION
        SELECT r1.source_id AS user_id, r2.target_id AS server_id 
        FROM relationships r1
        JOIN relationships r2 ON r1.target_id = r2.source_id
        WHERE r1.rel_type = 'MEMBER_OF' AND r2.rel_type = 'HAS_ACCESS'
    ),
    unauthorized_events AS (
        SELECT ae.user_id, ae.server_id
        FROM access_events ae
        JOIN entities s ON ae.server_id = s.id
        WHERE s.is_sensitive = 1
        AND NOT EXISTS (
            SELECT 1 FROM valid_access va 
            WHERE va.user_id = ae.user_id AND va.server_id = ae.server_id
        )
    ),
    user_totals AS (
        SELECT user_id, COUNT(*) as total_unauth
        FROM unauthorized_events
        GROUP BY user_id
    ),
    ranked_users AS (
        SELECT user_id, DENSE_RANK() OVER (ORDER BY total_unauth DESC) as rank_overall
        FROM user_totals
    ),
    grouped_events AS (
        SELECT user_id, server_id, COUNT(*) as unauthorized_attempts
        FROM unauthorized_events
        GROUP BY user_id, server_id
    )
    SELECT u.name as user_name, s.name as server_name, ge.unauthorized_attempts, ru.rank_overall
    FROM grouped_events ge
    JOIN entities u ON ge.user_id = u.id
    JOIN entities s ON ge.server_id = s.id
    JOIN ranked_users ru ON ge.user_id = ru.user_id
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    expected_rows = []
    for row in rows:
        expected_rows.append({
            "user_name": row["user_name"],
            "server_name": row["server_name"],
            "unauthorized_attempts": str(row["unauthorized_attempts"]),
            "rank_overall": str(row["rank_overall"])
        })
    return expected_rows

def test_files_exist():
    assert os.path.exists(CPP_PATH), f"C++ source file missing at {CPP_PATH}"
    assert os.path.exists(EXE_PATH), f"Compiled executable missing at {EXE_PATH}"
    assert os.access(EXE_PATH, os.X_OK), f"Executable at {EXE_PATH} is not executable"
    assert os.path.exists(CSV_PATH), f"Output CSV missing at {CSV_PATH}"

def test_csv_output():
    expected_data = get_expected_results(DB_PATH)

    with open(CSV_PATH, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header is not None, "CSV file is empty"

        expected_header = ["user_name", "server_name", "unauthorized_attempts", "rank_overall"]
        assert [h.strip() for h in header] == expected_header, f"CSV header {header} does not match expected {expected_header}"

        actual_rows = []
        for row in reader:
            if not row:
                continue
            assert len(row) == 4, f"Row {row} does not have exactly 4 columns"
            actual_rows.append({
                "user_name": row[0].strip(),
                "server_name": row[1].strip(),
                "unauthorized_attempts": row[2].strip(),
                "rank_overall": row[3].strip()
            })

    # Compare ignoring row order
    def sort_key(r):
        return (r["user_name"], r["server_name"])

    actual_sorted = sorted(actual_rows, key=sort_key)
    expected_sorted = sorted(expected_data, key=sort_key)

    assert len(actual_sorted) == len(expected_sorted), f"Expected {len(expected_sorted)} rows, found {len(actual_sorted)}"

    for actual, expected in zip(actual_sorted, expected_sorted):
        assert actual == expected, f"Row mismatch: expected {expected}, got {actual}"