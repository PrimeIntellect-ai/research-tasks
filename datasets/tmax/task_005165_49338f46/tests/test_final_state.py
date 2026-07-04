# test_final_state.py

import os
import sqlite3
import subprocess

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_filtered_csv_content():
    csv_path = "/home/user/filtered.csv"
    assert os.path.isfile(csv_path), f"Filtered CSV {csv_path} does not exist."

    expected_lines = [
        "162060,S2,45.0",
        "162180,S1,55.1",
        "162300,S3,33.3"
    ]

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_lines, f"Content of {csv_path} is incorrect. Expected {expected_lines}, got {lines}."

def test_sqlite_db_content():
    db_path = "/home/user/sensors.db"
    assert os.path.isfile(db_path), f"Database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check table existence
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='valid_readings';")
    assert cursor.fetchone() is not None, "Table 'valid_readings' does not exist in the database."

    # Check data
    cursor.execute("SELECT timestamp, sensor_id, reading FROM valid_readings ORDER BY timestamp ASC;")
    rows = cursor.fetchall()

    expected_rows = [
        (162060, 'S2', 45.0),
        (162180, 'S1', 55.1),
        (162300, 'S3', 33.3)
    ]

    assert rows == expected_rows, f"Database content is incorrect. Expected {expected_rows}, got {rows}."
    conn.close()

def test_cron_job_configured():
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
        crontab_content = result.stdout
    except subprocess.CalledProcessError:
        crontab_content = ""

    # Look for the specific cron schedule
    # "0 * * * * /home/user/pipeline.sh"
    # Allow some variation in spacing
    lines = crontab_content.strip().split('\n')
    found = False
    for line in lines:
        if line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 6:
            schedule = " ".join(parts[:5])
            command = " ".join(parts[5:])
            if schedule == "0 * * * *" and "/home/user/pipeline.sh" in command:
                found = True
                break

    assert found, "Cron job for /home/user/pipeline.sh to run at the top of every hour is not configured correctly."