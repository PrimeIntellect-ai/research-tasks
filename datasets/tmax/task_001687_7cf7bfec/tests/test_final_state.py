# test_final_state.py
import os
import sqlite3
import csv
import pytest

def test_cleaned_data_csv():
    csv_path = "/home/user/cleaned_data.csv"
    assert os.path.isfile(csv_path), f"File not found: {csv_path}"

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ['date', 'entity_id', 'non_ascii_count', 'rolling_avg_score'], f"Incorrect header in {csv_path}"

        rows = list(reader)
        expected_rows = [
            ['2023-10-01', 'A', '1', '10.0'],
            ['2023-10-02', 'A', '1', '12.5'],
            ['2023-10-03', 'A', '6', '15.0'],
            ['2023-10-04', 'A', '1', '15.0'],
            ['2023-10-01', 'B', '0', '5.0'],
            ['2023-10-02', 'B', '0', '5.0'],
            ['2023-10-03', 'B', '0', '7.0']
        ]

        rows_sorted = sorted(rows, key=lambda x: (x[1], x[0]))
        expected_sorted = sorted(expected_rows, key=lambda x: (x[1], x[0]))

        assert len(rows_sorted) == len(expected_sorted), f"Expected {len(expected_sorted)} rows, got {len(rows_sorted)}"

        for r, e in zip(rows_sorted, expected_sorted):
            assert r[0] == e[0], f"Date mismatch: expected {e[0]}, got {r[0]}"
            assert r[1] == e[1], f"Entity mismatch: expected {e[1]}, got {r[1]}"
            assert r[2] == e[2], f"Non-ASCII count mismatch: expected {e[2]}, got {r[2]}"
            assert abs(float(r[3]) - float(e[3])) <= 0.01, f"Rolling avg mismatch: expected {e[3]}, got {r[3]}"

def test_sqlite_database():
    db_path = "/home/user/metrics.db"
    assert os.path.isfile(db_path), f"Database file not found: {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='entity_metrics'")
    assert cursor.fetchone() is not None, "Table 'entity_metrics' not found in database"

    cursor.execute("SELECT date, entity_id, non_ascii_count, rolling_avg_score FROM entity_metrics ORDER BY entity_id, date")
    rows = cursor.fetchall()

    expected = [
        ('2023-10-01', 'A', 1, 10.0),
        ('2023-10-02', 'A', 1, 12.5),
        ('2023-10-03', 'A', 6, 15.0),
        ('2023-10-04', 'A', 1, 15.0),
        ('2023-10-01', 'B', 0, 5.0),
        ('2023-10-02', 'B', 0, 5.0),
        ('2023-10-03', 'B', 0, 7.0)
    ]

    assert len(rows) == len(expected), f"Row count mismatch in DB. Expected {len(expected)}, got {len(rows)}"

    for r, e in zip(rows, expected):
        assert r[0] == e[0], f"Date mismatch in DB: expected {e[0]}, got {r[0]}"
        assert r[1] == e[1], f"Entity mismatch in DB: expected {e[1]}, got {r[1]}"
        assert int(r[2]) == e[2], f"Non-ASCII count mismatch in DB: expected {e[2]}, got {r[2]}"
        assert abs(float(r[3]) - e[3]) <= 0.01, f"Rolling avg mismatch in DB: expected {e[3]}, got {r[3]}"

    conn.close()