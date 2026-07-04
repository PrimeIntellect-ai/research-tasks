# test_final_state.py
import os
import re
import subprocess
import pytest

def test_cleaner_script_exists():
    script_path = "/home/user/cleaner.py"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_clean_data_content():
    clean_data_path = "/home/user/clean_data.csv"
    assert os.path.exists(clean_data_path), f"The output file {clean_data_path} does not exist."

    expected_content = """timestamp,sensor_id,value
2023-10-01T09:59:00,A,8.0
2023-10-01T10:00:00,A,10.0
2023-10-01T10:01:00,A,12.0
2023-10-01T10:02:00,A,14.0
2023-10-01T10:03:00,A,16.0
2023-10-01T10:04:00,A,18.0
2023-10-01T10:06:00,A,22.0"""

    with open(clean_data_path, "r") as f:
        content = f.read().strip()

    # Normalize line endings
    content = content.replace("\r\n", "\n")
    expected_content = expected_content.replace("\r\n", "\n")

    assert content == expected_content, "The content of clean_data.csv does not match the expected deduplicated, sorted, and interpolated data."

def test_cron_backup_exists_and_content():
    backup_path = "/home/user/cron_backup.txt"
    assert os.path.exists(backup_path), f"The cron backup file {backup_path} does not exist."

    with open(backup_path, "r") as f:
        content = f.read()

    # Match the cron job pattern
    pattern = r"^15\s+\*\s+\*\s+\*\s+\*\s+.*python3\s+/home/user/cleaner\.py$"

    match = any(re.match(pattern, line.strip()) for line in content.splitlines())
    assert match, "The cron_backup.txt does not contain the correct cron job entry."

def test_actual_crontab_entry():
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
        content = result.stdout
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read the current user's crontab.")

    pattern = r"^15\s+\*\s+\*\s+\*\s+\*\s+.*python3\s+/home/user/cleaner\.py$"

    match = any(re.match(pattern, line.strip()) for line in content.splitlines())
    assert match, "The actual crontab does not contain the correct cron job entry."