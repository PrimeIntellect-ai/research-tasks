# test_final_state.py
import os
import stat
import sqlite3
import subprocess
import pytest

DB_PATH = "/home/user/routes.db"
OPTIMIZE_SQL_PATH = "/home/user/optimize.sql"
SCRIPT_PATH = "/home/user/get_reachable.sh"

def test_optimize_sql_exists():
    """Test that optimize.sql exists."""
    assert os.path.isfile(OPTIMIZE_SQL_PATH), f"File missing: {OPTIMIZE_SQL_PATH}"

def test_index_applied():
    """Test that an index was created on the edges table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA index_list('edges');")
    indices = cursor.fetchall()
    conn.close()
    assert len(indices) >= 1, "No index found on the 'edges' table."

def test_query_plan_optimized():
    """Test that the recursive query uses an index instead of a full table scan."""
    query = """
    EXPLAIN QUERY PLAN
    WITH RECURSIVE paths(node, total_cost) AS (
        SELECT 'A', 0
        UNION ALL
        SELECT e.target, p.total_cost + e.cost
        FROM paths p
        JOIN edges e ON p.node = e.source
        WHERE p.total_cost + e.cost <= 50
    )
    SELECT node, MIN(total_cost) as min_cost 
    FROM paths 
    GROUP BY node 
    ORDER BY node;
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    plan = cursor.fetchall()
    conn.close()

    plan_text = " ".join([row[-1] for row in plan]).upper()

    # It should not do a full table scan on edges
    assert "SCAN TABLE EDGES" not in plan_text and "SCAN EDGES" not in plan_text, \
        "The query plan still shows a full table scan on the 'edges' table."

    # It should use an index
    assert "SEARCH TABLE EDGES USING" in plan_text or "SEARCH EDGES USING" in plan_text, \
        "The query plan does not show an index search on the 'edges' table."

def test_script_exists_and_executable():
    """Test that the bash script exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"Script missing: {SCRIPT_PATH}"
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script is not executable: {SCRIPT_PATH}"

def test_script_output_A():
    """Test the bash script output for starting node A."""
    result = subprocess.run([SCRIPT_PATH, "A"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}"

    expected_output = "A:0\nB:10\nC:20\nD:25\n"
    assert result.stdout.strip() == expected_output.strip(), \
        f"Incorrect output for starting node 'A'.\nExpected:\n{expected_output.strip()}\nGot:\n{result.stdout.strip()}"

def test_script_output_C():
    """Test the bash script output for starting node C."""
    result = subprocess.run([SCRIPT_PATH, "C"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}"

    expected_output = "C:0\nD:5\nE:35\nF:45\n"
    assert result.stdout.strip() == expected_output.strip(), \
        f"Incorrect output for starting node 'C'.\nExpected:\n{expected_output.strip()}\nGot:\n{result.stdout.strip()}"