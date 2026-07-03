# test_final_state.py
import os
import sqlite3

def test_script_exists_and_executable():
    script_path = '/home/user/process_config.sh'
    assert os.path.isfile(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

def test_db_exists():
    db_path = '/home/user/cmdb_tracking.db'
    assert os.path.isfile(db_path), f"Database not found at {db_path}"

def test_db_schema():
    db_path = '/home/user/cmdb_tracking.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='daily_status';")
    table_exists = cursor.fetchone()
    assert table_exists, "Table 'daily_status' does not exist in the database"

    cursor.execute("PRAGMA table_info(daily_status);")
    columns = {row[1]: row[2].upper() for row in cursor.fetchall()}

    assert 'date' in columns, "Column 'date' missing from 'daily_status'"
    assert 'server' in columns, "Column 'server' missing from 'daily_status'"
    assert 'status' in columns, "Column 'status' missing from 'daily_status'"

    conn.close()

def test_db_records():
    db_path = '/home/user/cmdb_tracking.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check total count
    cursor.execute("SELECT count(*) FROM daily_status;")
    count = cursor.fetchone()[0]
    assert count == 9, f"Expected 9 records in daily_status, found {count}"

    # Check UTF-8 conversion and specific record
    cursor.execute("SELECT count(*) FROM daily_status WHERE status = 'Dégradé';")
    degrade_count = cursor.fetchone()[0]
    assert degrade_count == 1, f"Expected 1 record with status 'Dégradé', found {degrade_count}. This might indicate an issue with character encoding."

    # Check formatting and data extraction
    cursor.execute("SELECT date, server, status FROM daily_status ORDER BY date, server, status LIMIT 1;")
    first_row = cursor.fetchone()
    expected_first_row = ('2023-10-01', 'Server1', 'Actif')
    assert first_row == expected_first_row, f"Expected first ordered row to be {expected_first_row}, found {first_row}"

    # Check another specific row to ensure time was stripped
    cursor.execute("SELECT count(*) FROM daily_status WHERE date = '2023-10-02' AND server = 'Server2' AND status = 'Actif';")
    week2_count = cursor.fetchone()[0]
    assert week2_count == 1, "Expected 1 record for 2023-10-02, Server2, Actif. Ensure time portion of timestamp is discarded."

    conn.close()