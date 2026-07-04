# test_final_state.py
import os
import json
import pytest

def compute_expected_size(manifest_path, start_node="db_primary"):
    with open(manifest_path, 'r') as f:
        data = json.load(f)

    nodes = {}
    edges = {}

    for item in data:
        if item.get("type") == "node":
            nodes[item["id"]] = item["size"]
        elif item.get("type") == "edge":
            src = item["source"]
            tgt = item["target"]
            if src not in edges:
                edges[src] = []
            edges[src].append(tgt)

    # Traverse the graph to compute total size
    total_size = 0
    visited = set()
    queue = [start_node]

    while queue:
        current = queue.pop(0)
        if current not in visited:
            visited.add(current)
            total_size += nodes.get(current, 0)
            for neighbor in edges.get(current, []):
                queue.append(neighbor)

    return total_size

def test_report_contains_correct_size():
    manifest_path = "/home/user/backup_manifest.json"
    report_path = "/home/user/report.txt"

    assert os.path.exists(manifest_path), f"Manifest file missing at {manifest_path}"
    assert os.path.exists(report_path), f"Report file missing at {report_path}"

    expected_size = compute_expected_size(manifest_path)

    with open(report_path, 'r') as f:
        report_content = f.read().strip()

    assert report_content == str(expected_size), (
        f"Expected report to contain '{expected_size}', but found '{report_content}'"
    )

def test_rust_code_not_hardcoded():
    main_rs = "/home/user/backup_graph/src/main.rs"
    assert os.path.exists(main_rs), f"Missing main.rs at {main_rs}"

    with open(main_rs, 'r') as f:
        content = f.read()

    # Ensure the user didn't just hardcode the print statement
    assert "println!(\"400\")" not in content.replace(" ", ""), "The result should not be hardcoded in main.rs"
    assert "400" not in content, "The result should not be hardcoded in main.rs"