# test_final_state.py

import os
import json
import sqlite3
import random
import subprocess
import pytest

def create_fuzz_db(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("CREATE TABLE node_groups (node_id INTEGER PRIMARY KEY, group_id INTEGER)")
    cur.execute("CREATE TABLE links (target_id INTEGER, source_id INTEGER, weight REAL)")

    # Populate with random data
    for i in range(1, 1001):
        cur.execute("INSERT INTO node_groups (node_id, group_id) VALUES (?, ?)", (i, random.randint(1, 20)))

    for _ in range(5000):
        target = random.randint(1, 1000)
        source = random.randint(1, 1000)
        weight = random.uniform(0.1, 10.0)
        cur.execute("INSERT INTO links (target_id, source_id, weight) VALUES (?, ?, ?)", (target, source, weight))

    conn.commit()
    conn.close()

def oracle(db_path, node_ids):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    query = """
    WITH IntraGroupLinks AS (
        SELECT 
            l.target_id,
            l.source_id,
            l.weight,
            DENSE_RANK() OVER (PARTITION BY l.target_id ORDER BY l.weight DESC, l.source_id ASC) as rank
        FROM links l
        JOIN node_groups t_group ON l.target_id = t_group.node_id
        JOIN node_groups s_group ON l.source_id = s_group.node_id
        WHERE t_group.group_id = s_group.group_id AND l.target_id = ?
    )
    SELECT COALESCE(SUM(weight * rank), 0.0)
    FROM IntraGroupLinks;
    """
    results = []
    for nid in node_ids:
        cur.execute(query, (nid,))
        row = cur.fetchone()
        results.append(row[0] if row[0] is not None else 0.0)
    conn.close()
    return results

def test_graph_db_exists():
    """Check that the agent correctly created the graph.db file."""
    db_path = "/home/user/graph.db"
    assert os.path.exists(db_path), f"Agent did not create the database at {db_path}"

    # Verify it is a valid SQLite DB with the expected tables
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cur.fetchall()}
    conn.close()

    assert "node_groups" in tables, "Table 'node_groups' is missing from /home/user/graph.db"
    assert "links" in tables, "Table 'links' is missing from /home/user/graph.db"

def test_fuzz_equivalence(tmp_path):
    """Fuzz test the agent's script against the reference oracle."""
    agent_script = "/home/user/graph_analyzer.py"
    assert os.path.exists(agent_script), f"Agent script not found at {agent_script}"

    db_path = str(tmp_path / "fuzz.db")
    create_fuzz_db(db_path)

    random.seed(42)

    for i in range(50):
        length = random.randint(1, 50)
        node_ids = [random.randint(1, 1000) for _ in range(length)]

        expected = oracle(db_path, node_ids)
        input_json = json.dumps(node_ids)

        res = subprocess.run(
            ["python3", agent_script, db_path],
            input=input_json,
            text=True,
            capture_output=True
        )

        assert res.returncode == 0, f"Agent script failed with error:\n{res.stderr}"

        try:
            actual = json.loads(res.stdout)
        except json.JSONDecodeError:
            pytest.fail(f"Agent script output invalid JSON:\n{res.stdout}")

        assert isinstance(actual, list), "Agent script output is not a JSON array"
        assert len(actual) == len(expected), f"Output length mismatch. Expected {len(expected)}, got {len(actual)}"

        for a, e in zip(actual, expected):
            assert abs(a - e) < 1e-4, f"Mismatch on input {input_json}.\nExpected: {expected}\nGot: {actual}"