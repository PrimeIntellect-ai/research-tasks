# test_final_state.py
import json
import os
import sqlite3
import pytest
from collections import deque

REPORT_PATH = '/home/user/audit_report.json'
DB_PATH = '/home/user/financial_audit.db'

def get_db_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT account_id, account_type, risk_score FROM accounts")
    accounts = c.fetchall()

    c.execute("SELECT source_account, target_account FROM transactions")
    edges = c.fetchall()

    conn.close()
    return accounts, edges

def compute_pagerank(nodes, edges, d=0.85, tol=1e-6, max_iter=100):
    N = len(nodes)
    if N == 0:
        return {}

    out_degree = {n: 0 for n in nodes}
    for u, v in edges:
        out_degree[u] += 1

    pr = {n: 1.0 / N for n in nodes}

    for _ in range(max_iter):
        prev_pr = pr.copy()
        dangling_mass = sum(prev_pr[n] for n in nodes if out_degree[n] == 0)

        for n in nodes:
            pr[n] = (1 - d) / N + d * dangling_mass / N

        for u, v in edges:
            pr[v] += d * prev_pr[u] / out_degree[u]

        err = sum(abs(pr[n] - prev_pr[n]) for n in nodes)
        if err < N * tol:
            break

    return pr

def find_shortest_path(nodes, edges, high_risk, offshore):
    adj = {n: [] for n in nodes}
    for u, v in edges:
        adj[u].append(v)

    best_paths = []
    min_length = float('inf')

    for start in sorted(high_risk):
        queue = deque([[start]])
        visited = {start: 1}

        while queue:
            path = queue.popleft()
            curr = path[-1]

            if len(path) > min_length:
                continue

            if curr in offshore:
                if len(path) < min_length:
                    min_length = len(path)
                    best_paths = [path]
                elif len(path) == min_length:
                    best_paths.append(path)
                continue

            for neighbor in adj[curr]:
                if neighbor not in visited or visited[neighbor] >= len(path) + 1:
                    visited[neighbor] = len(path) + 1
                    queue.append(path + [neighbor])

    if not best_paths:
        return []

    # Sort by starting account_id alphabetically to break ties
    best_paths.sort(key=lambda p: p[0])
    return best_paths[0]

def test_report_exists_and_valid_json():
    assert os.path.isfile(REPORT_PATH), f"Report file missing at {REPORT_PATH}"
    with open(REPORT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} is not valid JSON")

    assert "top_3_pagerank_accounts" in data, "Missing 'top_3_pagerank_accounts' in JSON"
    assert "shortest_illicit_path" in data, "Missing 'shortest_illicit_path' in JSON"

def test_report_values():
    accounts, edges = get_db_data()

    nodes = [acc[0] for acc in accounts]
    high_risk = [acc[0] for acc in accounts if acc[2] > 80]
    offshore = [acc[0] for acc in accounts if acc[1] == 'offshore']

    # Compute expected PageRank
    pr = compute_pagerank(nodes, edges)
    # Sort by PageRank descending, then alphabetically
    sorted_pr = sorted(pr.items(), key=lambda x: (-x[1], x[0]))
    expected_top_3 = [x[0] for x in sorted_pr[:3]]

    # Compute expected shortest path
    expected_path = find_shortest_path(nodes, edges, high_risk, offshore)

    with open(REPORT_PATH, 'r') as f:
        data = json.load(f)

    assert data["top_3_pagerank_accounts"] == expected_top_3, \
        f"Expected top 3 PageRank accounts {expected_top_3}, but got {data.get('top_3_pagerank_accounts')}"

    assert data["shortest_illicit_path"] == expected_path, \
        f"Expected shortest path {expected_path}, but got {data.get('shortest_illicit_path')}"