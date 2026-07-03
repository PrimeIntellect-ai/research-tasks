# test_final_state.py

import os
import sqlite3
import csv
import pytest

DB_PATH = '/home/user/logistics.db'
OPTIMIZE_SQL_PATH = '/home/user/optimize.sql'
REPORT_PY_PATH = '/home/user/report.py'
METRICS_CSV_PATH = '/home/user/metrics.csv'

def get_golden_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = """
    WITH RecentDeliveries AS (
        SELECT
            courier_id,
            delivery_time_mins,
            AVG(delivery_time_mins) OVER (
                PARTITION BY courier_id
                ORDER BY created_at
                ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
            ) as rolling_avg_time,
            ROW_NUMBER() OVER (
                PARTITION BY courier_id
                ORDER BY created_at DESC
            ) as rn
        FROM deliveries
    ),
    LatestAverages AS (
        SELECT courier_id, rolling_avg_time as recent_avg_time
        FROM RecentDeliveries
        WHERE rn = 1
    ),
    FiveStarCounts AS (
        SELECT d.courier_id, COUNT(r.rating) as total_5_star_reviews
        FROM deliveries d
        JOIN reviews r ON d.id = r.delivery_id
        WHERE r.rating = 5
        GROUP BY d.courier_id
    )
    SELECT
        c.id as courier_id,
        c.name as courier_name,
        ROUND(l.recent_avg_time, 2) as recent_avg_time,
        COALESCE(f.total_5_star_reviews, 0) as total_5_star_reviews,
        DENSE_RANK() OVER (ORDER BY l.recent_avg_time ASC) as overall_rank
    FROM couriers c
    JOIN LatestAverages l ON c.id = l.courier_id
    LEFT JOIN FiveStarCounts f ON c.id = f.courier_id
    ORDER BY overall_rank ASC, courier_id ASC
    LIMIT 10;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows

def test_optimize_sql_exists():
    assert os.path.isfile(OPTIMIZE_SQL_PATH), f"{OPTIMIZE_SQL_PATH} is missing."

def test_optimize_sql_creates_indexes():
    # Read the SQL file
    with open(OPTIMIZE_SQL_PATH, 'r') as f:
        sql_content = f.read().lower()

    assert "create index" in sql_content, f"No CREATE INDEX statements found in {OPTIMIZE_SQL_PATH}"
    assert "deliveries" in sql_content, f"No index on deliveries table found in {OPTIMIZE_SQL_PATH}"
    assert "reviews" in sql_content, f"No index on reviews table found in {OPTIMIZE_SQL_PATH}"

def test_report_py_exists():
    assert os.path.isfile(REPORT_PY_PATH), f"{REPORT_PY_PATH} is missing."

def test_metrics_csv_correctness():
    assert os.path.isfile(METRICS_CSV_PATH), f"{METRICS_CSV_PATH} is missing."

    expected_rows = get_golden_data()

    with open(METRICS_CSV_PATH, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['courier_id', 'courier_name', 'recent_avg_time', 'total_5_star_reviews', 'overall_rank'], "CSV header does not match the expected format."

        actual_rows = list(reader)

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, but got {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert int(actual[0]) == expected[0], f"Row {i+1}: expected courier_id {expected[0]}, got {actual[0]}"
        assert actual[1] == expected[1], f"Row {i+1}: expected courier_name {expected[1]}, got {actual[1]}"
        assert float(actual[2]) == expected[2], f"Row {i+1}: expected recent_avg_time {expected[2]}, got {actual[2]}"
        assert int(actual[3]) == expected[3], f"Row {i+1}: expected total_5_star_reviews {expected[3]}, got {actual[3]}"
        assert int(actual[4]) == expected[4], f"Row {i+1}: expected overall_rank {expected[4]}, got {actual[4]}"