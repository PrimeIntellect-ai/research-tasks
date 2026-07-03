# test_final_state.py

import os
import json
import csv
from collections import defaultdict
import pytest

def test_metrics_json_correctness():
    csv_path = "/home/user/data/comments.csv"
    json_path = "/home/user/metrics.json"

    assert os.path.isfile(csv_path), f"Missing {csv_path}"
    assert os.path.isfile(json_path), f"Missing {json_path}"

    # Recompute truth from the CSV
    thread_to_users = defaultdict(set)
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            u = int(row['user_id'])
            t = int(row['thread_id'])
            thread_to_users[t].add(u)

    edges = set()
    for t, users in thread_to_users.items():
        user_list = sorted(list(users))
        for i in range(len(user_list)):
            for j in range(i + 1, len(user_list)):
                edges.add((user_list[i], user_list[j]))

    degrees = defaultdict(int)
    for u, v in edges:
        degrees[u] += 1
        degrees[v] += 1

    expected_edges = len(edges)

    max_deg = -1
    max_user = -1
    # Sort keys to resolve ties by picking the smallest user_id
    for u in sorted(degrees.keys()):
        if degrees[u] > max_deg:
            max_deg = degrees[u]
            max_user = u

    with open(json_path, 'r') as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("metrics.json is not valid JSON")

    assert "total_unique_edges" in metrics, "Missing 'total_unique_edges' in metrics.json"
    assert "max_degree_user_id" in metrics, "Missing 'max_degree_user_id' in metrics.json"

    actual_edges = metrics["total_unique_edges"]
    actual_max_user = metrics["max_degree_user_id"]

    assert actual_edges == expected_edges, f"Incorrect total_unique_edges: expected {expected_edges}, got {actual_edges}"
    assert actual_max_user == max_user, f"Incorrect max_degree_user_id: expected {max_user}, got {actual_max_user}"