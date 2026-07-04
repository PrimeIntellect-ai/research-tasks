# test_final_state.py

import os
import csv
import json
from collections import defaultdict

def test_aggregated_roles_json():
    """Test that the output JSON file has the correct aggregated graph metrics."""
    csv_path = "/home/user/edges.csv"
    json_path = "/home/user/aggregated_roles.json"

    assert os.path.exists(json_path), f"Output file {json_path} does not exist."

    # Recompute the expected metrics from the input CSV
    in_weight = defaultdict(int)
    out_weight = defaultdict(int)
    nodes = set()

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            src = row['source']
            tgt = row['target']
            weight = int(row['weight'])

            out_weight[src] += weight
            in_weight[tgt] += weight
            nodes.add(src)
            nodes.add(tgt)

    expected = defaultdict(lambda: {"nodes": [], "total_activity": 0})

    for node in nodes:
        iw = in_weight[node]
        ow = out_weight[node]
        activity = iw + ow

        if iw > ow:
            role = "net_sink"
        elif ow > iw:
            role = "net_source"
        else:
            role = "balanced"

        expected[role]["nodes"].append(node)
        expected[role]["total_activity"] += activity

    for role in expected:
        expected[role]["nodes"].sort()

    # Load the actual JSON output
    with open(json_path, 'r') as f:
        try:
            actual = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_path} is not valid JSON."

    # Verify the output matches the expected aggregations
    for role, data in expected.items():
        assert role in actual, f"Expected role '{role}' is missing in the output JSON."

        actual_nodes = actual[role].get("nodes", [])
        actual_activity = actual[role].get("total_activity", 0)

        assert actual_nodes == data["nodes"], (
            f"Mismatch in nodes for role '{role}'. "
            f"Expected {data['nodes']}, got {actual_nodes}."
        )
        assert actual_activity == data["total_activity"], (
            f"Mismatch in total_activity for role '{role}'. "
            f"Expected {data['total_activity']}, got {actual_activity}."
        )