# test_final_state.py

import os
import json
import sqlite3
import subprocess
import pytest
import re

def is_clean(filepath):
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except Exception:
        return False

    if "users" in data and isinstance(data["users"], list):
        for user in data["users"]:
            if isinstance(user, dict):
                if user.get("privilege") == "root" and user.get("username") != "admin":
                    return False

    if "hostname" in data:
        hostname = data["hostname"]
        if not isinstance(hostname, str) or not re.match(r'^[a-zA-Z0-9\-]+$', hostname):
            return False

    return True

def test_video_alert_extraction():
    count_file = "/home/user/red_alert_count.txt"
    assert os.path.isfile(count_file), f"File {count_file} does not exist."

    with open(count_file, 'r') as f:
        content = f.read().strip()

    assert content == "42", f"Expected red alert count to be 42, but got {content}"

def test_configuration_sanitizer_adversarial():
    script_path = "/home/user/verify_config.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    clean_dir = "/app/corpora/clean/"
    evil_dir = "/app/corpora/evil/"

    clean_failed = []
    if os.path.isdir(clean_dir):
        for filename in os.listdir(clean_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(clean_dir, filename)
                result = subprocess.run(["python3", script_path, filepath], capture_output=True)
                if result.returncode != 0:
                    clean_failed.append(filename)

    evil_failed = []
    if os.path.isdir(evil_dir):
        for filename in os.listdir(evil_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(evil_dir, filename)
                result = subprocess.run(["python3", script_path, filepath], capture_output=True)
                if result.returncode == 0:
                    evil_failed.append(filename)

    errors = []
    if evil_failed:
        errors.append(f"{len(evil_failed)} evil files bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        errors.append(f"{len(clean_failed)} clean files modified/rejected: {', '.join(clean_failed)}")

    assert not errors, " | ".join(errors)

def test_etl_database_import():
    db_path = "/home/user/cmdb.db"
    assert os.path.isfile(db_path), f"Database {db_path} does not exist."

    incoming_dir = "/app/incoming_configs/"
    expected_clean_count = 0

    if os.path.isdir(incoming_dir):
        for filename in os.listdir(incoming_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(incoming_dir, filename)
                if is_clean(filepath):
                    expected_clean_count += 1

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT count(*) FROM valid_configs;")
        actual_count = cursor.fetchone()[0]
    except sqlite3.Error as e:
        pytest.fail(f"Database query failed: {e}")
    finally:
        conn.close()

    assert actual_count == expected_clean_count, f"Expected {expected_clean_count} records in valid_configs, but found {actual_count}."