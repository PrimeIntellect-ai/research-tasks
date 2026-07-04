# test_final_state.py

import os
import csv
import sqlite3
import pytest

def get_expected_data():
    db_path = "/home/user/metrics.db"
    assert os.path.exists(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Recompute the expected data based on the requirements
    query = """
        SELECT d.name, m.timestamp, m.reading,
               AVG(m.reading) OVER (
                   PARTITION BY m.device_id 
                   ORDER BY m.timestamp 
                   ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
               ) as rolling_avg
        FROM measurements m
        JOIN devices d ON m.device_id = d.id
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    # Filter: reading > 45.0
    filtered = [r for r in rows if r[2] > 45.0]

    # Sort: device name (ASC), timestamp (ASC)
    filtered.sort(key=lambda x: (x[0], x[1]))

    # Paginate: LIMIT 10 OFFSET 5
    paginated = filtered[5:15]

    return paginated

def test_results_csv_exists():
    csv_path = "/home/user/results.csv"
    assert os.path.exists(csv_path), f"Output file {csv_path} was not generated."
    assert os.path.isfile(csv_path), f"{csv_path} is not a file."

def test_results_csv_content():
    csv_path = "/home/user/results.csv"
    if not os.path.exists(csv_path):
        pytest.fail(f"Cannot test content, {csv_path} is missing.")

    expected_data = get_expected_data()

    with open(csv_path, mode='r', newline='') as f:
        reader = list(csv.reader(f))

    assert len(reader) > 0, "CSV file is empty."

    header = reader[0]
    expected_header = ["device_name", "timestamp", "reading", "rolling_avg"]
    assert header == expected_header, f"CSV header is incorrect. Expected {expected_header}, got {header}."

    actual_data = reader[1:]
    assert len(actual_data) == len(expected_data), f"Expected exactly {len(expected_data)} rows of data, got {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert len(actual) == 4, f"Row {i+1} does not have exactly 4 columns: {actual}"

        actual_device, actual_ts, actual_reading, actual_rolling = actual
        exp_device, exp_ts, exp_reading, exp_rolling = expected

        assert actual_device == exp_device, f"Row {i+1}: expected device_name '{exp_device}', got '{actual_device}'"
        assert actual_ts == exp_ts, f"Row {i+1}: expected timestamp '{exp_ts}', got '{actual_ts}'"

        try:
            actual_reading_float = float(actual_reading)
        except ValueError:
            pytest.fail(f"Row {i+1}: reading '{actual_reading}' is not a valid float.")

        assert abs(actual_reading_float - exp_reading) < 1e-6, f"Row {i+1}: expected reading {exp_reading}, got {actual_reading_float}"

        exp_rolling_str = f"{exp_rolling:.2f}"
        assert actual_rolling == exp_rolling_str, f"Row {i+1}: expected rolling_avg '{exp_rolling_str}' (formatted to 2 decimals), got '{actual_rolling}'"