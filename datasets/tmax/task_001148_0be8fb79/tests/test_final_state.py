# test_final_state.py

import os
import csv
import sqlite3
import pytest

REPORT_PATH = "/home/user/report.csv"
DB_PATH = "/home/user/company.db"

def test_report_exists():
    assert os.path.exists(REPORT_PATH), f"Report file {REPORT_PATH} is missing."
    assert os.path.isfile(REPORT_PATH), f"{REPORT_PATH} is not a file."

def test_report_content():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} is missing."

    # Recompute expected data from the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
    WITH RECURSIVE subordinates AS (
        SELECT emp_id FROM org_chart WHERE emp_id = 1
        UNION ALL
        SELECT o.emp_id FROM org_chart o
        INNER JOIN subordinates s ON o.manager_id = s.emp_id
    ),
    sales_events AS (
        SELECT 
            e.emp_id,
            json_extract(e.payload, '$.timestamp') as event_timestamp,
            CAST(json_extract(e.payload, '$.amount') AS NUMERIC) as sale_amount
        FROM events e
        INNER JOIN subordinates s ON e.emp_id = s.emp_id
        WHERE json_extract(e.payload, '$.type') = 'sale'
    )
    SELECT 
        emp_id,
        event_timestamp,
        sale_amount,
        SUM(sale_amount) OVER (PARTITION BY emp_id ORDER BY event_timestamp ASC) as cumulative_sales
    FROM sales_events
    ORDER BY emp_id ASC, event_timestamp ASC;
    """

    cursor.execute(query)
    expected_rows = cursor.fetchall()
    conn.close()

    # Format expected rows as strings to match CSV reading
    expected_csv_rows = []
    for row in expected_rows:
        expected_csv_rows.append([str(row[0]), str(row[1]), str(row[2]), str(row[3])])

    expected_header = ["emp_id", "event_timestamp", "sale_amount", "cumulative_sales"]

    # Read the generated CSV
    actual_csv_rows = []
    with open(REPORT_PATH, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            actual_header = next(reader)
        except StopIteration:
            pytest.fail("The generated CSV file is empty.")

        for row in reader:
            if any(row):  # skip empty rows
                actual_csv_rows.append(row)

    assert actual_header == expected_header, f"CSV header mismatch. Expected {expected_header}, got {actual_header}."

    assert len(actual_csv_rows) == len(expected_csv_rows), f"CSV row count mismatch. Expected {len(expected_csv_rows)} data rows, got {len(actual_csv_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_csv_rows, expected_csv_rows)):
        assert actual == expected, f"Data row {i+1} mismatch. Expected {expected}, got {actual}."