# test_final_state.py

import os
import json
import csv
import subprocess
import pytest

def test_query_graph_script_exists():
    script_path = "/home/user/query_graph.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

def test_query_graph_execution_and_logic():
    script_path = "/home/user/query_graph.py"
    output_path = "/home/user/test_output.json"

    if os.path.exists(output_path):
        os.remove(output_path)

    cmd = [
        "python3", script_path,
        "--action", "PURCHASED",
        "--min-weight", "40",
        "--sort-order", "desc",
        "--limit", "2",
        "--offset", "1",
        "--output", output_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}\nOutput: {result.stdout}"

    assert os.path.isfile(output_path), f"Output file {output_path} was not created by the script."

    with open(output_path, "r") as f:
        try:
            output_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Output file is not valid JSON.")

    # Recompute the expected result using standard libraries to ensure correctness
    nodes = {}
    with open("/home/user/graph_data/nodes.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            nodes[row["node_id"]] = {
                "label": row["label"],
                "weight": int(row["weight"])
            }

    edges = []
    with open("/home/user/graph_data/edges.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            edges.append(row)

    # Find all valid paths
    paths = []
    for e1 in edges:
        if e1["rel_type"] == "PURCHASED":
            u_id = e1["source_id"]
            i_id = e1["target_id"]

            if u_id in nodes and nodes[u_id]["label"] == "User" and i_id in nodes and nodes[i_id]["label"] == "Item":
                if nodes[i_id]["weight"] >= 40:
                    for e2 in edges:
                        if e2["source_id"] == i_id and e2["rel_type"] == "BELONGS_TO":
                            c_id = e2["target_id"]
                            if c_id in nodes and nodes[c_id]["label"] == "Category":
                                path_score = nodes[u_id]["weight"] + nodes[i_id]["weight"]
                                paths.append({
                                    "user_id": u_id,
                                    "item_id": i_id,
                                    "category_id": c_id,
                                    "path_score": path_score
                                })

    # Sort paths: desc by path_score, asc by user_id
    paths.sort(key=lambda x: (-x["path_score"], x["user_id"]))

    # Apply pagination (offset=1, limit=2)
    expected_data = paths[1:3]

    assert output_data == expected_data, (
        f"Output JSON does not match expected data.\n"
        f"Expected: {json.dumps(expected_data, indent=2)}\n"
        f"Got: {json.dumps(output_data, indent=2)}"
    )