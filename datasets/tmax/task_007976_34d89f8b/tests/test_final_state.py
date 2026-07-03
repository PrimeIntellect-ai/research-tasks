# test_final_state.py

import os
import sqlite3
import subprocess
import pytest

SCRIPT_PATH = "/home/user/get_subordinates.sh"
DB_PATH = "/home/user/db/org_chart.db"
LOG_PATH = "/home/user/top_vp.log"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_script_output_vp1():
    result = subprocess.run([SCRIPT_PATH, "2"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"
    expected_output = "Subordinate count for 2: 7"
    assert expected_output in result.stdout.strip(), f"Expected '{expected_output}', got '{result.stdout.strip()}'"

def test_script_output_director1():
    result = subprocess.run([SCRIPT_PATH, "4"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"
    expected_output = "Subordinate count for 4: 3"
    assert expected_output in result.stdout.strip(), f"Expected '{expected_output}', got '{result.stdout.strip()}'"

def test_hierarchy_metrics_table():
    assert os.path.isfile(DB_PATH), f"Database {DB_PATH} does not exist."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='hierarchy_metrics';")
    assert cursor.fetchone() is not None, "Table 'hierarchy_metrics' does not exist."

    # Check specific values
    cursor.execute("SELECT total_subordinates FROM hierarchy_metrics WHERE emp_id=1;")
    ceo_count = cursor.fetchone()
    assert ceo_count is not None and ceo_count[0] == 11, "CEO (emp_id 1) should have 11 subordinates."

    cursor.execute("SELECT total_subordinates FROM hierarchy_metrics WHERE emp_id=2;")
    vp1_count = cursor.fetchone()
    assert vp1_count is not None and vp1_count[0] == 7, "VP1 (emp_id 2) should have 7 subordinates."

    cursor.execute("SELECT total_subordinates FROM hierarchy_metrics WHERE emp_id=12;")
    ic6_count = cursor.fetchone()
    assert ic6_count is not None and ic6_count[0] == 0, "IC6 (emp_id 12) should have 0 subordinates."

    conn.close()

def test_top_vp_log():
    assert os.path.isfile(LOG_PATH), f"Log file {LOG_PATH} does not exist."
    with open(LOG_PATH, "r") as f:
        content = f.read().strip()
    assert content == "2:7", f"Expected log file content '2:7', got '{content}'"

def test_script_uses_parameterized_query():
    with open(SCRIPT_PATH, "r") as f:
        content = f.read()
    # A simple check to ensure they are passing parameters to sqlite3, 
    # typically using `?` or `@` and passing the variable as an argument to sqlite3
    assert "?" in content or "@" in content or ":" in content or "$" in content, \
        "Script does not appear to use parameterized queries (could not find parameter markers like ?)."