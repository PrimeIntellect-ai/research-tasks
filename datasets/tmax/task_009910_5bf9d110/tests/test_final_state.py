# test_final_state.py

import os
import stat
import pytest

SCRIPT_PATH = "/home/user/generate_backup_plan.sh"
PLAN_PATH = "/home/user/backup_plan.txt"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script file {SCRIPT_PATH} does not exist."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script file {SCRIPT_PATH} is not executable."

def test_backup_plan_contents():
    assert os.path.isfile(PLAN_PATH), f"Backup plan file {PLAN_PATH} does not exist."

    expected_lines = [
        "[BACKUP-EXEC] Starting snapshot for volume: vol-prod-data1",
        "[BACKUP-EXEC] Starting snapshot for volume: vol-prod-data2",
        "[BACKUP-EXEC] Starting snapshot for volume: vol-prod-log1",
        "[BACKUP-EXEC] Starting snapshot for volume: vol-shared-backup"
    ]

    with open(PLAN_PATH, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {PLAN_PATH} do not match expected output. "
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )