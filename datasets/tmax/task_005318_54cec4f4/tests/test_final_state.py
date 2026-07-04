# test_final_state.py

import os
import sqlite3
import subprocess
import pytest

def test_libtelemetry_compiled_correctly():
    lib_path = "/home/user/telemetry/libtelemetry.so"
    assert os.path.isfile(lib_path), f"Shared library {lib_path} was not created."

    # Check if it's a shared object
    file_output = subprocess.check_output(["file", lib_path]).decode("utf-8")
    assert "shared object" in file_output, f"{lib_path} is not a valid shared object. Ensure -shared and -fPIC are used."

    # Check for exported symbol
    try:
        nm_output = subprocess.check_output(["nm", "-D", lib_path]).decode("utf-8")
        assert "process_telemetry" in nm_output, f"Symbol 'process_telemetry' not found in {lib_path}"
    except subprocess.CalledProcessError:
        pytest.fail(f"Failed to run nm on {lib_path}. Is it a valid shared library?")

def test_database_schema_migrated():
    db_path = "/home/user/metrics.db"
    assert os.path.isfile(db_path), f"Database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(builds);")
    columns = {row[1]: row[2].upper() for row in cursor.fetchall()}
    conn.close()

    assert "memory_used" in columns, "Column 'memory_used' was not added to the builds table."
    assert "battery_drain" in columns, "Column 'battery_drain' was not added to the builds table."

    # Check data types if possible, though SQLite is flexible, the task specifies INTEGER and REAL
    assert "INT" in columns["memory_used"], "Column 'memory_used' should be of type INTEGER."
    assert "REAL" in columns["battery_drain"], "Column 'battery_drain' should be of type REAL."

def test_database_has_new_telemetry_data():
    db_path = "/home/user/metrics.db"
    assert os.path.isfile(db_path), f"Database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT device, build_time, memory_used, battery_drain FROM builds WHERE device='Pixel 7';")
        row = cursor.fetchone()
    except sqlite3.OperationalError as e:
        pytest.fail(f"Failed to query the builds table: {e}")
    finally:
        conn.close()

    assert row is not None, "No row found for device 'Pixel 7'. Did the Go program execute successfully?"

    device, build_time, memory_used, battery_drain = row
    assert device == "Pixel 7", f"Expected device 'Pixel 7', got {device}"
    assert abs(float(build_time) - 145.2) < 0.01, f"Expected build_time 145.2, got {build_time}"
    assert int(memory_used) == 4096, f"Expected memory_used 4096, got {memory_used}"
    assert abs(float(battery_drain) - 1.5) < 0.01, f"Expected battery_drain 1.5, got {battery_drain}"

def test_go_process_file_exists():
    go_file = "/home/user/telemetry/process.go"
    assert os.path.isfile(go_file), f"Go source file {go_file} does not exist."