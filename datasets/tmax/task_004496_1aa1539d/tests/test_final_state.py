# test_final_state.py

import os
import pytest

CSV_PATH = "/home/user/backup_plan.csv"

EXPECTED_CSV_CONTENT = """table_name,backup_level,path
audit_logs,0,audit_logs
users,0,users
posts,1,posts->users
user_settings,1,user_settings->users
comments,2,comments->posts->users
likes,3,likes->comments->posts->users"""

def test_csv_file_exists():
    """Check if the backup_plan.csv file exists."""
    assert os.path.isfile(CSV_PATH), f"CSV file missing at {CSV_PATH}"

def test_csv_file_content():
    """Check if the backup_plan.csv file contains the correct output."""
    assert os.path.isfile(CSV_PATH), f"CSV file missing at {CSV_PATH}"

    with open(CSV_PATH, "r") as f:
        content = f.read().strip()

    # Standardize line endings just in case
    content_lines = [line.strip() for line in content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in EXPECTED_CSV_CONTENT.splitlines() if line.strip()]

    assert content_lines == expected_lines, "The CSV content does not match the expected backup plan."