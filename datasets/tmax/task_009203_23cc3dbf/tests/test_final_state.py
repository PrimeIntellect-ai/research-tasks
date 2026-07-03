# test_final_state.py
import os
import re
import pytest

CSV_PATH = "/home/user/unauthorized_access.csv"
PY_SCRIPT_PATH = "/home/user/audit_query.py"
SH_SCRIPT_PATH = "/home/user/generate_report.sh"

def test_csv_report_exists_and_correct():
    assert os.path.isfile(CSV_PATH), f"Report file missing at {CSV_PATH}"

    with open(CSV_PATH, "r") as f:
        content = f.read().strip().splitlines()

    assert len(content) == 4, f"Expected 4 lines in CSV (header + 3 rows), found {len(content)}"

    expected_lines = [
        "ID,Name",
        "101,Alice_Admin",
        "102,Bob_Manager",
        "103,Charlie_Staff"
    ]

    for i, expected in enumerate(expected_lines):
        assert content[i].strip() == expected, f"Line {i+1} mismatch. Expected '{expected}', got '{content[i].strip()}'"

def test_python_script_exists_and_parameterized():
    assert os.path.isfile(PY_SCRIPT_PATH), f"Python script missing at {PY_SCRIPT_PATH}"

    with open(PY_SCRIPT_PATH, "r") as f:
        code = f.read()

    # Check for execute method calls
    assert "execute" in code, "The Python script does not seem to execute any SQL queries."

    # Check for parameterization markers (e.g., ?, :param, %s)
    has_param_marker = re.search(r'\?|:\w+|%\w+', code)
    assert has_param_marker, "The Python script does not appear to use SQL parameterization (no ?, :name, or %s found)."

    # Ensure sys.argv is used
    assert "sys.argv" in code or "argparse" in code, "The Python script must take the resource name as a command-line argument."

def test_bash_script_exists():
    assert os.path.isfile(SH_SCRIPT_PATH), f"Bash script missing at {SH_SCRIPT_PATH}"

    with open(SH_SCRIPT_PATH, "r") as f:
        code = f.read()

    assert "audit_query.py" in code, "The bash script does not seem to call the Python script."
    assert "CONFIDENTIAL_FINANCE_RECORDS" in code, "The bash script does not pass the correct resource name parameter."