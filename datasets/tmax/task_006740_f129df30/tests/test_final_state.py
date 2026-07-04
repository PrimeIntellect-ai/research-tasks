# test_final_state.py
import os
import json
import sqlite3
import pytest
import re

SCRIPT_PATH = '/home/user/analyze_backups.py'
REPORT_PATH = '/home/user/backup_report.json'
DB_PATH = '/home/user/backup_catalog.db'

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Script missing at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"Path {SCRIPT_PATH} is not a file"

def test_script_requirements():
    with open(SCRIPT_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for LIMIT and OFFSET (case-insensitive)
    assert re.search(r'\bLIMIT\b', content, re.IGNORECASE), "Script must use LIMIT for pagination"
    assert re.search(r'\bOFFSET\b', content, re.IGNORECASE), "Script must use OFFSET for pagination"

    # Check for parameterized queries (presence of '?')
    assert '?' in content, "Script must use parameterized queries (e.g., '?')"

def test_report_exists_and_content():
    assert os.path.exists(REPORT_PATH), f"Report missing at {REPORT_PATH}"

    with open(REPORT_PATH, 'r', encoding='utf-8') as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} does not contain valid JSON")

    assert "region" in report_data, "Report must contain 'region' key"
    assert report_data["region"] == "us-west-2", "Report region should be 'us-west-2'"
    assert "clusters" in report_data, "Report must contain 'clusters' key"

    # Derive expected data from the database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        SELECT c.id, c.name
        FROM clusters c
        WHERE c.region = 'us-west-2'
    """)
    clusters = c.fetchall()

    expected_clusters = {}
    for cid, cname in clusters:
        # Get latest successful backup
        c.execute("""
            SELECT id, timestamp
            FROM backups
            WHERE cluster_id = ? AND status = 'SUCCESS'
            ORDER BY timestamp DESC
            LIMIT 1
        """, (cid,))
        latest = c.fetchone()

        # Get total size of successful backups
        c.execute("""
            SELECT SUM(size_bytes)
            FROM backups
            WHERE cluster_id = ? AND status = 'SUCCESS'
        """, (cid,))
        total_size = c.fetchone()[0]

        if latest and total_size is not None:
            expected_clusters[cname] = {
                "latest_backup_id": latest[0],
                "latest_backup_timestamp": latest[1],
                "total_successful_size_bytes": total_size
            }

    conn.close()

    assert report_data["clusters"] == expected_clusters, "Report 'clusters' data does not match the expected derived data"