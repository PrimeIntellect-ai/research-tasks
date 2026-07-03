# test_final_state.py
import os
import sys
import json
import subprocess
import re
import pytest

SCRIPT_PATH = "/home/user/analyze_deadlocks.py"
REPORT_PATH = "/home/user/deadlock_report.json"

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Script missing at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"

def test_script_uses_parameterized_query():
    with open(SCRIPT_PATH, 'r') as f:
        content = f.read()

    # Verify that the script uses parameterized queries (e.g., uses ? or named parameters)
    # and passes them to an execute method.
    assert '?' in content or re.search(r':\w+', content), "Script does not appear to use parameterized queries ('?' or named parameters)."
    assert '.execute' in content, "Script does not call .execute() on a cursor."

def test_script_execution_and_output():
    if os.path.exists(REPORT_PATH):
        os.remove(REPORT_PATH)

    cmd = [
        sys.executable, SCRIPT_PATH,
        "--start-tx", "T1",
        "--min-total-wait", "500",
        "--limit", "2",
        "--offset", "1"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. stderr: {result.stderr}"

    assert os.path.exists(REPORT_PATH), f"Report file missing at {REPORT_PATH}. The script must generate this file."

    with open(REPORT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Report file is not valid JSON")

    expected_data = [
        {
            "path": ["T1", "T4", "T5", "T1"],
            "total_wait": 700
        },
        {
            "path": ["T1", "T2", "T3", "T1"],
            "total_wait": 600
        }
    ]

    assert data == expected_data, f"JSON output does not match expected results.\nExpected: {expected_data}\nGot: {data}"