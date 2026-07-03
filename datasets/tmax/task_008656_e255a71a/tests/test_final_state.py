# test_final_state.py

import os
import json
import pytest
from collections import defaultdict, deque

def load_graph():
    logs_path = "/home/user/access_logs.jsonl"
    assert os.path.exists(logs_path), f"File {logs_path} is missing."

    graph = defaultdict(list)
    out_degree = defaultdict(int)

    with open(logs_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            grantor = data.get("grantor_id")
            grantee = data.get("grantee_id") or data.get("resource_id")
            if grantor and grantee:
                graph[grantor].append(grantee)
                out_degree[grantor] += 1

    return graph, out_degree

def compute_shortest_path_length(graph, start, end):
    queue = deque([(start, 1)])
    visited = {start}

    while queue:
        node, dist = queue.popleft()
        if node == end:
            return dist
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return float('inf')

def test_audit_report_exists_and_format():
    report_path = "/home/user/audit_report.json"
    assert os.path.exists(report_path), f"Output file {report_path} does not exist."

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    assert "shortest_path" in data, "Key 'shortest_path' is missing from audit_report.json."
    assert "top_grantors" in data, "Key 'top_grantors' is missing from audit_report.json."

    assert isinstance(data["shortest_path"], list), "'shortest_path' must be a list."
    assert isinstance(data["top_grantors"], list), "'top_grantors' must be a list."

def test_shortest_path_validity():
    report_path = "/home/user/audit_report.json"
    if not os.path.exists(report_path):
        pytest.fail(f"File {report_path} is missing.")

    with open(report_path, 'r') as f:
        data = json.load(f)

    path = data.get("shortest_path", [])
    assert len(path) > 0, "'shortest_path' is empty."
    assert path[0] == "E_VENDOR", f"Expected path to start with 'E_VENDOR', got {path[0]}"
    assert path[-1] == "R_SECURE_PAYMENTS", f"Expected path to end with 'R_SECURE_PAYMENTS', got {path[-1]}"

    graph, _ = load_graph()

    # Check if the path is valid
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i+1]
        assert v in graph[u], f"Invalid edge in shortest_path: {u} -> {v} does not exist."

    # Check if it's actually the shortest path
    expected_length = compute_shortest_path_length(graph, "E_VENDOR", "R_SECURE_PAYMENTS")
    assert len(path) == expected_length, f"Expected shortest path of length {expected_length} (nodes), but got {len(path)}."

def test_top_grantors_correctness():
    report_path = "/home/user/audit_report.json"
    if not os.path.exists(report_path):
        pytest.fail(f"File {report_path} is missing.")

    with open(report_path, 'r') as f:
        data = json.load(f)

    top_grantors_actual = data.get("top_grantors", [])

    _, out_degree = load_graph()

    # Sort by grants descending, then emp_id ascending
    sorted_grantors = sorted(out_degree.items(), key=lambda x: (-x[1], x[0]))
    expected_top_3 = [{"emp_id": k, "grants": v} for k, v in sorted_grantors[:3]]

    assert len(top_grantors_actual) == 3, f"Expected exactly 3 top grantors, got {len(top_grantors_actual)}."

    for i in range(3):
        actual = top_grantors_actual[i]
        expected = expected_top_3[i]

        assert "emp_id" in actual, f"Missing 'emp_id' in top_grantors item at index {i}."
        assert "grants" in actual, f"Missing 'grants' in top_grantors item at index {i}."

        assert actual["emp_id"] == expected["emp_id"], f"Expected emp_id {expected['emp_id']} at index {i}, got {actual['emp_id']}."
        assert actual["grants"] == expected["grants"], f"Expected {expected['grants']} grants for {expected['emp_id']}, got {actual['grants']}."