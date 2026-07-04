# test_final_state.py
import os
import json
import sqlite3
import pytest

def test_json_log_exists_and_valid():
    log_path = '/home/user/processing_log.json'
    assert os.path.isfile(log_path), f"JSON log file {log_path} is missing."

    with open(log_path, 'r') as f:
        try:
            log_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("processing_log.json is not valid JSON.")

    assert "valid_rows_a" in log_data, "Key 'valid_rows_a' missing in JSON log."
    assert "invalid_rows_a" in log_data, "Key 'invalid_rows_a' missing in JSON log."
    assert "rows_b" in log_data, "Key 'rows_b' missing in JSON log."
    assert "merged_groups" in log_data, "Key 'merged_groups' missing in JSON log."

    assert log_data["valid_rows_a"] == 4, f"Expected 4 valid_rows_a, got {log_data['valid_rows_a']}"
    assert log_data["invalid_rows_a"] == 2, f"Expected 2 invalid_rows_a, got {log_data['invalid_rows_a']}"
    assert log_data["rows_b"] == 3, f"Expected 3 rows_b, got {log_data['rows_b']}"
    assert log_data["merged_groups"] == 4, f"Expected 4 merged_groups, got {log_data['merged_groups']}"

def test_database_exists_and_has_data():
    db_path = '/home/user/telemetry.db'
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT count(*) FROM merged_telemetry;")
        count = cursor.fetchone()[0]
        assert count == 4, f"Expected 4 rows in merged_telemetry, got {count}"

        # Check specific rows
        cursor.execute("SELECT avg_cpu_temp, avg_ram_usage FROM merged_telemetry WHERE epoch_sec=1698849001 AND machine_id='m1';")
        row1 = cursor.fetchone()
        assert row1 is not None, "Row for epoch_sec=1698849001, machine_id='m1' is missing."
        assert abs(row1[0] - 46.0) < 0.01, f"Expected avg_cpu_temp 46.0, got {row1[0]}"
        assert abs(row1[1] - 61.0) < 0.01, f"Expected avg_ram_usage 61.0, got {row1[1]}"

        cursor.execute("SELECT avg_cpu_temp, avg_ram_usage FROM merged_telemetry WHERE epoch_sec=1698849002 AND machine_id='m2';")
        row2 = cursor.fetchone()
        assert row2 is not None, "Row for epoch_sec=1698849002, machine_id='m2' is missing."
        assert abs(row2[0] - 50.0) < 0.01, f"Expected avg_cpu_temp 50.0, got {row2[0]}"
        assert abs(row2[1] - 0.0) < 0.01, f"Expected avg_ram_usage 0.0, got {row2[1]}"

        cursor.execute("SELECT avg_cpu_temp, avg_ram_usage FROM merged_telemetry WHERE epoch_sec=1698849003 AND machine_id='m1';")
        row3 = cursor.fetchone()
        assert row3 is not None, "Row for epoch_sec=1698849003, machine_id='m1' is missing."
        assert abs(row3[0] - 47.0) < 0.01, f"Expected avg_cpu_temp 47.0, got {row3[0]}"
        assert abs(row3[1] - 0.0) < 0.01, f"Expected avg_ram_usage 0.0, got {row3[1]}"

        cursor.execute("SELECT avg_cpu_temp, avg_ram_usage FROM merged_telemetry WHERE epoch_sec=1698849003 AND machine_id='m3';")
        row4 = cursor.fetchone()
        assert row4 is not None, "Row for epoch_sec=1698849003, machine_id='m3' is missing."
        assert abs(row4[0] - 0.0) < 0.01, f"Expected avg_cpu_temp 0.0, got {row4[0]}"
        assert abs(row4[1] - 80.0) < 0.01, f"Expected avg_ram_usage 80.0, got {row4[1]}"

    except sqlite3.OperationalError as e:
        pytest.fail(f"Database query failed: {e}. Ensure table 'merged_telemetry' exists with correct schema.")
    finally:
        conn.close()