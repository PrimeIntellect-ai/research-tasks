# test_final_state.py

import os
import csv
from collections import defaultdict

def test_top_datasets_file_exists():
    file_path = "/home/user/dataset_graph/top_datasets.txt"
    assert os.path.isfile(file_path), f"Expected output file {file_path} does not exist. Did you run the program and redirect/write the output?"

def test_top_datasets_content():
    csv_path = "/home/user/dataset_graph/graph_data.csv"
    assert os.path.isfile(csv_path), f"Input file {csv_path} is missing."

    # Recompute the expected centrality scores
    dataset_to_tags = defaultdict(set)
    tag_to_datasets = defaultdict(set)

    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                d, t = row[0].strip(), row[1].strip()
                dataset_to_tags[d].add(t)
                tag_to_datasets[t].add(d)

    scores = {}
    for d, tags in dataset_to_tags.items():
        neighbors = set()
        for t in tags:
            neighbors.update(tag_to_datasets[t])
        neighbors.discard(d)  # Exclude self
        scores[d] = len(neighbors)

    # Sort by score descending, then by dataset ID ascending (string comparison)
    sorted_datasets = sorted(scores.items(), key=lambda x: (-x[1], x[0]))

    # Top 5 expected
    top_5 = sorted_datasets[:5]
    expected_lines = [f"{d}:{score}" for d, score in top_5]

    # Read actual output
    out_path = "/home/user/dataset_graph/top_datasets.txt"
    with open(out_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == 5, f"Expected exactly 5 lines in top_datasets.txt, found {len(actual_lines)}."

    for i, (expected, actual) in enumerate(zip(expected_lines, actual_lines)):
        assert expected == actual, f"Mismatch at line {i+1}. Expected '{expected}', got '{actual}'."