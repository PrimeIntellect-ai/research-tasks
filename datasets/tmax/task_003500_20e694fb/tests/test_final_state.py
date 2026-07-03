# test_final_state.py
import os
import json
from collections import defaultdict

def test_influencer_calc_project_exists():
    path = "/home/user/influencer_calc"
    assert os.path.isdir(path), f"Rust project directory {path} does not exist."
    assert os.path.isfile(os.path.join(path, "Cargo.toml")), f"Cargo.toml not found in {path}. Is it a valid Rust project?"

def test_result_json_exists():
    path = "/home/user/result.json"
    assert os.path.isfile(path), f"Output file {path} does not exist."

def test_result_json_content():
    edges_path = "/home/user/edges.csv"
    assert os.path.isfile(edges_path), f"Input file {edges_path} missing."

    # Recompute the truth
    adj = defaultdict(set)
    with open(edges_path, 'r') as f:
        header = f.readline()
        for line in f:
            if not line.strip():
                continue
            u, v = map(int, line.strip().split(','))
            adj[u].add(v)
            adj[v].add(u)

    scores = []
    for node in adj:
        friends = adj[node]
        fof = set()
        for friend in friends:
            fof.update(adj[friend])
        # remove direct friends and self
        fof -= friends
        fof.discard(node)
        scores.append((node, len(fof)))

    scores.sort(key=lambda x: (-x[1], x[0]))
    expected_top_5 = [[n, s] for n, s in scores[:5]]

    result_path = "/home/user/result.json"
    with open(result_path, 'r') as f:
        try:
            actual_top_5 = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {result_path} is not valid JSON."

    assert isinstance(actual_top_5, list), f"Expected JSON array, got {type(actual_top_5).__name__}"
    assert len(actual_top_5) == 5, f"Expected exactly 5 results, got {len(actual_top_5)}"

    # Convert inner elements to lists in case they are tuples or other types
    actual_top_5 = [list(item) for item in actual_top_5]

    assert actual_top_5 == expected_top_5, f"Expected {expected_top_5}, but got {actual_top_5}"