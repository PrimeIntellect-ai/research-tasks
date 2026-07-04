# test_final_state.py

import os
import json
import csv
import sqlite3
import pytest

def compute_pagerank(nodes, edges, alpha=0.85, max_iter=100, tol=1.0e-6):
    """Compute PageRank in pure Python to match networkx default behavior."""
    N = len(nodes)
    if N == 0:
        return {}

    pr = {n: 1.0 / N for n in nodes}
    out_degree = {n: 0 for n in nodes}
    for u, v in edges:
        out_degree[u] += 1

    for _ in range(max_iter):
        new_pr = {n: (1.0 - alpha) / N for n in nodes}
        dangling_sum = sum(pr[n] for n in nodes if out_degree[n] == 0)

        for n in nodes:
            new_pr[n] += alpha * dangling_sum / N

        for u, v in edges:
            new_pr[v] += alpha * pr[u] / out_degree[u]

        err = sum(abs(new_pr[n] - pr[n]) for n in nodes)
        pr = new_pr
        if err < tol:
            break

    return pr

@pytest.fixture
def expected_data():
    jsonl_path = "/home/user/dataset/papers.jsonl"
    assert os.path.exists(jsonl_path), f"Input file {jsonl_path} is missing."

    nodes = []
    edges = []
    ml_papers = {}

    with open(jsonl_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)
            pid = data['id']
            nodes.append(pid)
            if "machine_learning" in data.get("keywords", []):
                ml_papers[pid] = data['title']
            for cited in data.get("citations", []):
                edges.append((pid, cited))

    pr = compute_pagerank(nodes, edges)

    ml_pr = [(pid, ml_papers[pid], pr[pid]) for pid in ml_papers]
    # Sort by PageRank descending, then ID ascending
    ml_pr.sort(key=lambda x: (-x[2], x[0]))

    top_3 = ml_pr[:3]
    return top_3

def test_database_exists():
    db_path = "/home/user/research.db"
    assert os.path.exists(db_path), f"Database file {db_path} was not created."

    # Try to connect to ensure it's a valid SQLite DB
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        assert len(tables) > 0, "Database exists but contains no tables."
    except sqlite3.Error as e:
        pytest.fail(f"Failed to read SQLite database at {db_path}: {e}")

def test_csv_output(expected_data):
    csv_path = "/home/user/influential_ml_papers.csv"
    assert os.path.exists(csv_path), f"Output file {csv_path} was not created."

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "CSV file is empty."

    header = rows[0]
    assert header == ['id', 'title', 'pagerank'], f"Incorrect CSV header. Expected ['id', 'title', 'pagerank'], got {header}"

    data_rows = rows[1:]
    assert len(data_rows) == 3, f"Expected exactly 3 data rows in CSV, got {len(data_rows)}."

    for i, (expected_id, expected_title, expected_pr) in enumerate(expected_data):
        actual_id, actual_title, actual_pr_str = data_rows[i]

        assert actual_id == expected_id, f"Row {i+1}: Expected id '{expected_id}', got '{actual_id}'"
        assert actual_title == expected_title, f"Row {i+1}: Expected title '{expected_title}', got '{actual_title}'"

        expected_pr_rounded = f"{expected_pr:.4f}"
        assert actual_pr_str == expected_pr_rounded, f"Row {i+1}: Expected pagerank '{expected_pr_rounded}', got '{actual_pr_str}'"