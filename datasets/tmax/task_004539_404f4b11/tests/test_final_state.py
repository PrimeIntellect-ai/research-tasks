# test_final_state.py
import os
import json
import csv
import pytest

def test_cpp_file_exists():
    assert os.path.isfile("/home/user/deadlock_analyzer.cpp"), "C++ source file /home/user/deadlock_analyzer.cpp is missing."

def test_executable_exists():
    exe_path = "/home/user/deadlock_analyzer"
    assert os.path.isfile(exe_path), f"Compiled executable {exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_json_output_correctness():
    json_path = "/home/user/deadlock_report.json"
    assert os.path.isfile(json_path), f"Output JSON file {json_path} is missing."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    assert "deadlocks" in data, "JSON must contain a 'deadlocks' key at the root."
    deadlocks = data["deadlocks"]
    assert isinstance(deadlocks, list), "'deadlocks' must be an array."

    # Recompute the expected wait-for graph and cycles from the CSV
    csv_path = "/home/user/tx_locks.csv"
    assert os.path.isfile(csv_path), f"Input CSV file {csv_path} is missing."

    granted = {}
    waiting = []

    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["status"] == "GRANTED":
                granted[row["resource_id"]] = row["tx_id"]
            elif row["status"] == "WAITING":
                waiting.append((row["tx_id"], row["resource_id"]))

    # Graph: tx_id -> list of tx_ids it is waiting for
    graph = {}
    for tx, res in waiting:
        if res in granted:
            target = granted[res]
            graph.setdefault(tx, []).append(target)

    # DFS to find all elementary cycles
    def find_cycles(graph):
        cycles = []
        visited = set()
        path = []

        def dfs(node):
            if node in path:
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:])
                return
            if node in visited:
                return

            path.append(node)
            visited.add(node)
            for neighbor in graph.get(node, []):
                dfs(neighbor)
            path.pop()

        for node in graph:
            if node not in visited:
                dfs(node)

        # Normalize cycles (sort internally) and remove duplicates
        normalized = set()
        for c in cycles:
            normalized.add(tuple(sorted(c)))

        return [list(c) for c in normalized]

    expected_cycles = find_cycles(graph)

    # Normalize actual output to compare contents
    normalized_actual = sorted([sorted(cycle) for cycle in deadlocks])
    normalized_expected = sorted([sorted(cycle) for cycle in expected_cycles])

    assert normalized_actual == normalized_expected, (
        f"Detected deadlocks do not match the expected cycles.\n"
        f"Expected: {normalized_expected}\n"
        f"Got: {normalized_actual}"
    )

def test_json_sorting_rules():
    json_path = "/home/user/deadlock_report.json"
    if not os.path.isfile(json_path):
        pytest.skip("Output JSON file is missing.")

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.skip("Invalid JSON.")

    deadlocks = data.get("deadlocks", [])
    if not isinstance(deadlocks, list):
        pytest.skip("'deadlocks' is not a list.")

    # Check internal sorting
    for cycle in deadlocks:
        assert cycle == sorted(cycle), f"Cycle {cycle} is not sorted alphabetically."

    # Check outer array sorting
    assert deadlocks == sorted(deadlocks, key=lambda x: x[0] if x else ""), (
        "The 'deadlocks' array is not sorted alphabetically by the first element of each cycle."
    )