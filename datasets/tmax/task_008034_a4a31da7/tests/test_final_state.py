# test_final_state.py

import os
import json
import sqlite3
import subprocess
import pytest

SCRIPT_PATH = "/home/user/db_report.py"
REPORT_PATH = "/home/user/report.json"
DB_PATH = "/home/user/backups.db"
JSONL_PATH = "/home/user/nosql_metrics.jsonl"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable"

def test_script_uses_parameterized_queries():
    with open(SCRIPT_PATH, "r") as f:
        content = f.read()

    # Basic check to ensure parameterization is used instead of string formatting for SQL
    # It should contain a '?' for sqlite parameterization
    assert "?" in content, "Script does not appear to use SQLite parameterization ('?') for the query."

def test_run_script_and_verify_report():
    # Run the script with the required argument
    result = subprocess.run(
        ["python3", SCRIPT_PATH, "us-east-1"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script failed to execute. stderr: {result.stderr}"

    # Check if report.json was created
    assert os.path.isfile(REPORT_PATH), f"Report not generated at {REPORT_PATH}"

    # Calculate the expected truth from the actual data sources
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Find servers in us-east-1 with failed backups
    query = """
        SELECT s.hostname, COUNT(b.job_id)
        FROM servers s
        JOIN backup_jobs b ON s.id = b.server_id
        WHERE s.datacenter = ? AND b.status = 'FAILED'
        GROUP BY s.hostname
    """
    cursor.execute(query, ("us-east-1",))
    failed_servers = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()

    # Calculate bytes transferred from JSONL
    expected_report = {}
    for hostname, failures in failed_servers.items():
        expected_report[hostname] = {
            "failures": failures,
            "total_bytes": 0
        }

    with open(JSONL_PATH, "r") as f:
        for line in f:
            if not line.strip():
                continue
            record = json.loads(line)
            hostname = record.get("hostname")
            if hostname in expected_report and record.get("type") == "backup":
                expected_report[hostname]["total_bytes"] += record.get("bytes_transferred", 0)

    # Read the actual report
    with open(REPORT_PATH, "r") as f:
        try:
            actual_report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Report at {REPORT_PATH} is not valid JSON")

    assert actual_report == expected_report, f"Report content mismatch. Expected {expected_report}, got {actual_report}"