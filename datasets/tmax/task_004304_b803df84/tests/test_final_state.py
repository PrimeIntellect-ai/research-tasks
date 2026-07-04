# test_final_state.py

import os
import stat
import pytest

SCRIPT_PATH = "/home/user/audit_trace.sh"
RESULT_PATH = "/home/user/audit_result.csv"

EXPECTED_CSV_CONTENT = """id,user_id,doc_id,timestamp,user_seq
1,alice,doc_A,2023-10-01 10:00:00,1
2,bob,doc_A,2023-10-01 10:05:00,1
4,alice,doc_A,2023-10-01 10:15:00,2
5,dave,doc_A,2023-10-01 10:20:00,1
6,bob,doc_A,2023-10-01 10:25:00,2
7,alice,doc_A,2023-10-01 10:30:00,3"""

def test_script_exists_and_executable():
    """Test that the bash script exists and is executable."""
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"

    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script at {SCRIPT_PATH} is not executable"

def test_script_contains_reindex():
    """Test that the script contains the REINDEX command."""
    with open(SCRIPT_PATH, 'r') as f:
        content = f.read()
    assert "REINDEX" in content.upper(), "The script does not contain the required REINDEX command."

def test_result_csv_exists():
    """Test that the output CSV file exists."""
    assert os.path.exists(RESULT_PATH), f"Result file not found at {RESULT_PATH}"
    assert os.path.isfile(RESULT_PATH), f"{RESULT_PATH} is not a file"

def test_result_csv_content():
    """Test that the output CSV file contains the correct data."""
    with open(RESULT_PATH, 'r') as f:
        content = f.read().strip()

    # Normalize line endings
    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in EXPECTED_CSV_CONTENT.splitlines() if line.strip()]

    assert actual_lines == expected_lines, "The content of the CSV file does not match the expected output."