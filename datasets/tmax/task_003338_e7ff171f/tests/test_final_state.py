# test_final_state.py

import os
import json
import sqlite3
import pytest
from collections import defaultdict, deque

DB_PATH = "/home/user/financial_audit.db"
RESULT_PATH = "/home/user/audit_result.json"

def compute_truth():
    if not os.path.exists(DB_PATH):
        pytest.fail(f"Database missing at {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Get account names
    c.execute("SELECT id, name FROM accounts")
    accounts = {row['id']: row['name'] for row in c.fetchall()}

    # Get transfers
    c.execute("SELECT tx_id, sender_id, receiver_id, amount, timestamp FROM transfers ORDER BY sender_id, timestamp")
    transfers = c.fetchall()

    # Compute flagged transfers
    flagged_edges = []
    history = defaultdict(list)

    for tx in transfers:
        sender = tx['sender_id']
        receiver = tx['receiver_id']
        amount = tx['amount']

        # Add to history
        history[sender].append(amount)

        # Get up to 3 recent including current
        recent = history[sender][-3:]
        avg = sum(recent) / len(recent)

        if amount > avg:
            flagged_edges.append((accounts[sender], accounts[receiver]))

    # Build graph
    graph = defaultdict(list)
    out_degree = defaultdict(int)

    for u, v in flagged_edges:
        graph[u].append(v)
        out_degree[u] += 1
        if v not in out_degree:
            out_degree[v] = 0

    # Shortest path BFS
    start = "ShellCorp"
    end = "OffshoreVault"

    queue = deque([[start]])
    visited = set([start])
    shortest_path = None

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == end:
            shortest_path = path
            break

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    # Highest out-degree
    highest_out_degree = None
    if out_degree:
        max_deg = max(out_degree.values())
        candidates = [node for node, deg in out_degree.items() if deg == max_deg]
        highest_out_degree = sorted(candidates)[0]

    return {
        "shortest_path": shortest_path,
        "highest_out_degree": highest_out_degree
    }

def test_result_file_exists():
    assert os.path.exists(RESULT_PATH), f"Result file missing at {RESULT_PATH}"
    assert os.path.isfile(RESULT_PATH), f"{RESULT_PATH} is not a file"

def test_result_contents():
    assert os.path.exists(RESULT_PATH), "Result file missing"

    with open(RESULT_PATH, 'r') as f:
        try:
            result = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Result file is not valid JSON")

    truth = compute_truth()

    assert "shortest_path" in result, "Missing 'shortest_path' in result JSON"
    assert "highest_out_degree" in result, "Missing 'highest_out_degree' in result JSON"

    assert result["shortest_path"] == truth["shortest_path"], \
        f"Expected shortest_path {truth['shortest_path']}, got {result['shortest_path']}"

    assert result["highest_out_degree"] == truth["highest_out_degree"], \
        f"Expected highest_out_degree {truth['highest_out_degree']}, got {result['highest_out_degree']}"