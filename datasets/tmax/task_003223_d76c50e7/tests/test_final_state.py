# test_final_state.py

import os
import subprocess
import pytest

FIXED_CSV_PATH = "/home/user/data/query_logs_fixed.csv"
BAD_QUERIES_LOG_PATH = "/home/user/bad_queries.log"
SCRIPT_PATH = "/home/user/scripts/build_report.py"

def test_fixed_csv_exists():
    assert os.path.isfile(FIXED_CSV_PATH), f"The fixed CSV file is missing at {FIXED_CSV_PATH}"

def test_fixed_csv_contents():
    with open(FIXED_CSV_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    assert len(lines) == 99, f"Expected 99 lines in fixed CSV, found {len(lines)}"

    content = "".join(lines)
    assert "QueryID,Timestamp,UserID,QueryText,ExecutionTime" in lines[0], "Missing or incorrect CSV header in the fixed file"
    assert "Q0042" not in content, "Row Q0042 (corrupted) should be removed from the fixed CSV"
    assert "Q0076" not in content, "Row Q0076 (corrupted) should be removed from the fixed CSV"
    assert "\x00" not in content, "Null bytes should not be present in the fixed CSV"
    assert "NULL_VAL" not in content, "NULL_VAL should not be present in the fixed CSV"

def test_bad_queries_log_exists():
    assert os.path.isfile(BAD_QUERIES_LOG_PATH), f"The bad queries log is missing at {BAD_QUERIES_LOG_PATH}"

def test_bad_queries_log_contents():
    with open(BAD_QUERIES_LOG_PATH, 'r', encoding='utf-8') as f:
        content = f.read().strip().splitlines()

    expected = ["Q0042", "Q0076"]
    assert content == expected, f"Expected bad queries log to contain {expected}, but found {content}"

def test_build_script_succeeds_with_fixed_csv():
    assert os.path.isfile(SCRIPT_PATH), "Build script is missing"

    result = subprocess.run(
        ["python3", SCRIPT_PATH, FIXED_CSV_PATH],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    assert result.returncode == 0, f"Build script failed on fixed CSV. Stderr: {result.stderr}"
    assert "Build successful:" in result.stdout, "Build script did not output success message"