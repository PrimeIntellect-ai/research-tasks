# test_final_state.py
import os
import sqlite3
import re
import pytest

GRAPH_IMPORT_PATH = "/home/user/graph_import.cypher"
INDEX_STRATEGY_PATH = "/home/user/index_strategy.cypher"
DB_PATH = "/home/user/company.db"

def get_expected_hierarchy():
    if not os.path.exists(DB_PATH):
        pytest.fail(f"Database {DB_PATH} missing.")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        WITH RECURSIVE hierarchy AS (
            SELECT emp_id, name, manager_id, 0 as level
            FROM employees WHERE manager_id IS NULL
            UNION ALL
            SELECT e.emp_id, e.name, e.manager_id, h.level + 1
            FROM employees e
            JOIN hierarchy h ON e.manager_id = h.emp_id
        )
        SELECT emp_id, name, manager_id, level FROM hierarchy
    """)
    rows = c.fetchall()
    conn.close()
    return rows

def test_graph_import_exists_and_ordered():
    assert os.path.exists(GRAPH_IMPORT_PATH), f"{GRAPH_IMPORT_PATH} was not created."

    with open(GRAPH_IMPORT_PATH, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) > 0, f"{GRAPH_IMPORT_PATH} is empty."

    seen_rel = False
    for i, line in enumerate(lines):
        if "MANAGES" in line or "MATCH" in line:
            seen_rel = True
        else:
            if seen_rel:
                pytest.fail(f"Line {i+1} ('{line}') appears to be a node creation, but occurs after a relationship creation.")

def test_graph_import_nodes():
    expected_data = get_expected_hierarchy()

    with open(GRAPH_IMPORT_PATH, "r") as f:
        content = f.read()

    for emp_id, name, manager_id, level in expected_data:
        # Look for a line that creates this employee
        # E.g., CREATE (:Employee {emp_id: "E1", name: "Alice (CEO)", level: 0});
        # We'll use a regex to be flexible with spacing and property order
        pattern = rf"CREATE\s*\(\s*:\s*Employee\s*{{[^}}]*emp_id\s*:\s*['\"]{emp_id}['\"][^}}]*}}\s*\)"
        match = re.search(pattern, content)
        assert match is not None, f"Could not find node creation for emp_id '{emp_id}' in {GRAPH_IMPORT_PATH}"

        # Verify name and level are also in that matched creation or the general line
        # To be robust, let's find the exact line containing the emp_id creation
        lines_with_emp = [line for line in content.split('\n') if re.search(pattern, line)]
        assert len(lines_with_emp) == 1, f"Expected exactly one node creation line for '{emp_id}'"
        line = lines_with_emp[0]

        assert re.search(rf"name\s*:\s*['\"]{re.escape(name)}['\"]", line), f"Node creation for '{emp_id}' missing correct name '{name}'"
        assert re.search(rf"level\s*:\s*{level}\b", line), f"Node creation for '{emp_id}' missing correct level {level}"

def test_graph_import_relationships():
    expected_data = get_expected_hierarchy()

    with open(GRAPH_IMPORT_PATH, "r") as f:
        content = f.read()

    for emp_id, name, manager_id, level in expected_data:
        if manager_id is None:
            continue

        # Look for relationship: manager -> employee
        # E.g., MATCH (m:Employee {emp_id: "E1"}), (e:Employee {emp_id: "E2"}) CREATE (m)-[:MANAGES]->(e);
        # We will check that both emp_id and manager_id are in the same MATCH statement and MANAGES is created

        # A simple robust check: find a line that has both manager_id and emp_id and MANAGES
        lines = [line for line in content.split('\n') if "MANAGES" in line and manager_id in line and emp_id in line]
        assert len(lines) >= 1, f"Could not find relationship creation from manager '{manager_id}' to employee '{emp_id}'"

def test_index_strategy_cypher():
    assert os.path.exists(INDEX_STRATEGY_PATH), f"{INDEX_STRATEGY_PATH} was not created."

    with open(INDEX_STRATEGY_PATH, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"{INDEX_STRATEGY_PATH} must contain exactly two commands (one per line)."

    content = " ".join(lines).upper()

    # Check for unique constraint on emp_id
    assert "CONSTRAINT" in content, "Missing CONSTRAINT keyword in index strategy."
    assert "UNIQUE" in content, "Missing UNIQUE keyword in index strategy."
    assert "EMP_ID" in content, "Missing emp_id property in index strategy."

    # Check for index on level
    assert "INDEX" in content, "Missing INDEX keyword in index strategy."
    assert "LEVEL" in content, "Missing level property in index strategy."
    assert "EMPLOYEE" in content, "Missing Employee label in index strategy."