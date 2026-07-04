# test_final_state.py

import os
import sqlite3
import pytest

def get_expected_data():
    raw_file = "/home/user/raw_telemetry.csv"
    if not os.path.exists(raw_file):
        pytest.fail(f"Raw file {raw_file} is missing, cannot compute expected data.")

    expected = []
    last_val = None
    window = []

    with open(raw_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            ts = int(parts[0])
            user_id = parts[1]
            val_str = parts[2] if len(parts) > 2 else ""

            # Anonymize user_id
            if len(user_id) <= 4:
                anon_id = user_id
            else:
                anon_id = "*" * (len(user_id) - 4) + user_id[-4:]

            # Gap filling (forward fill)
            if val_str == "":
                val = last_val
            else:
                val = float(val_str)
            last_val = val

            # Rolling 3-period SMA
            window.append(val)
            if len(window) > 3:
                window.pop(0)
            sma = sum(window) / len(window)

            expected.append((ts, anon_id, round(val, 2), round(sma, 2)))

    return expected

def test_c_files_exist():
    """Test that the C source and compiled executable exist."""
    assert os.path.isfile("/home/user/process.c"), "C source file /home/user/process.c is missing."
    assert os.path.isfile("/home/user/process"), "Compiled executable /home/user/process is missing."

def test_processed_csv_exists():
    """Test that the intermediate processed CSV was created."""
    assert os.path.isfile("/home/user/processed_telemetry.csv"), "Processed CSV /home/user/processed_telemetry.csv is missing."

def test_database_exists():
    """Test that the SQLite database was created."""
    assert os.path.isfile("/home/user/telemetry.db"), "Database /home/user/telemetry.db is missing."

def test_database_contents():
    """Test that the database contains the correctly processed data."""
    db_path = "/home/user/telemetry.db"
    assert os.path.isfile(db_path), "Database /home/user/telemetry.db is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check table existence
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cleaned_data'")
    assert cursor.fetchone() is not None, "Table 'cleaned_data' does not exist in the database."

    # Fetch data
    try:
        cursor.execute("SELECT ts, anon_id, val, sma FROM cleaned_data ORDER BY ts ASC")
        rows = cursor.fetchall()
    except sqlite3.OperationalError as e:
        pytest.fail(f"Failed to query 'cleaned_data': {e}")
    finally:
        conn.close()

    expected = get_expected_data()
    assert len(rows) == len(expected), f"Expected {len(expected)} rows, found {len(rows)} in cleaned_data."

    for i, (row, exp) in enumerate(zip(rows, expected)):
        assert row[0] == exp[0], f"Row {i+1}: Expected timestamp {exp[0]}, got {row[0]}"
        assert row[1] == exp[1], f"Row {i+1}: Expected anon_id '{exp[1]}', got '{row[1]}'"
        assert round(row[2], 2) == exp[2], f"Row {i+1}: Expected val {exp[2]}, got {round(row[2], 2) if row[2] is not None else None}"
        assert round(row[3], 2) == exp[3], f"Row {i+1}: Expected sma {exp[3]}, got {round(row[3], 2) if row[3] is not None else None}"