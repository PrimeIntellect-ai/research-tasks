# test_final_state.py

import os
import sqlite3
import subprocess
import pytest

def test_impact_txt_content():
    impact_path = "/home/user/impact.txt"
    assert os.path.exists(impact_path), f"File {impact_path} does not exist."

    with open(impact_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = [
        "App-Backend-API",
        "App-Frontend-Web",
        "App-Reporting"
    ]

    assert lines == expected, f"Contents of {impact_path} do not match the expected sorted output."

def test_query_sql_unmodified():
    query_path = "/home/user/query.sql"
    assert os.path.exists(query_path), f"File {query_path} does not exist."

    expected_content = """WITH RECURSIVE impact AS (
    SELECT target_id FROM relations WHERE source_id = 42
    UNION
    SELECT r.target_id FROM relations r
    INNER JOIN impact i ON r.source_id = i.target_id
)
SELECT e.name FROM entities e
JOIN impact i ON e.id = i.target_id
WHERE e.type = 'Application';
"""
    with open(query_path, "r") as f:
        content = f.read()

    assert content.strip() == expected_content.strip(), f"File {query_path} was modified."

def test_database_indexes():
    db_path = "/home/user/graph.db"
    query_path = "/home/user/query.sql"

    assert os.path.exists(db_path), f"Database {db_path} does not exist."

    with open(query_path, "r") as f:
        query = f.read()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("EXPLAIN QUERY PLAN " + query)
        plan = cursor.fetchall()
    except sqlite3.Error as e:
        pytest.fail(f"Failed to execute EXPLAIN QUERY PLAN: {e}")
    finally:
        conn.close()

    for row in plan:
        detail = row[3]
        if "SCAN TABLE entities" in detail:
            pytest.fail(f"Query plan still contains full table scan on entities: {detail}")
        if "SCAN TABLE relations" in detail:
            pytest.fail(f"Query plan still contains full table scan on relations: {detail}")

def test_verify_plan_sh():
    script_path = "/home/user/verify_plan.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script {script_path} failed to execute."

    output = result.stdout.upper()
    assert "QUERY PLAN" in output or "SEARCH TABLE" in output or "SCAN TABLE" in output, \
        f"Script {script_path} does not seem to output a query plan."