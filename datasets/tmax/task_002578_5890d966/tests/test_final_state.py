# test_final_state.py

import os
import pytest
from collections import defaultdict, deque

def get_expected_output():
    classifications_path = "/home/user/node_classifications.txt"
    edges_path = "/home/user/raw_schema_edges.csv"

    if not os.path.exists(classifications_path) or not os.path.exists(edges_path):
        return None

    classifications = {}
    with open(classifications_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and ":" in line:
                node, cls = line.split(":", 1)
                classifications[node] = cls

    sensitive = [n for n, c in classifications.items() if c == "Sensitive"]
    public = set([n for n, c in classifications.items() if c == "Public"])

    adj = defaultdict(list)
    with open(edges_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(",")
                if len(parts) == 3:
                    src, tgt, status = parts
                    if status == "Active":
                        adj[src].append(tgt)

    paths = []
    for start in sensitive:
        q = deque([[start]])
        distances = {start: 0}

        while q:
            path = q.popleft()
            curr = path[-1]

            if curr in public:
                paths.append(path)
                continue

            for nxt in adj.get(curr, []):
                # Allow discovering multiple paths of the same length to the same node
                if nxt not in distances or distances[nxt] >= len(path):
                    distances[nxt] = len(path)
                    q.append(path + [nxt])

    if not paths:
        return "COMPLIANT: No paths found"

    min_len = min(len(p) for p in paths)
    best_paths = [p for p in paths if len(p) == min_len]

    formatted_paths = [" -> ".join(p) for p in best_paths]
    formatted_paths.sort()

    return f"VIOLATION: {formatted_paths[0]}"

def test_cpp_source_exists():
    path = "/home/user/audit_paths.cpp"
    assert os.path.isfile(path), f"C++ source code is missing at {path}"

def test_cpp_executable_exists():
    path = "/home/user/audit_paths"
    assert os.path.isfile(path), f"Compiled C++ executable is missing at {path}"
    assert os.access(path, os.X_OK), f"File at {path} is not executable"

def test_bash_script_exists_and_executable():
    path = "/home/user/audit_pipeline.sh"
    assert os.path.isfile(path), f"Bash script is missing at {path}"
    assert os.access(path, os.X_OK), f"Bash script at {path} is not executable"

def test_audit_report_content():
    path = "/home/user/audit_report.txt"
    assert os.path.isfile(path), f"Audit report is missing at {path}. Did you run the pipeline?"

    with open(path, "r") as f:
        actual_content = f.read().strip()

    expected_content = get_expected_output()
    assert expected_content is not None, "Setup files are missing, cannot compute expected output."

    assert actual_content == expected_content, (
        f"Audit report content does not match expected output.\n"
        f"Expected: '{expected_content}'\n"
        f"Actual:   '{actual_content}'"
    )