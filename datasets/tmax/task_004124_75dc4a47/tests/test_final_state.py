# test_final_state.py

import os
import csv
import sqlite3
import pytest

def test_utf8_conversion():
    """Test that the raw file was converted to UTF-8 properly."""
    file_path = "/home/user/sensor_data_utf8.csv"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "Température mesurée" in content or "°C" in content, "Expected special characters not found in UTF-8 file."
    except UnicodeDecodeError:
        pytest.fail(f"The file {file_path} is not valid UTF-8.")

def test_sampled_data():
    """Test that the data was sampled correctly (first 20% per sensor)."""
    file_path = "/home/user/sensor_data_sampled.csv"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    counts = {'SENS_A': 0, 'SENS_B': 0, 'SENS_C': 0}
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sensor = row.get('sensor_id')
            if sensor in counts:
                counts[sensor] += 1
            else:
                pytest.fail(f"Unexpected sensor_id found: {sensor}")

    assert counts['SENS_A'] == 20, f"Expected 20 rows for SENS_A, got {counts['SENS_A']}"
    assert counts['SENS_B'] == 10, f"Expected 10 rows for SENS_B, got {counts['SENS_B']}"
    assert counts['SENS_C'] == 40, f"Expected 40 rows for SENS_C, got {counts['SENS_C']}"

def test_database_import():
    """Test that the sampled data was imported into the SQLite database."""
    db_path = "/home/user/sensors.db"
    assert os.path.isfile(db_path), f"Database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM readings")
        count = cursor.fetchone()[0]
        assert count == 70, f"Expected 70 rows in the 'readings' table, got {count}"
    except sqlite3.OperationalError as e:
        pytest.fail(f"Failed to query 'readings' table: {e}")
    finally:
        conn.close()

def test_average_temps_export():
    """Test that the average temperatures were exported correctly."""
    file_path = "/home/user/average_temps.csv"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    expected_rows = [
        ['sensor_id', 'avg_temperature'],
        ['SENS_A', '15.5'],
        ['SENS_B', '22.0'],
        ['SENS_C', '8.4']
    ]

    actual_rows = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            # Strip whitespace just in case
            actual_rows.append([col.strip() for col in row])

    # Convert floats for robust comparison if possible
    assert len(actual_rows) == 4, "Expected exactly 4 rows (including header) in average_temps.csv"
    assert actual_rows[0] == expected_rows[0], "Header mismatch in average_temps.csv"

    for i in range(1, 4):
        assert actual_rows[i][0] == expected_rows[i][0], f"Expected sensor_id {expected_rows[i][0]}, got {actual_rows[i][0]}"
        try:
            actual_temp = float(actual_rows[i][1])
            expected_temp = float(expected_rows[i][1])
            assert abs(actual_temp - expected_temp) < 0.01, f"Expected avg_temperature {expected_temp} for {expected_rows[i][0]}, got {actual_temp}"
        except ValueError:
            pytest.fail(f"Could not parse average temperature as float: {actual_rows[i][1]}")