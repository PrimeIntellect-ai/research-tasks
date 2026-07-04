# test_final_state.py

import os
import json
from collections import defaultdict, deque

def compute_truth():
    file_path = "/home/user/audit_data/transfers.jsonl"
    if not os.path.exists(file_path):
        return None, None, None

    transfers = []
    with open(file_path, "r") as f:
        for line in f:
            if line.strip():
                transfers.append(json.loads(line))

    # 1. Filter and Aggregate
    completed = [t for t in transfers if t.get("status") == "COMPLETED"]

    bytes_by_source = defaultdict(int)
    for t in completed:
        bytes_by_source[t["source"]] += t["bytes"]

    max_sender = None
    max_bytes = -1
    for source, total_bytes in bytes_by_source.items():
        if total_bytes > max_bytes:
            max_bytes = total_bytes
            max_sender = source

    # 2. Graph Traversal (Shortest Path)
    graph = defaultdict(list)
    for t in completed:
        graph[t["source"]].append(t["target"])

    shortest_path_length = -1
    queue = deque([("NODE_SUSPECT", 0)])
    visited = set(["NODE_SUSPECT"])

    while queue:
        current, dist = queue.popleft()
        if current == "NODE_VAULT":
            shortest_path_length = dist
            break

        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))

    return max_sender, max_bytes, shortest_path_length

def test_audit_report_exists():
    """Check that the audit report file was created."""
    assert os.path.isfile("/home/user/audit_report.txt"), "/home/user/audit_report.txt does not exist."

def test_audit_report_content():
    """Check that the audit report contains the correct computed values."""
    max_sender, max_bytes, shortest_path_length = compute_truth()

    assert max_sender is not None, "Could not compute truth values because data file is missing."

    expected_lines = [
        f"Highest Transfer Node: {max_sender}",
        f"Highest Transfer Bytes: {max_bytes}",
        f"Shortest Path Length: {shortest_path_length}"
    ]

    with open("/home/user/audit_report.txt", "r") as f:
        content = f.read()

    for expected in expected_lines:
        assert expected in content, f"Expected line '{expected}' not found in /home/user/audit_report.txt."