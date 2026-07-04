# test_final_state.py
import os
import sqlite3
import subprocess
import pytest

def test_optimize_sql_exists_and_contains_indexes():
    sql_path = "/home/user/optimize.sql"
    assert os.path.isfile(sql_path), f"File {sql_path} does not exist."

    with open(sql_path, "r") as f:
        content = f.read().upper()

    assert "CREATE INDEX" in content, f"{sql_path} does not contain CREATE INDEX statements."

def test_indexes_applied_to_db():
    db_path = "/home/user/source.db"
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_autoindex%';")
    indexes = cursor.fetchall()
    conn.close()

    assert len(indexes) >= 3, f"Expected at least 3 custom indexes in {db_path}, found {len(indexes)}."

def test_etl_script_exists_and_executable():
    script_path = "/home/user/etl.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()
    assert "?" in content, f"Script {script_path} does not seem to use parameterized queries (missing '?')."

def test_etl_script_execution_2023_10_15():
    script_path = "/home/user/etl.sh"
    date_arg = "2023-10-15"
    report_path = f"/home/user/report_{date_arg}.csv"

    if os.path.exists(report_path):
        os.remove(report_path)

    result = subprocess.run([script_path, date_arg], capture_output=True, text=True)
    assert result.returncode == 0, f"Execution of {script_path} failed: {result.stderr}"

    assert os.path.isfile(report_path), f"Report file {report_path} was not created."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "customer_id,customer_name,total_spent",
        "1,Alice Smith,40.00",
        "2,Bob Jones,21.00"
    ]

    assert lines == expected_lines, f"Contents of {report_path} do not match expected output for {date_arg}."

def test_etl_script_execution_2023_10_16():
    script_path = "/home/user/etl.sh"
    date_arg = "2023-10-16"
    report_path = f"/home/user/report_{date_arg}.csv"

    if os.path.exists(report_path):
        os.remove(report_path)

    result = subprocess.run([script_path, date_arg], capture_output=True, text=True)
    assert result.returncode == 0, f"Execution of {script_path} failed: {result.stderr}"

    assert os.path.isfile(report_path), f"Report file {report_path} was not created."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "customer_id,customer_name,total_spent",
        "1,Alice Smith,15.50"
    ]

    assert lines == expected_lines, f"Contents of {report_path} do not match expected output for {date_arg}."