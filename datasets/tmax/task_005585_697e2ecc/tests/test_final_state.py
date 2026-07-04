# test_final_state.py

import os
import sqlite3
import pytest
import re

def test_script_exists():
    script_path = "/home/user/etl_pipeline.py"
    assert os.path.isfile(script_path), f"ETL script {script_path} does not exist."

def test_files_moved_to_processed():
    processed_dir = "/home/user/processed"
    drops_dir = "/home/user/drops"

    expected_files = ["es.json", "fr.json", "de.json"]
    for file in expected_files:
        assert os.path.isfile(os.path.join(processed_dir, file)), f"File {file} was not moved to {processed_dir}."
        assert not os.path.isfile(os.path.join(drops_dir, file)), f"File {file} still exists in {drops_dir}."

def test_database_contents():
    db_path = "/home/user/loc_db.sqlite"
    assert os.path.isfile(db_path), f"Database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT lang, key FROM translations ORDER BY lang, key;")
    rows = cursor.fetchall()
    conn.close()

    expected_rows = [
        ("de", "error_not_found"),
        ("de", "logout_btn"),
        ("de", "welcome_msg"),
        ("es", "logout_btn"),
        ("es", "welcome_msg"),
        ("fr", "error_not_found"),
        ("fr", "logout_btn"),
    ]

    assert rows == expected_rows, f"Database entries do not match expected valid translations. Found: {rows}"

def test_invalid_translations_log():
    log_path = "/home/user/invalid_translations.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = {
        "es.json:error_not_found:INVALID_PLACEHOLDERS",
        "fr.json:welcome_msg:INVALID_PLACEHOLDERS"
    }

    assert set(lines) == expected_lines, f"Log file contents do not match expected invalid translations. Found: {lines}"

def test_cron_backup():
    cron_path = "/home/user/cron_backup.txt"
    assert os.path.isfile(cron_path), f"Cron backup file {cron_path} does not exist."

    with open(cron_path, "r") as f:
        content = f.read().strip()

    # Check for script path
    assert "/home/user/etl_pipeline.py" in content or "etl_pipeline.py" in content, "Cron backup does not contain the script name."

    # Check for 5-minute interval (either */5 or 0,5,10...)
    match_star_5 = re.search(r'\*/5\s+\*\s+\*\s+\*\s+\*', content)
    match_list_5 = re.search(r'(0,5,10,15,20,25,30,35,40,45,50,55|0-59/5)\s+\*\s+\*\s+\*\s+\*', content)

    assert match_star_5 or match_list_5, f"Cron backup does not specify a 5-minute interval. Found: {content}"