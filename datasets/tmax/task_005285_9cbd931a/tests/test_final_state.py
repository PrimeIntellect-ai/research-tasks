# test_final_state.py

import os
import sqlite3
import subprocess
import glob
import requests
import pytest

def test_pylogparser_installed_and_fixed():
    try:
        import pylogparser
    except ImportError:
        pytest.fail("pylogparser is not installed or still has an ImportError.")

    # Test the parse_line function
    line = '10.0.0.1 - - [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326'
    try:
        result = pylogparser.parse_line(line)
    except Exception as e:
        pytest.fail(f"pylogparser.parse_line failed: {e}")

    assert isinstance(result, dict), "parse_line should return a dictionary"
    assert result.get('ip') == '10.0.0.1', "IP not parsed correctly"

def test_database_exists_and_schema_correct():
    db_path = "/home/user/logs.db"
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='access_logs';")
    table = cursor.fetchone()
    assert table is not None, "Table 'access_logs' does not exist in the database."

    cursor.execute("PRAGMA table_info(access_logs);")
    columns = [col[1] for col in cursor.fetchall()]
    expected_columns = {"ip", "timestamp", "method", "endpoint"}
    assert expected_columns.issubset(set(columns)), f"Table 'access_logs' missing required columns. Found: {columns}"

    conn.close()

def test_database_endpoints_normalized():
    db_path = "/home/user/logs.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT endpoint FROM access_logs;")
    rows = cursor.fetchall()
    assert len(rows) > 0, "No records found in access_logs table."

    for row in rows:
        endpoint = row[0]
        assert "?" not in endpoint, f"Endpoint '{endpoint}' is not normalized (contains '?')."

    conn.close()

def test_crontab_configured():
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True, check=True)
        crontab_output = result.stdout.strip()
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab. Is it installed?")

    # Check for the run_pipeline.sh script and correct schedule
    assert "/home/user/run_pipeline.sh" in crontab_output, "run_pipeline.sh not found in crontab."

    # Look for the '0 * * * *' schedule
    lines = crontab_output.split('\n')
    found_schedule = False
    for line in lines:
        if line.startswith('0 * * * *') and "/home/user/run_pipeline.sh" in line:
            found_schedule = True
            break

    assert found_schedule, f"Crontab does not have the correct schedule (0 * * * *) for the script. Output: {crontab_output}"

def test_api_server_ip_stats():
    # First, calculate expected stats from the database
    db_path = "/home/user/logs.db"
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT ip, COUNT(*) FROM access_logs GROUP BY ip;")
    expected_stats = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()

    assert len(expected_stats) > 0, "Database is empty, cannot verify API response."

    # Now query the API
    url = "http://127.0.0.1:8888/api/ip-stats"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        api_stats = response.json()
    except ValueError:
        pytest.fail("API response is not valid JSON.")

    assert api_stats == expected_stats, f"API stats do not match database stats. Expected: {expected_stats}, Got: {api_stats}"