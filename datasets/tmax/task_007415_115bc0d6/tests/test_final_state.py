# test_final_state.py
import os
import sqlite3
import pytest

def test_script_exists_and_executable():
    """Verify the script exists and is executable."""
    script_path = "/home/user/process_audit.sh"
    assert os.path.exists(script_path), f"Script not found at {script_path}"
    assert os.path.isfile(script_path), f"{script_path} is not a file"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable"

def test_database_exists():
    """Verify the SQLite database was created."""
    db_path = "/home/user/config_tracking.db"
    assert os.path.exists(db_path), f"Database not found at {db_path}"
    assert os.path.isfile(db_path), f"{db_path} is not a file"

def test_database_schema_and_content():
    """Verify the schema, row counts, and masking logic in the database."""
    db_path = "/home/user/config_tracking.db"
    if not os.path.exists(db_path):
        pytest.fail(f"Database {db_path} does not exist.")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check table existence
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='audit_log';")
    assert cursor.fetchone() is not None, "Table 'audit_log' does not exist in the database."

    # Check total rows
    cursor.execute("SELECT COUNT(*) FROM audit_log;")
    total_rows = cursor.fetchone()[0]
    assert total_rows == 3, f"Expected 3 rows in audit_log, found {total_rows}."

    # Check password masking
    cursor.execute("SELECT COUNT(*) FROM audit_log WHERE details LIKE '%password=***%';")
    masked_passwords = cursor.fetchone()[0]
    assert masked_passwords == 2, f"Expected 2 rows with masked passwords, found {masked_passwords}."

    # Check IP masking
    cursor.execute("SELECT COUNT(*) FROM audit_log WHERE details LIKE '%ip=%.XXX%';")
    masked_ips = cursor.fetchone()[0]
    assert masked_ips == 3, f"Expected 3 rows with masked IPs, found {masked_ips}."

    # Check specific extraction correctness
    cursor.execute("SELECT action FROM audit_log WHERE timestamp='2023-10-27T10:05:12Z';")
    row = cursor.fetchone()
    assert row is not None, "Record with timestamp '2023-10-27T10:05:12Z' not found."
    assert row[0] == "UPDATE_FW", f"Expected action 'UPDATE_FW' for timestamp '2023-10-27T10:05:12Z', found '{row[0]}'."

    # Ensure no unmasked passwords or unmasked last octets of IPs remain
    cursor.execute("SELECT COUNT(*) FROM audit_log WHERE details LIKE '%password=%' AND details NOT LIKE '%password=***%';")
    unmasked_passwords = cursor.fetchone()[0]
    assert unmasked_passwords == 0, f"Found {unmasked_passwords} rows with unmasked passwords."

    conn.close()