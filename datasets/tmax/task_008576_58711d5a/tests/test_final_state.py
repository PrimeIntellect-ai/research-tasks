# test_final_state.py
import os
import csv
import re
from datetime import datetime, timedelta

def get_raw_data():
    raw_path = "/home/user/data/raw_logs.csv"
    assert os.path.isfile(raw_path), "raw_logs.csv is missing"

    with open(raw_path, "r", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
    return header, rows

def test_scripts_exist_and_executable():
    scripts = [
        "/home/user/etl/extract.sh",
        "/home/user/etl/transform.sh",
        "/home/user/etl/dag.sh"
    ]
    for script in scripts:
        assert os.path.isfile(script), f"Script missing: {script}"
        assert os.access(script, os.X_OK), f"Script not executable: {script}"

def test_extracted_csv():
    extracted_path = "/home/user/data/extracted.csv"
    assert os.path.isfile(extracted_path), "extracted.csv is missing"

    header, rows = get_raw_data()
    expected_lines = [",".join(header)]
    for row in rows:
        ts, level, msg = row
        msg_cleaned = msg.replace("\n", "\\n").replace("\r", "")
        expected_lines.append(f"{ts},{level},{msg_cleaned}")

    with open(extracted_path, "r") as f:
        actual_lines = [line.strip("\r\n") for line in f.readlines()]

    assert actual_lines == expected_lines, "extracted.csv does not match expected output"

def test_transformed_csv():
    transformed_path = "/home/user/data/transformed.csv"
    assert os.path.isfile(transformed_path), "transformed.csv is missing"

    _, rows = get_raw_data()

    if not rows:
        return

    timestamps = []
    error_counts = {}

    for row in rows:
        ts_str = row[0]
        level = row[1]
        dt = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
        minute_dt = dt.replace(second=0, microsecond=0)
        timestamps.append(minute_dt)

        if level == "ERROR":
            error_counts[minute_dt] = error_counts.get(minute_dt, 0) + 1

    min_dt = min(timestamps)
    max_dt = max(timestamps)

    expected_lines = []
    curr_dt = min_dt
    while curr_dt <= max_dt:
        count = error_counts.get(curr_dt, 0)
        expected_lines.append(f"{curr_dt.strftime('%Y-%m-%d %H:%M')},{count}")
        curr_dt += timedelta(minutes=1)

    with open(transformed_path, "r") as f:
        actual_lines = [line.strip("\r\n") for line in f.readlines() if line.strip()]

    assert actual_lines == expected_lines, "transformed.csv does not match expected gap-filled output"

def test_cron_backup():
    backup_path = "/home/user/crontab_backup.txt"
    assert os.path.isfile(backup_path), "crontab_backup.txt is missing"

    with open(backup_path, "r") as f:
        content = f.read()

    pattern1 = r"(?m)^(?:\*/5|0-59/5)\s+\*\s+\*\s+\*\s+\*.*dag\.sh"
    pattern2 = r"(?m)^[0,5,10,15,20,25,30,35,40,45,50,55]+\s+\*\s+\*\s+\*\s+\*.*dag\.sh"

    match = re.search(pattern1, content) or re.search(pattern2, content)
    assert match, "Crontab backup does not contain valid 5-minute schedule for dag.sh"