# test_final_state.py

import os
import sqlite3
import pytest

WORKSPACE_DIR = "/home/user/workspace"
CLEAN_DATA_CSV = os.path.join(WORKSPACE_DIR, "clean_data.csv")
DB_PATH = os.path.join(WORKSPACE_DIR, "patients.db")

EXPECTED_DB_ROWS = [
    (101, "AS", "[REDACTED]", 1, 120),
    (101, "AS", "[REDACTED]", 2, 118),
    (102, "BJ", "[REDACTED]", 1, 130),
    (102, "BJ", "[REDACTED]", 3, 140),
    (104, "DP", "[REDACTED]", 1, 115),
    (104, "DP", "[REDACTED]", 2, 116),
    (104, "DP", "[REDACTED]", 3, 117),
]

EXPECTED_CSV_LINES = [
    "ID,Initials,Email,Month,BP",
    "101,AS,[REDACTED],1,120",
    "101,AS,[REDACTED],2,118",
    "102,BJ,[REDACTED],1,130",
    "102,BJ,[REDACTED],3,140",
    "104,DP,[REDACTED],1,115",
    "104,DP,[REDACTED],2,116",
    "104,DP,[REDACTED],3,117",
]

def test_clean_data_csv_exists_and_content():
    assert os.path.isfile(CLEAN_DATA_CSV), f"File {CLEAN_DATA_CSV} does not exist."

    with open(CLEAN_DATA_CSV, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == EXPECTED_CSV_LINES, f"Content of {CLEAN_DATA_CSV} does not match the expected output."

def test_database_exists_and_content():
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} does not exist."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='bp_log';")
    assert cursor.fetchone() is not None, "Table 'bp_log' does not exist in the database."

    # Check rows
    cursor.execute("SELECT ID, Initials, Email, Month, BP FROM bp_log ORDER BY ID, Month;")
    rows = cursor.fetchall()

    assert rows == EXPECTED_DB_ROWS, f"Database rows in 'bp_log' do not match expected output."

    conn.close()

def test_makefile_exists():
    makefile_path = os.path.join(WORKSPACE_DIR, "Makefile")
    assert os.path.isfile(makefile_path), "Makefile is missing."

def test_c_program_exists():
    c_prog_path = os.path.join(WORKSPACE_DIR, "cleaner.c")
    assert os.path.isfile(c_prog_path), "cleaner.c is missing."

def test_executable_exists():
    exe_path = os.path.join(WORKSPACE_DIR, "cleaner")
    assert os.path.isfile(exe_path) and os.access(exe_path, os.X_OK), "Executable 'cleaner' is missing or not executable."