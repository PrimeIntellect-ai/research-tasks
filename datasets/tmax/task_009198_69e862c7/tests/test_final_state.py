# test_final_state.py

import os
import sqlite3
import json
import pytest

DB_PATH = "/home/user/locks.db"
TTL_PATH = "/home/user/wait_for.ttl"
JSON_PATH = "/home/user/deadlocks.json"

def get_expected_deadlocks():
    """Derive the expected deadlocks directly from the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Recompute the wait-for edges
    # TxA waits for TxB
    c.execute("""
        SELECT a.tx_id, b.tx_id
        FROM lock_requests a
        JOIN lock_requests b ON a.resource_id = b.resource_id
        WHERE b.grant_time IS NOT NULL
          AND a.request_time > b.grant_time
          AND (b.release_time IS NULL OR a.request_time < b.release_time)
          AND a.tx_id != b.tx_id
    """)
    edges = c.fetchall()
    conn.close()

    # Keep only the most recent granted transaction before request
    # Since we are doing a simplified derivation, we can just build a graph from the valid edges
    # For the given data, all valid overlapping requests are the most recent.

    graph = {}
    for a, b in edges:
        if a not in graph:
            graph[a] = []
        graph[a].append(b)

    # Find cycles of length 2 and 3
    cycles = []
    for node in graph:
        # Length 2
        for neighbor in graph.get(node, []):
            if node in graph.get(neighbor, []):
                cycle = sorted([node, neighbor])
                if cycle not in cycles:
                    cycles.append(cycle)
            # Length 3
            for neighbor_of_neighbor in graph.get(neighbor, []):
                if node in graph.get(neighbor_of_neighbor, []):
                    cycle = sorted([node, neighbor, neighbor_of_neighbor])
                    if cycle not in cycles:
                        cycles.append(cycle)

    # Format according to rules
    cycles.sort(key=lambda x: x[0])
    return cycles

def test_wait_for_ttl_exists():
    assert os.path.isfile(TTL_PATH), f"RDF file missing at {TTL_PATH}"
    with open(TTL_PATH, 'r') as f:
        content = f.read()
    assert "waitsFor" in content, "The predicate 'waitsFor' was not found in the Turtle file."

def test_deadlocks_json():
    assert os.path.isfile(JSON_PATH), f"JSON file missing at {JSON_PATH}"

    with open(JSON_PATH, 'r') as f:
        try:
            student_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {JSON_PATH} is not valid JSON.")

    expected_data = get_expected_deadlocks()

    assert isinstance(student_data, list), "JSON root should be a list."

    # Normalize student data
    normalized_student = []
    for cycle in student_data:
        assert isinstance(cycle, list), "Each cycle should be a list of strings."
        normalized_student.append(sorted(cycle))

    normalized_student.sort(key=lambda x: x[0] if x else "")

    assert normalized_student == expected_data, f"Expected deadlocks {expected_data}, but got {normalized_student}"