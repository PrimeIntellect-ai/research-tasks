# test_final_state.py

import os
import sqlite3
import subprocess
import hashlib

def test_script_exists_and_executable():
    """Test that process_configs.sh exists and is executable."""
    script_path = "/home/user/process_configs.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_cron_job_configured():
    """Test that the cron job is scheduled for the user."""
    try:
        output = subprocess.check_output(["crontab", "-l", "-u", "user"], text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        output = e.output

    assert "0 * * * * /home/user/process_configs.sh" in output, "Cron job is not configured correctly for 'user'."

def test_database_records():
    """Test that the SQLite database has the correct deduplicated records."""
    db_path = "/home/user/config_inventory.db"
    assert os.path.isfile(db_path), f"Database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check table schema
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='configs';")
    assert cursor.fetchone() is not None, "Table 'configs' does not exist in the database."

    # Check total count
    cursor.execute("SELECT COUNT(*) FROM configs;")
    count = cursor.fetchone()[0]
    assert count == 3, f"Expected 3 records in the database, found {count}."

    # Check earliest timestamp deduplication
    cursor.execute("SELECT server_id FROM configs WHERE data=?;", ("port=80\nmode=active",))
    row = cursor.fetchone()
    assert row is not None, "Record for 'port=80\\nmode=active' is missing."
    assert row[0] == "srv2", f"Expected server_id 'srv2' for 'port=80\\nmode=active', got {row[0]}."

    cursor.execute("SELECT server_id FROM configs WHERE data=?;", ("port=8080\nmode=passive",))
    row = cursor.fetchone()
    assert row is not None, "Record for 'port=8080\\nmode=passive' is missing."
    assert row[0] == "srv1", f"Expected server_id 'srv1' for 'port=8080\\nmode=passive', got {row[0]}."

    cursor.execute("SELECT server_id FROM configs WHERE data=?;", ("port=443\nmode=active",))
    row = cursor.fetchone()
    assert row is not None, "Record for 'port=443\\nmode=active' is missing."
    assert row[0] == "srv3", f"Expected server_id 'srv3' for 'port=443\\nmode=active', got {row[0]}."

    conn.close()

def test_stats_csv():
    """Test that the stats.csv file contains correct aggregations and sorting."""
    csv_path = "/home/user/stats.csv"
    assert os.path.isfile(csv_path), f"Stats file {csv_path} does not exist."

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 4, f"Expected 4 lines in stats.csv (1 header + 3 data), found {len(lines)}."
    assert lines[0] == "hash,server_count", f"Expected header 'hash,server_count', got '{lines[0]}'."

    hash_passive = hashlib.sha256(b"port=8080\nmode=passive").hexdigest()
    hash_active_80 = hashlib.sha256(b"port=80\nmode=active").hexdigest()
    hash_active_443 = hashlib.sha256(b"port=443\nmode=active").hexdigest()

    expected_lines = [
        f"{hash_passive},2",
        f"{hash_active_80},2",
        f"{hash_active_443},1"
    ]

    # Sort the expected lines by count desc, then hash asc
    expected_lines.sort(key=lambda x: (-int(x.split(',')[1]), x.split(',')[0]))

    for i, expected in enumerate(expected_lines):
        assert lines[i+1] == expected, f"Line {i+2} in stats.csv is incorrect. Expected '{expected}', got '{lines[i+1]}'."