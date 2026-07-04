# test_final_state.py

import os
import stat
import subprocess
import pytest

SCRIPT_PATH = "/home/user/get_total_size.sh"
QUERY_PLAN_PATH = "/home/user/query_plan.txt"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script missing at {SCRIPT_PATH}"
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script at {SCRIPT_PATH} is not executable"

def test_script_output_target_dir():
    result = subprocess.run([SCRIPT_PATH, "target_dir"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"
    output = result.stdout.strip()
    assert output == "600", f"Expected output '600' for target_dir, got '{output}'"

def test_script_output_other_dir():
    result = subprocess.run([SCRIPT_PATH, "other_dir"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"
    output = result.stdout.strip()
    assert output == "400", f"Expected output '400' for other_dir, got '{output}'"

def test_script_contents():
    with open(SCRIPT_PATH, "r") as f:
        content = f.read().upper()
    assert "REINDEX" in content, "Script does not contain REINDEX command"
    assert "WITH" in content, "Script does not seem to use a CTE (WITH)"
    assert "SQLITE3" in content, "Script does not seem to invoke sqlite3"

def test_query_plan_exists_and_valid():
    assert os.path.exists(QUERY_PLAN_PATH), f"Query plan missing at {QUERY_PLAN_PATH}"
    with open(QUERY_PLAN_PATH, "r") as f:
        content = f.read().upper()
    assert "SCAN" in content, "query_plan.txt does not appear to contain EXPLAIN QUERY PLAN output"
    assert len(content.strip()) > 0, "query_plan.txt is empty"