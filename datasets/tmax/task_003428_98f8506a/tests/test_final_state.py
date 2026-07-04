# test_final_state.py

import os
import math
from collections import deque
import pytest

def get_expected_results():
    edgelist_path = '/home/user/molecule.edgelist'
    assert os.path.exists(edgelist_path), f"Missing {edgelist_path}"

    adj = {}
    max_node = 0
    with open(edgelist_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            u, v = map(int, line.split())
            if u not in adj: adj[u] = []
            if v not in adj: adj[v] = []
            adj[u].append(v)
            adj[v].append(u)
            max_node = max(max_node, u, v)

    N = max_node + 1

    lengths = {}
    D = 0
    counts = {}
    total_pairs = 0

    for start in range(N):
        q = deque([start])
        dist = {start: 0}
        while q:
            u = q.popleft()
            for v in adj.get(u, []):
                if v not in dist:
                    dist[v] = dist[u] + 1
                    q.append(v)

        for v, d in dist.items():
            if start < v:
                counts[d] = counts.get(d, 0) + 1
                if d > D:
                    D = d
                total_pairs += 1

    emp = {d: counts.get(d, 0) / total_pairs for d in range(1, D + 1)}

    def T(d):
        return (3**d) / math.factorial(d)

    sum_T = sum(T(d) for d in range(1, D + 1))
    theory = {d: T(d) / sum_T for d in range(1, D + 1)}

    tvd = 0.5 * sum(abs(emp.get(d, 0) - theory[d]) for d in range(1, D + 1))

    return D, tvd

def test_fit_results_exists():
    results_path = '/home/user/fit_results.txt'
    assert os.path.exists(results_path), f"File {results_path} does not exist."
    assert os.path.isfile(results_path), f"{results_path} is not a file."

def test_fit_results_content():
    results_path = '/home/user/fit_results.txt'
    assert os.path.exists(results_path), f"File {results_path} does not exist."

    expected_D, expected_tvd = get_expected_results()

    with open(results_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {results_path}, found {len(lines)}"

    expected_line1 = f"Diameter: {expected_D}"
    expected_line2 = f"TVD: {expected_tvd:.4f}"

    assert lines[0] == expected_line1, f"First line mismatch. Expected '{expected_line1}', got '{lines[0]}'"
    assert lines[1] == expected_line2, f"Second line mismatch. Expected '{expected_line2}', got '{lines[1]}'"