# test_final_state.py
import os
import json
from collections import deque

def compute_expected(start_node="node_0", end_node="node_49", db_path="/home/user/graph_db/nodes"):
    def load_node(node_id):
        path = os.path.join(db_path, f"{node_id}.json")
        if not os.path.isfile(path):
            return {"id": node_id, "weight": 0, "linked_nodes": []}
        with open(path) as f:
            return json.load(f)

    visited = set()
    queue = deque([(start_node, 0)])
    shortest_hops = -1
    reachable_nodes = []

    while queue:
        curr, hops = queue.popleft()
        if curr not in visited:
            visited.add(curr)
            node_data = load_node(curr)
            reachable_nodes.append(node_data)

            if curr == end_node and shortest_hops == -1:
                shortest_hops = hops

            for neighbor in node_data.get("linked_nodes", []):
                if neighbor not in visited:
                    queue.append((neighbor, hops + 1))

    total_weight = sum(n.get("weight", 0) for n in reachable_nodes)

    filtered = [n for n in reachable_nodes if n.get("weight", 0) >= 20]
    filtered.sort(key=lambda x: (-x.get("weight", 0), x.get("id", "")))
    top_3 = [n["id"] for n in filtered[:3]]

    return shortest_hops, total_weight, ", ".join(top_3)

def test_etl_pipeline_script_exists_and_executable():
    script_path = "/home/user/etl_pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_etl_report_contents():
    report_path = "/home/user/etl_report.txt"
    assert os.path.isfile(report_path), f"Report {report_path} does not exist. Did you execute the script?"

    with open(report_path, "r") as f:
        content = f.read().strip()
        lines = [line.strip() for line in content.split('\n')]

    assert len(lines) == 3, f"Report should have exactly 3 lines, but found {len(lines)} lines."

    expected_hops, expected_weight, expected_top3 = compute_expected()

    assert lines[0] == str(expected_hops), f"Line 1 (Shortest Path Hops) is incorrect. Expected '{expected_hops}', got '{lines[0]}'."
    assert lines[1] == str(expected_weight), f"Line 2 (Total Weight) is incorrect. Expected '{expected_weight}', got '{lines[1]}'."
    assert lines[2] == expected_top3, f"Line 3 (Top 3 nodes) is incorrect. Expected '{expected_top3}', got '{lines[2]}'."