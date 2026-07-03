# test_final_state.py

import os
import sqlite3
import json
import pytest

DB_PATH = "/home/user/backups.db"
REPORT_PATH = "/home/user/pagerank_report.json"

def compute_pagerank(edges, alpha=0.85, max_iter=100, tol=1.0e-6):
    """
    Computes PageRank using the same default algorithm as NetworkX.
    """
    nodes = set()
    out_degree = {}
    for u, v in edges:
        nodes.add(u)
        nodes.add(v)
        out_degree[u] = out_degree.get(u, 0) + 1
        if v not in out_degree:
            out_degree[v] = 0

    N = len(nodes)
    if N == 0:
        return {}

    pr = {n: 1.0 / N for n in nodes}

    for _ in range(max_iter):
        prev_pr = pr.copy()
        dangling_sum = sum(prev_pr[n] for n in nodes if out_degree[n] == 0)

        for n in nodes:
            pr[n] = (1.0 - alpha) / N + alpha * (dangling_sum / N)

        for u, v in edges:
            pr[v] += alpha * prev_pr[u] / out_degree[u]

        err = sum(abs(pr[n] - prev_pr[n]) for n in nodes)
        if err < N * tol:
            break

    return pr

def test_pagerank_report_exists_and_valid():
    assert os.path.exists(REPORT_PATH), f"Report file {REPORT_PATH} does not exist."

    with open(REPORT_PATH, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Report file is not valid JSON.")

    assert isinstance(report, dict), "Root of JSON must be an object."
    assert "pagerank_scores" in report, "Root object must have a single key 'pagerank_scores'."
    assert len(report) == 1, "Root object must have exactly one key."

    scores = report["pagerank_scores"]
    assert isinstance(scores, list), "'pagerank_scores' must be a list."

def test_pagerank_report_values():
    assert os.path.exists(REPORT_PATH), f"Report file {REPORT_PATH} does not exist."
    with open(REPORT_PATH, "r") as f:
        report = json.load(f)
    scores = report.get("pagerank_scores", [])

    # Retrieve active edges from DB
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} does not exist."
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT source_job, target_job FROM job_dependencies WHERE is_active = 1")
    edges = c.fetchall()
    conn.close()

    # Compute expected PageRank
    pr = compute_pagerank(edges)
    expected_results = [{"job": k, "score": round(v, 4)} for k, v in pr.items()]
    expected_results.sort(key=lambda x: (-x["score"], x["job"]))

    assert len(scores) == len(expected_results), f"Expected {len(expected_results)} scores, found {len(scores)}."

    for i, (actual, expected) in enumerate(zip(scores, expected_results)):
        assert isinstance(actual, dict), f"Item at index {i} is not a dictionary."
        assert set(actual.keys()) == {"job", "score"}, f"Item at index {i} must have exactly 'job' and 'score' keys."

        assert isinstance(actual["job"], str), f"'job' at index {i} must be a string."
        assert isinstance(actual["score"], float), f"'score' at index {i} must be a float."

        assert actual["job"] == expected["job"], f"Expected job '{expected['job']}' at index {i}, found '{actual.get('job')}'."
        assert actual["score"] == expected["score"], f"Expected score {expected['score']} for job '{expected['job']}', found {actual.get('score')}."