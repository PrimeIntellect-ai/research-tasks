# test_final_state.py

import os
import glob
import subprocess
import sqlite3
import json
import urllib.request
import time
import uuid
import pytest

CLEAN_DIR = "/app/corpora/clean"
EVIL_DIR = "/app/corpora/evil"
SANITIZER_SCRIPT = "/home/user/sanitizer.py"
DB_PATH = "/app/analytics.db"

def test_sanitizer_clean_corpus():
    assert os.path.isfile(SANITIZER_SCRIPT), f"Sanitizer script missing at {SANITIZER_SCRIPT}"

    clean_files = glob.glob(os.path.join(CLEAN_DIR, "*.json"))
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_files = []
    for filepath in clean_files:
        with open(filepath, 'r') as f:
            content = f.read()

        result = subprocess.run(
            ["python3", SANITIZER_SCRIPT, content],
            capture_output=True
        )
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean modified/rejected. Offending files: {failed_files[:10]}"

def test_sanitizer_evil_corpus():
    assert os.path.isfile(SANITIZER_SCRIPT), f"Sanitizer script missing at {SANITIZER_SCRIPT}"

    evil_files = glob.glob(os.path.join(EVIL_DIR, "*.json"))
    assert len(evil_files) > 0, "No evil corpus files found."

    bypassed_files = []
    for filepath in evil_files:
        with open(filepath, 'r') as f:
            content = f.read()

        result = subprocess.run(
            ["python3", SANITIZER_SCRIPT, content],
            capture_output=True
        )
        if result.returncode == 0:
            bypassed_files.append(os.path.basename(filepath))

    assert not bypassed_files, f"{len(bypassed_files)} of {len(evil_files)} evil bypassed. Offending files: {bypassed_files[:10]}"

def test_nginx_config():
    nginx_conf_path = "/app/nginx.conf"
    assert os.path.isfile(nginx_conf_path), f"Nginx config missing at {nginx_conf_path}"

    with open(nginx_conf_path, 'r') as f:
        config_content = f.read()

    # Check if proxy_pass points to port 5000
    assert "5000" in config_content, "Nginx config does not seem to forward to port 5000."

def test_database_initial_count():
    assert os.path.isfile(DB_PATH), f"Database file missing at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()

    assert count == 100, f"Expected 100 rows in database, but found {count}."

def test_e2e_pipeline():
    # Make sure DB exists
    assert os.path.isfile(DB_PATH), f"Database file missing at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    initial_count = cursor.fetchone()[0]
    conn.close()

    # Generate 10 valid payloads
    for i in range(10):
        payload = {
            "user_id": str(uuid.uuid4()),
            "username": f"user{i}test",
            "email": f"user{i}@example.com",
            "age": 25,
            "bio": "Just a test bio"
        }
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            "http://localhost:8000/submit",
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        try:
            urllib.request.urlopen(req, timeout=5)
        except Exception as e:
            pytest.fail(f"Failed to post data to Nginx: {e}")

    # Wait for background processing
    time.sleep(2)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    final_count = cursor.fetchone()[0]
    conn.close()

    expected_count = initial_count + 10
    assert final_count == expected_count, f"E2E test failed: expected DB count to be {expected_count}, but got {final_count}."