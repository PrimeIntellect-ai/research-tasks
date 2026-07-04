# test_final_state.py

import os
import csv
import sqlite3
import pytest

DB_PATH = '/home/user/compliance.db'
CSV_PATH = '/home/user/flagged_paths.csv'

def get_expected_results():
    """
    Recomputes the expected results from the database according to the rules:
    - A -> B (t1) and B -> C (t2)
    - A.domain == C.domain
    - A.domain != B.domain
    - t2.amount > B's average outgoing transaction amount
    - Sorted by t2.amount DESC, A.name ASC
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
    WITH B_Avg AS (
        SELECT source_id, AVG(amount) as avg_amount
        FROM transactions
        GROUP BY source_id
    )
    SELECT 
        A.name AS A_name,
        B.name AS B_name,
        C.name AS C_name,
        t1.amount AS t1_amount,
        t2.amount AS t2_amount
    FROM transactions t1
    JOIN transactions t2 ON t1.target_id = t2.source_id
    JOIN entities A ON t1.source_id = A.id
    JOIN entities B ON t1.target_id = B.id
    JOIN entities C ON t2.target_id = C.id
    JOIN B_Avg ON B.id = B_Avg.source_id
    WHERE A.domain = C.domain
      AND A.domain != B.domain
      AND t2.amount > B_Avg.avg_amount
    ORDER BY t2.amount DESC, A.name ASC
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return results

def test_csv_exists():
    assert os.path.exists(CSV_PATH), f"Expected output file not found: {CSV_PATH}"
    assert os.path.isfile(CSV_PATH), f"Path exists but is not a file: {CSV_PATH}"

def test_csv_content():
    expected_data = get_expected_results()

    with open(CSV_PATH, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)

        expected_header = ['A_name', 'B_name', 'C_name', 't1_amount', 't2_amount']
        assert header == expected_header, f"CSV header is incorrect. Expected {expected_header}, got {header}"

        rows = list(reader)

    assert len(rows) == len(expected_data), f"Expected {len(expected_data)} rows in CSV, but found {len(rows)}"

    for i, (actual_row, expected_row) in enumerate(zip(rows, expected_data)):
        # Convert expected row values to string for comparison with CSV
        expected_str_row = [
            str(expected_row[0]),
            str(expected_row[1]),
            str(expected_row[2]),
            str(float(expected_row[3])),
            str(float(expected_row[4]))
        ]

        # Ensure float formatting matches (e.g. 150.0)
        actual_formatted = [
            actual_row[0],
            actual_row[1],
            actual_row[2],
            str(float(actual_row[3])),
            str(float(actual_row[4]))
        ]

        assert actual_formatted == expected_str_row, f"Row {i+1} mismatch. Expected {expected_str_row}, got {actual_formatted}"

def test_audit_script_uses_window_function_or_cte():
    script_path = '/home/user/audit.py'
    assert os.path.exists(script_path), f"Script missing at {script_path}"

    with open(script_path, 'r') as f:
        content = f.read().upper()

    has_window_or_cte = ('AVG(' in content and 'OVER' in content) or ('WITH ' in content and 'AVG(' in content)
    assert has_window_or_cte, "The script does not appear to use a window function (AVG() OVER (...)) or CTE with AVG() as required."