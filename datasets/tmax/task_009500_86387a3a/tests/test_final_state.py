# test_final_state.py
import os
import stat
import subprocess
import sqlite3
import pytest

SCRIPT_PATH = '/home/user/generate_report.sh'
DB_PATH = '/home/user/company.db'

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable."

def test_database_integrity():
    assert os.path.exists(DB_PATH), f"Database {DB_PATH} is missing."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA integrity_check;")
    result = cursor.fetchone()[0]
    assert result == "ok", f"Database integrity check failed: {result}"
    conn.close()

def test_script_output_2023_01_02():
    expected_output = (
        "1,Frank,400,Alice -> Charlie -> Frank\n"
        "2,Dave,250,Alice -> Bob -> Dave\n"
        "3,Eve,200,Alice -> Bob -> Eve"
    )

    result = subprocess.run([SCRIPT_PATH, '2023-01-02'], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"

    output = result.stdout.strip()
    assert output == expected_output, f"Output for 2023-01-02 did not match expected.\nExpected:\n{expected_output}\nGot:\n{output}"

def test_script_output_2023_01_03():
    expected_output = (
        "1,Eve,500,Alice -> Bob -> Eve\n"
        "2,Frank,400,Alice -> Charlie -> Frank\n"
        "3,Dave,250,Alice -> Bob -> Dave"
    )

    result = subprocess.run([SCRIPT_PATH, '2023-01-03'], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"

    output = result.stdout.strip()
    assert output == expected_output, f"Output for 2023-01-03 did not match expected.\nExpected:\n{expected_output}\nGot:\n{output}"