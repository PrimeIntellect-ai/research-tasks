# test_final_state.py

import os
import sqlite3
import requests
import pytest
import subprocess
import time

def test_rules_db_exists():
    db_path = "/app/waf-service/db/rules.db"
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

def test_rules_db_schema():
    db_path = "/app/waf-service/db/rules.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(signatures);")
    columns = cursor.fetchall()
    conn.close()

    assert len(columns) > 0, "Table 'signatures' does not exist or has no columns."

    column_names = [col[1] for col in columns]
    assert "rule_hash" in column_names, "Column 'rule_hash' is missing from 'signatures' table."

def test_service_running_and_responds():
    url = "http://127.0.0.1:8443/"

    # Try a few times in case the service is slow to start
    max_retries = 3
    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=2)
            break
        except requests.exceptions.RequestException:
            if i == max_retries - 1:
                pytest.fail(f"Could not connect to service at {url}")
            time.sleep(1)

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert "WAF Active" in response.text, f"Expected 'WAF Active' in response body, got {response.text}"

def test_http_parser_ext_installed():
    try:
        # Check if the module can be imported in python3
        result = subprocess.run(
            ["python3", "-c", "import http_parser_ext"],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to import http_parser_ext in Python 3. Stderr: {e.stderr}")

def test_migrate_script_exists():
    script_path = "/app/waf-service/migrate_db.sh"
    assert os.path.isfile(script_path), f"Migration script {script_path} does not exist."