# test_final_state.py

import os
import json
from collections import defaultdict

def test_projected_graph_exists():
    """Test that the output file projected_graph.json exists."""
    output_path = "/home/user/projected_graph.json"
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

def test_projected_graph_content():
    """Test that the projected_graph.json contains the correct derived output."""
    input_path = "/home/user/audit_logs.jsonl"
    output_path = "/home/user/projected_graph.json"

    assert os.path.isfile(input_path), f"Input file {input_path} is missing."
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    # 1. Derive expected state from input file
    edge_weights = defaultdict(int)
    with open(input_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            record = json.loads(line)
            sender = record.get("sender")
            recipient = record.get("recipient")
            if sender and recipient:
                edge_weights[(sender, recipient)] += 1

    # 2. Filter edges with weight < 3
    filtered_edges = [
        {"source": src, "target": tgt, "weight": weight}
        for (src, tgt), weight in edge_weights.items()
        if weight >= 3
    ]

    # 3. Sort: Weight DESC, Source ASC, Target ASC
    sorted_edges = sorted(
        filtered_edges,
        key=lambda x: (-x["weight"], x["source"], x["target"])
    )

    # 4. Paginate: Page 2, Page Size 2
    page = 2
    page_size = 2
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    expected_output = sorted_edges[start_idx:end_idx]

    # 5. Read actual output
    with open(output_path, 'r') as f:
        try:
            actual_output = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_path} is not valid JSON.")

    # 6. Validate output schema and content
    assert isinstance(actual_output, list), "Output must be a JSON array."
    assert len(actual_output) == len(expected_output), f"Expected {len(expected_output)} items, got {len(actual_output)}."

    for i, actual_item in enumerate(actual_output):
        expected_item = expected_output[i]

        # Check exact keys
        assert set(actual_item.keys()) == {"source", "target", "weight"}, \
            f"Item at index {i} has incorrect keys: {list(actual_item.keys())}"

        # Check types
        assert isinstance(actual_item["source"], str), f"Item {i} 'source' must be a string."
        assert isinstance(actual_item["target"], str), f"Item {i} 'target' must be a string."
        assert isinstance(actual_item["weight"], int), f"Item {i} 'weight' must be an integer."

        # Check values
        assert actual_item == expected_item, \
            f"Item at index {i} does not match expected.\nExpected: {expected_item}\nActual: {actual_item}"