# test_final_state.py

import os
import stat
import subprocess
import pytest

SCRIPT_PATH = "/home/user/analyze_graph.sh"
QUERY_PLAN_PATH = "/home/user/query_plan.txt"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable."

def test_script_output_engineering():
    try:
        result = subprocess.run([SCRIPT_PATH, "Engineering"], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script failed with error: {e.stderr}")

    output_lines = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
    expected_lines = ["Alice,Charlie,Sales", "Alice,Grace,HR"]

    assert sorted(output_lines) == sorted(expected_lines), \
        f"Expected output for 'Engineering' to be {expected_lines}, but got {output_lines}"

def test_script_output_sales():
    try:
        result = subprocess.run([SCRIPT_PATH, "Sales"], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script failed with error: {e.stderr}")

    output_lines = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
    expected_lines = ["Charlie,Diana,Marketing", "Frank,Grace,HR"]

    assert sorted(output_lines) == sorted(expected_lines), \
        f"Expected output for 'Sales' to be {expected_lines}, but got {output_lines}"

def test_query_plan_contains_index():
    assert os.path.isfile(QUERY_PLAN_PATH), f"Query plan file {QUERY_PLAN_PATH} does not exist."

    with open(QUERY_PLAN_PATH, "r") as f:
        content = f.read().upper()

    assert "INDEX" in content, f"The query plan in {QUERY_PLAN_PATH} does not demonstrate the use of an INDEX."