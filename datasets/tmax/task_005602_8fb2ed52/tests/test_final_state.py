# test_final_state.py

import os
import json
import sqlite3
import subprocess
import pytest

DB_PATH = "/home/user/legacy_etl.db"
BUILD_INDEXES_SCRIPT = "/home/user/build_indexes.sh"
GET_UPSTREAM_SCRIPT = "/home/user/get_upstream.sh"
SALES_LINEAGE_JSON = "/home/user/sales_lineage.json"

def test_build_indexes_script_exists():
    assert os.path.isfile(BUILD_INDEXES_SCRIPT), f"{BUILD_INDEXES_SCRIPT} does not exist."
    assert os.access(BUILD_INDEXES_SCRIPT, os.X_OK), f"{BUILD_INDEXES_SCRIPT} is not executable."

def test_indexes_created():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='index' AND tbl_name='job_deps';")
    index_count = cursor.fetchone()[0]
    conn.close()
    assert index_count > 0, "No index was created on the 'job_deps' table."

def test_get_upstream_script_exists():
    assert os.path.isfile(GET_UPSTREAM_SCRIPT), f"{GET_UPSTREAM_SCRIPT} does not exist."
    assert os.access(GET_UPSTREAM_SCRIPT, os.X_OK), f"{GET_UPSTREAM_SCRIPT} is not executable."

def test_sales_lineage_json_correct():
    assert os.path.isfile(SALES_LINEAGE_JSON), f"{SALES_LINEAGE_JSON} does not exist."

    with open(SALES_LINEAGE_JSON, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{SALES_LINEAGE_JSON} does not contain valid JSON.")

    expected = [
        "Calculate_Metrics",
        "Clean_Marketing_Data",
        "Clean_Sales_Data",
        "Extract_Marketing_API",
        "Extract_Sales_DB",
        "Join_Sales_Marketing"
    ]

    assert isinstance(data, list), "Output JSON must be an array."
    assert sorted(data) == sorted(expected), f"Lineage data in {SALES_LINEAGE_JSON} does not match expected upstream jobs."

def test_get_upstream_script_execution():
    # Test the script with another job to ensure it works dynamically
    target_job = "Join_Sales_Marketing"
    expected_output = [
        "Clean_Marketing_Data",
        "Clean_Sales_Data",
        "Extract_Marketing_API",
        "Extract_Sales_DB"
    ]

    result = subprocess.run([GET_UPSTREAM_SCRIPT, target_job], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail("Script output is not valid JSON.")

    assert isinstance(data, list), "Script output must be a JSON array."
    assert sorted(data) == sorted(expected_output), f"Script output for {target_job} did not match expected upstream jobs."