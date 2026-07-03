# test_final_state.py
import os
import json
import sqlite3
import pytest
from collections import defaultdict, deque

DB_PATH = '/home/user/company.db'
REPORT_PATH = '/home/user/analyzer/report.json'

@pytest.fixture
def db_connection():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} does not exist."
    conn = sqlite3.connect(DB_PATH)
    yield conn
    conn.close()

@pytest.fixture
def expected_results(db_connection):
    c = db_connection.cursor()

    # 1. Cross-Department Traffic
    # We want unique pairs of differing departments.
    # The prompt says "between every unique pair of departments" and format is "DeptA-DeptB" alphabetically.
    c.execute('''
        SELECT d1.name, d2.name, c.bytes
        FROM communications c
        JOIN employees e1 ON c.sender_id = e1.id
        JOIN employees e2 ON c.receiver_id = e2.id
        JOIN departments d1 ON e1.department_id = d1.id
        JOIN departments d2 ON e2.department_id = d2.id
    ''')

    cross_dept_traffic = defaultdict(int)
    for d1, d2, bytes_transferred in c.fetchall():
        if d1 != d2:
            dept_pair = f"{min(d1, d2)}-{max(d1, d2)}"
            cross_dept_traffic[dept_pair] += bytes_transferred

    # 2. Graph Construction & Centrality
    c.execute('SELECT sender_id, receiver_id FROM communications')
    edges = c.fetchall()

    graph = defaultdict(set)
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)

    centrality = []
    for node, neighbors in graph.items():
        centrality.append((len(neighbors), -node, node))  # -node for ascending order on tie

    # Sort by degree desc, then node asc
    centrality.sort(key=lambda x: (x[0], x[1]), reverse=True)
    top_central_employees = [node for _, _, node in centrality[:3]]

    # 3. Shortest Path from 1 to 7
    start_node = 1
    target_node = 7

    queue = deque([[start_node]])
    visited = {start_node}
    shortest_path = []

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == target_node:
            shortest_path = path
            break

        # To ensure deterministic shortest path if there are multiple, we could sort neighbors
        for neighbor in sorted(graph[node]):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    return {
        "cross_dept_traffic": dict(cross_dept_traffic),
        "top_central_employees": top_central_employees,
        "shortest_path_1_to_7": shortest_path
    }

def test_report_exists():
    assert os.path.exists(REPORT_PATH), f"Report file {REPORT_PATH} is missing."
    assert os.path.isfile(REPORT_PATH), f"{REPORT_PATH} is not a file."

def test_report_contents(expected_results):
    assert os.path.exists(REPORT_PATH), f"Report file {REPORT_PATH} is missing."

    try:
        with open(REPORT_PATH, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {REPORT_PATH} does not contain valid JSON.")

    assert "cross_dept_traffic" in data, "Missing 'cross_dept_traffic' in report."
    assert "top_central_employees" in data, "Missing 'top_central_employees' in report."
    assert "shortest_path_1_to_7" in data, "Missing 'shortest_path_1_to_7' in report."

    # Check cross_dept_traffic
    expected_traffic = expected_results["cross_dept_traffic"]
    for pair, bytes_count in expected_traffic.items():
        assert pair in data["cross_dept_traffic"], f"Missing department pair {pair} in cross_dept_traffic."
        assert data["cross_dept_traffic"][pair] == bytes_count, f"Expected {bytes_count} bytes for {pair}, got {data['cross_dept_traffic'][pair]}."

    # Check top_central_employees
    assert data["top_central_employees"] == expected_results["top_central_employees"], \
        f"Expected top central employees {expected_results['top_central_employees']}, got {data['top_central_employees']}."

    # Check shortest_path_1_to_7
    assert data["shortest_path_1_to_7"] == expected_results["shortest_path_1_to_7"], \
        f"Expected shortest path {expected_results['shortest_path_1_to_7']}, got {data['shortest_path_1_to_7']}."