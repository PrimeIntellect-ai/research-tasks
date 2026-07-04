# test_final_state.py
import os
import pytest

PLAN_FILE = "/home/user/restore_plan.txt"
C_FILE = "/home/user/planner.c"
EXEC_FILE = "/home/user/planner"

def test_c_source_exists():
    assert os.path.isfile(C_FILE), f"Source file {C_FILE} does not exist. You must write the C program."

def test_executable_exists():
    assert os.path.isfile(EXEC_FILE), f"Executable {EXEC_FILE} does not exist. Did you compile the program?"
    assert os.access(EXEC_FILE, os.X_OK), f"File {EXEC_FILE} is not executable."

def test_restore_plan():
    assert os.path.isfile(PLAN_FILE), f"Output file {PLAN_FILE} does not exist. Did you run the program?"

    with open(PLAN_FILE, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected = ['7', '8', '99']
    assert lines == expected, f"Expected restore plan {expected}, but got {lines}. Ensure you filter out FAILED backups and minimize total size."