# test_final_state.py
import os
import json
import sqlite3
import subprocess
import re

def test_db_fixture_json():
    fixture_path = "/home/user/app/fixtures/db_fixture.json"
    assert os.path.isfile(fixture_path), f"Fixture file {fixture_path} is missing."

    with open(fixture_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{fixture_path} is not a valid JSON file.")

    assert data.get("host") == "127.0.0.1", "JSON 'host' value is incorrect."
    assert data.get("port") == "5432", "JSON 'port' value is incorrect."
    assert data.get("user") == "ci_tester", "JSON 'user' value is incorrect."

def test_sqlite_database_migration():
    db_path = "/home/user/app/test.db"
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name, status FROM users;")
        rows = cursor.fetchall()
    except sqlite3.OperationalError as e:
        pytest.fail(f"Failed to query database: {e}")
    finally:
        conn.close()

    assert len(rows) == 1, "Database does not contain exactly one user."
    assert rows[0] == ("admin", "active"), "Database seed data is incorrect."

def test_mock_service_log():
    log_path = "/home/user/app/mock_service.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read()

    assert "MOCK_ALIVE" in content, "The string 'MOCK_ALIVE' was not found in mock_service.log."

def test_benchmark_log():
    log_path = "/home/user/app/benchmark.log"
    assert os.path.isfile(log_path), f"Benchmark log file {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert re.match(r"^[0-9]+$", content), f"Benchmark log does not contain a valid integer: '{content}'"
    val = int(content)
    assert 2 <= val <= 10, f"Benchmark value {val} is outside the expected range (2-10 seconds)."

def test_mock_service_not_running():
    try:
        output = subprocess.check_output(["pgrep", "-f", "mock_service.sh"], text=True)
        running_pids = output.strip().split("\n")
    except subprocess.CalledProcessError:
        running_pids = []

    assert len(running_pids) == 0, "mock_service.sh is still running in the background."

def test_setup_script_exists_and_executable():
    script_path = "/home/user/app/test_env_setup.sh"
    assert os.path.isfile(script_path), f"Setup script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Setup script {script_path} is not executable."