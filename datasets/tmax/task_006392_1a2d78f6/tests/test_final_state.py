# test_final_state.py
import os
import json
import pytest

SCHEMA_PATH = "/home/user/schema.json"
OUTPUT_PATH = "/home/user/users_dependencies.txt"

def test_users_dependencies_output():
    assert os.path.exists(SCHEMA_PATH), f"Required file {SCHEMA_PATH} is missing."
    assert os.path.exists(OUTPUT_PATH), f"Output file {OUTPUT_PATH} does not exist. Did you run your script?"
    assert os.path.isfile(OUTPUT_PATH), f"Expected {OUTPUT_PATH} to be a file."

    with open(SCHEMA_PATH, 'r') as f:
        schema = json.load(f)

    # Compute expected dependencies dynamically
    graph = {t['name']: [fk['references'] for fk in t.get('fks', [])] for t in schema.get('tables', [])}
    reverse_graph = {t: [] for t in graph}
    for t, fks in graph.items():
        for fk in fks:
            if fk in reverse_graph:
                reverse_graph[fk].append(t)
            else:
                reverse_graph[fk] = [t]

    deps = set()
    queue = reverse_graph.get('users', [])[:]
    while queue:
        curr = queue.pop(0)
        if curr not in deps:
            deps.add(curr)
            queue.extend(reverse_graph.get(curr, []))

    expected_deps = sorted(list(deps))

    with open(OUTPUT_PATH, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_deps, (
        f"Dependencies in {OUTPUT_PATH} do not match expected output.\n"
        f"Expected: {expected_deps}\n"
        f"Actual: {actual_lines}"
    )