# test_final_state.py

import os
import sqlite3
import pytest
from collections import defaultdict

DB_PATH = "/home/user/metrics.db"
CSV_PATH = "/home/user/raw_telemetry.csv"

def get_expected_aggregates():
    if not os.path.exists(CSV_PATH):
        pytest.fail(f"Input file {CSV_PATH} is missing. Cannot compute expected state.")

    aggregates = defaultdict(list)
    with open(CSV_PATH, 'r') as f:
        for line in f:
            # Strip newline exactly as read
            line = line.strip('\n')
            fields = line.split(',')

            # Quality Gate: strictly 4 comma-separated fields
            if len(fields) == 4:
                try:
                    ts = int(fields[0])
                    sensor_id = fields[1]
                    value = float(fields[2])

                    # Time-based Bucketing
                    bucket = (ts // 3600) * 3600
                    aggregates[(bucket, sensor_id)].append(value)
                except ValueError:
                    # Ignore rows where types don't match expectations
                    continue

    expected = []
    for (bucket, sensor_id), values in aggregates.items():
        avg = sum(values) / len(values)
        # Round to exactly 2 decimal places
        expected.append((bucket, sensor_id, round(avg, 2)))

    return sorted(expected)

def test_database_exists():
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} was not created."

def test_table_schema():
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} is missing."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(hourly_aggregates);")
    columns = cursor.fetchall()
    conn.close()

    assert len(columns) > 0, "Table 'hourly_aggregates' does not exist in the database."

    col_dict = {col[1]: col[2].upper() for col in columns}

    assert "bucket_time" in col_dict, "Column 'bucket_time' is missing."
    assert "INTEGER" in col_dict["bucket_time"], f"Column 'bucket_time' must be INTEGER, got {col_dict['bucket_time']}."

    assert "sensor_id" in col_dict, "Column 'sensor_id' is missing."
    assert "TEXT" in col_dict["sensor_id"], f"Column 'sensor_id' must be TEXT, got {col_dict['sensor_id']}."

    assert "avg_value" in col_dict, "Column 'avg_value' is missing."
    assert "REAL" in col_dict["avg_value"], f"Column 'avg_value' must be REAL, got {col_dict['avg_value']}."

def test_aggregated_data_correctness():
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} is missing."

    expected_data = get_expected_aggregates()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT bucket_time, sensor_id, avg_value FROM hourly_aggregates ORDER BY bucket_time ASC, sensor_id ASC;")
        actual_data = cursor.fetchall()
    except sqlite3.OperationalError as e:
        pytest.fail(f"Failed to query 'hourly_aggregates' table: {e}")
    finally:
        conn.close()

    # Ensure precision issues don't fail the test if they inserted correctly but sqlite returned float
    actual_data_rounded = [(row[0], row[1], round(float(row[2]), 2)) for row in actual_data]

    assert actual_data_rounded == expected_data, (
        f"Aggregated data mismatch.\n"
        f"Expected: {expected_data}\n"
        f"Got:      {actual_data_rounded}"
    )