# test_final_state.py

import os
import json
import pytest

def parse_version(version_str):
    return tuple(map(int, version_str.split('.')))

def test_audit_go_exists():
    assert os.path.isfile("/home/user/audit.go"), "/home/user/audit.go does not exist. You must write your Go code here."

def test_new_vuln_apps_correctness():
    deps_path = "/home/user/deps.json"
    rules_path = "/home/user/rules.txt"
    baseline_path = "/home/user/baseline.txt"
    output_path = "/home/user/new_vuln_apps.txt"

    assert os.path.isfile(output_path), f"The output file {output_path} was not created."

    # 1. Deserialize the Dependency Graph
    with open(deps_path, 'r') as f:
        deps_data = json.load(f)

    nodes = {node["id"]: node for node in deps_data.get("nodes", [])}
    edges = deps_data.get("edges", [])

    # Build adjacency list for dependencies
    graph = {node_id: [] for node_id in nodes}
    for edge in edges:
        if edge["from"] in graph:
            graph[edge["from"]].append(edge["to"])

    # 2. Evaluate Vulnerability Rules
    vulnerable_nodes = set()
    with open(rules_path, 'r') as f:
        rules = [line.strip() for line in f if line.strip()]

    for rule in rules:
        parts = rule.split('<')
        if len(parts) != 2:
            continue
        pkg_name = parts[0].strip()
        rule_version = parse_version(parts[1].strip())

        for node_id, node in nodes.items():
            if node["name"] == pkg_name:
                node_version = parse_version(node["version"])
                if node_version < rule_version:
                    vulnerable_nodes.add(node_id)

    # 3. Graph Traversal
    def is_affected(node_id, visited):
        if node_id in vulnerable_nodes:
            return True
        visited.add(node_id)
        for dep in graph.get(node_id, []):
            if dep not in visited:
                if is_affected(dep, visited):
                    return True
        return False

    affected_apps = set()
    for node_id, node in nodes.items():
        if node["type"] == "app":
            if is_affected(node_id, set()):
                affected_apps.add(node_id)

    # 4. Diffing and Sorting
    with open(baseline_path, 'r') as f:
        baseline = set(line.strip() for line in f if line.strip())

    new_vuln_apps = sorted(list(affected_apps - baseline))

    # Read the actual output
    with open(output_path, 'r') as f:
        actual_output = [line.strip() for line in f if line.strip()]

    assert actual_output == new_vuln_apps, (
        f"The contents of {output_path} do not match the expected newly vulnerable applications.\n"
        f"Expected: {new_vuln_apps}\n"
        f"Actual: {actual_output}"
    )