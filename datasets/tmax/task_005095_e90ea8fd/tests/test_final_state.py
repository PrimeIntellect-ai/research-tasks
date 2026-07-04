# test_final_state.py

import os
import stat
import subprocess
import sqlite3
import pytest

SCRIPT_PATH = "/home/user/process_graph.sh"
DB_PATH = "/home/user/graph.db"
TOP_PATHS_CSV = "/home/user/top_paths.csv"
QUERY_PLAN_TXT = "/home/user/query_plan.txt"

@pytest.fixture(scope="session", autouse=True)
def run_script():
    """Ensure the script exists, is executable, and runs successfully."""
    assert os.path.isfile(SCRIPT_PATH), f"Script not found: {SCRIPT_PATH}"

    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script is not executable: {SCRIPT_PATH}"

    # Remove output files to ensure the script generates them
    for path in [DB_PATH, TOP_PATHS_CSV, QUERY_PLAN_TXT]:
        if os.path.exists(path):
            os.remove(path)

    result = subprocess.run([SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Script execution failed with error:\n{result.stderr}"

def test_database_and_tables():
    """Test that the database is created and contains the required tables and data."""
    assert os.path.isfile(DB_PATH), f"Database not created at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {row[0] for row in cursor.fetchall()}
    assert "nodes" in tables, "Table 'nodes' is missing in the database."
    assert "edges" in tables, "Table 'edges' is missing in the database."

    # Check data import
    cursor.execute("SELECT COUNT(*) FROM nodes;")
    assert cursor.fetchone()[0] == 6, "Incorrect number of rows in 'nodes' table."

    cursor.execute("SELECT COUNT(*) FROM edges;")
    assert cursor.fetchone()[0] == 8, "Incorrect number of rows in 'edges' table."

    # Check indexes
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='edges';")
    indexes = cursor.fetchall()
    assert len(indexes) > 0, "No indexes found on the 'edges' table."

    conn.close()

def test_top_paths_output():
    """Test that the top_paths.csv contains the correct data."""
    assert os.path.isfile(TOP_PATHS_CSV), f"Output file not found: {TOP_PATHS_CSV}"

    with open(TOP_PATHS_CSV, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = {
        "Alice,Diana,Eve,650",
        "Diana,Eve,Frank,1100"
    }

    actual_lines = set(lines)
    assert actual_lines == expected_lines, f"Incorrect output in {TOP_PATHS_CSV}. Expected {expected_lines}, got {actual_lines}"

def test_query_plan_output():
    """Test that the query_plan.txt contains EXPLAIN QUERY PLAN output."""
    assert os.path.isfile(QUERY_PLAN_TXT), f"Output file not found: {QUERY_PLAN_TXT}"

    with open(QUERY_PLAN_TXT, "r") as f:
        content = f.read().upper()

    assert "SCAN" in content or "SEARCH" in content, f"Query plan output does not look like EXPLAIN QUERY PLAN results. Content:\n{content}"