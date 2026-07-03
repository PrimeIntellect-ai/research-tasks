# test_final_state.py

import os
import json
import sqlite3
import pytest

DB_PATH = "/home/user/graph_data.db"
RESULTS_PATH = "/home/user/motif_results.json"

def get_expected_motifs():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    query = """
        SELECT r1.src, r1.dst, r2.dst
        FROM relations r1
        JOIN relations r2 ON r1.dst = r2.src
        JOIN relations r3 ON r1.src = r3.src AND r2.dst = r3.dst
        JOIN nodes n1 ON r1.src = n1.id
        JOIN nodes n2 ON r1.dst = n2.id
        JOIN nodes n3 ON r2.dst = n3.id
        WHERE n1.property = 'target' 
          AND n2.property = 'target' 
          AND n3.property = 'target'
    """
    c.execute(query)
    results = c.fetchall()
    conn.close()

    # Sort lexicographically by A_id, B_id, C_id
    sorted_results = sorted([list(row) for row in results])
    return sorted_results

def test_indexes_created():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} does not exist."
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index';")
    indexes = c.fetchall()
    conn.close()

    # Check if there are indexes created by the user (excluding auto-generated ones if any)
    user_indexes = [idx for idx in indexes if not idx[0].startswith('sqlite_autoindex')]
    assert len(user_indexes) > 0, "No indexes were created on the database."

    tables_with_indexes = {idx[1] for idx in user_indexes}
    assert "nodes" in tables_with_indexes or "relations" in tables_with_indexes, "Indexes must be created on 'nodes' or 'relations' tables."

def test_motif_results():
    assert os.path.exists(RESULTS_PATH), f"Results file {RESULTS_PATH} does not exist."

    with open(RESULTS_PATH, 'r') as f:
        try:
            student_results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {RESULTS_PATH} is not valid JSON.")

    expected_results = get_expected_motifs()

    assert isinstance(student_results, list), "Output must be a JSON array."
    assert student_results == expected_results, f"Expected motifs {expected_results}, but got {student_results}."