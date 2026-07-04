# test_final_state.py

import os
import subprocess
import pytest

def test_backup_planner_executable():
    exe_path = "/home/user/backup_planner"
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_backup_plan_output():
    plan_path = "/home/user/backup_plan.txt"
    assert os.path.isfile(plan_path), f"File {plan_path} does not exist."

    with open(plan_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = [
        "DB_AUTH",
        "DB_INVENTORY",
        "DB_LOGS",
        "DB_PRODUCTS",
        "DB_USERS",
        "DB_WEB"
    ]

    assert lines == expected, f"Output in {plan_path} does not match the expected sorted unique list of databases. Expected: {expected}, Got: {lines}"

def test_executable_behavior():
    exe_path = "/home/user/backup_planner"
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist."

    try:
        # Run the utility with a timeout to catch infinite loops
        result = subprocess.run([exe_path, "DB_WEB"], capture_output=True, text=True, timeout=2)
    except subprocess.TimeoutExpired:
        pytest.fail("Execution of backup_planner timed out. It likely still contains an infinite loop or combinatorial explosion.")

    assert result.returncode == 0, f"backup_planner exited with non-zero status: {result.returncode}"

    output_lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]

    # Check for duplicates
    assert len(output_lines) == len(set(output_lines)), "Output contains duplicate entries, tracking visited nodes is likely missing or incorrect."

    expected_set = {
        "DB_AUTH",
        "DB_INVENTORY",
        "DB_LOGS",
        "DB_PRODUCTS",
        "DB_USERS",
        "DB_WEB"
    }
    assert set(output_lines) == expected_set, f"Executable output set {set(output_lines)} does not match expected {expected_set}."