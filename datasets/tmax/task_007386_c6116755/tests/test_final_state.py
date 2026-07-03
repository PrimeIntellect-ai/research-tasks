# test_final_state.py
import os
from collections import defaultdict
import itertools

def test_go_script_exists():
    script_path = "/home/user/project_graph.go"
    assert os.path.isfile(script_path), f"Expected Go script at {script_path} is missing."

def test_output_file_exists():
    output_path = "/home/user/output/item_item_edges.csv"
    assert os.path.isfile(output_path), f"Expected output file at {output_path} is missing."

def test_output_content():
    input_path = "/home/user/data/user_item.csv"
    output_path = "/home/user/output/item_item_edges.csv"

    assert os.path.isfile(input_path), f"Input file {input_path} is missing."

    # Compute expected output
    user_items = defaultdict(set)
    with open(input_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            user, item = line.split(",")
            user_items[user].add(item)

    item_pairs = defaultdict(int)
    for user, items in user_items.items():
        # Generate all combinations of items for this user
        for item1, item2 in itertools.combinations(sorted(list(items)), 2):
            item_pairs[(item1, item2)] += 1

    expected_edges = []
    for (item1, item2), weight in item_pairs.items():
        if weight >= 2:
            expected_edges.append((item1, item2, weight))

    # Sort by weight (desc), item_1 (asc), item_2 (asc)
    expected_edges.sort(key=lambda x: (-x[2], x[0], x[1]))

    expected_lines = [f"{i1},{i2},{w}" for i1, i2, w in expected_edges]

    # Read actual output
    with open(output_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"Output file content is incorrect.\nExpected:\n{chr(10).join(expected_lines)}\n\nActual:\n{chr(10).join(actual_lines)}"