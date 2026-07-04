# test_final_state.py

import os
import csv
import sqlite3
import pytest
from collections import defaultdict, deque

DB_PATH = '/home/user/compliance.db'
VIOLATIONS_CSV_PATH = '/home/user/violations.csv'

def get_expected_violations():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Load edges
    cur.execute("SELECT source, target FROM network_edges")
    adj = defaultdict(list)
    for source, target in cur.fetchall():
        adj[source].append(target)

    # Load employees
    cur.execute("SELECT emp_id, assigned_node FROM employees")
    employees = cur.fetchall()

    # Compute reachable nodes (up to 2 hops)
    reachable = {}
    for emp_id, start_node in employees:
        visited = set()
        queue = deque([(start_node, 0)])
        while queue:
            node, dist = queue.popleft()
            if node not in visited:
                visited.add(node)
                if dist < 2:
                    for neighbor in adj.get(node, []):
                        queue.append((neighbor, dist + 1))
        reachable[emp_id] = visited

    # Check access logs
    cur.execute("SELECT emp_id, accessed_node FROM access_logs")
    logs = cur.fetchall()

    violations = set()
    for emp_id, accessed_node in logs:
        if emp_id in reachable:
            if accessed_node not in reachable[emp_id]:
                violations.add((emp_id, accessed_node))

    conn.close()

    return sorted(list(violations))

def test_violations_csv_exists():
    assert os.path.exists(VIOLATIONS_CSV_PATH), f"File {VIOLATIONS_CSV_PATH} was not created."
    assert os.path.isfile(VIOLATIONS_CSV_PATH), f"{VIOLATIONS_CSV_PATH} is not a file."

def test_violations_csv_content():
    expected_violations = get_expected_violations()

    with open(VIOLATIONS_CSV_PATH, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail("The violations.csv file is empty.")

        assert header == ['emp_id', 'accessed_node'], f"Incorrect CSV header. Expected ['emp_id', 'accessed_node'], got {header}."

        rows = list(reader)

    assert len(rows) == len(expected_violations), f"Expected {len(expected_violations)} violation rows, but got {len(rows)}."

    for i, (expected, actual) in enumerate(zip(expected_violations, rows)):
        assert list(expected) == actual, f"Row {i+1} mismatch. Expected {list(expected)}, got {actual}."