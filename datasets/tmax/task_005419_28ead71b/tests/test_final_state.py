# test_final_state.py
import os
import sqlite3
import subprocess
import re

def test_etl_script_executable():
    script_path = '/home/user/etl.sh'
    assert os.path.isfile(script_path), f"ETL script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"ETL script {script_path} is not executable."

def test_parsed_csv_contents():
    csv_path = '/home/user/parsed.csv'
    assert os.path.isfile(csv_path), f"Parsed CSV {csv_path} does not exist."

    with open(csv_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "2024-05-12T08:15:30,WARN,404,admincode,192.168.1.5",
        "2024-05-12T08:16:05,ERROR,500,sysadmin,10.0.0.9",
        "2024-05-12T08:17:22,INFO,NULL,bob,NULL",
        "2024-05-12T08:18:00,CRITICAL,503,NULL,172.16.0.4"
    ]

    assert lines == expected_lines, f"Contents of {csv_path} do not match the expected normalized output."

def test_sqlite_database_contents():
    db_path = '/home/user/metrics.db'
    assert os.path.isfile(db_path), f"Database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incidents';")
    assert cursor.fetchone() is not None, "Table 'incidents' does not exist in the database."

    cursor.execute("SELECT timestamp, level, code, user, ip FROM incidents ORDER BY timestamp ASC;")
    rows = cursor.fetchall()
    conn.close()

    expected_rows = [
        ("2024-05-12T08:15:30", "WARN", 404, "admincode", "192.168.1.5"),
        ("2024-05-12T08:16:05", "ERROR", 500, "sysadmin", "10.0.0.9"),
        ("2024-05-12T08:17:22", "INFO", "NULL", "bob", "NULL"),
        ("2024-05-12T08:18:00", "CRITICAL", 503, "NULL", "172.16.0.4")
    ]

    # SQLite might return integers as ints or strings if imported from CSV without strict typing, 
    # and "NULL" string as string. Let's normalize to strings for comparison.
    normalized_rows = [tuple(str(item) for item in row) for row in rows]
    expected_normalized = [tuple(str(item) for item in row) for row in expected_rows]

    assert normalized_rows == expected_normalized, "Database contents do not match the expected data."

def test_cron_schedule_file():
    txt_path = '/home/user/cron_schedule.txt'
    assert os.path.isfile(txt_path), f"Cron schedule file {txt_path} does not exist."

    with open(txt_path, 'r') as f:
        content = f.read().strip()

    # Normalize whitespace
    content_normalized = re.sub(r'\s+', ' ', content)
    expected_normalized = "15 * * * * /home/user/etl.sh /home/user/incoming.log /home/user/parsed.csv"

    assert expected_normalized in content_normalized, f"File {txt_path} does not contain the correct cron expression."

def test_cron_job_installed():
    try:
        result = subprocess.run(['crontab', '-u', 'user', '-l'], capture_output=True, text=True, check=True)
        crontab_content = result.stdout
    except subprocess.CalledProcessError:
        crontab_content = ""

    crontab_normalized = re.sub(r'\s+', ' ', crontab_content)
    expected_cmd = "15 * * * * /home/user/etl.sh /home/user/incoming.log /home/user/parsed.csv"

    assert expected_cmd in crontab_normalized, "The cron job was not correctly installed for the 'user' account."