# test_final_state.py

import os
import json
from collections import defaultdict
import pytest

def get_expected_result():
    """Dynamically compute the expected result from the raw JSON file."""
    json_path = "/home/user/raw_edges.json"
    assert os.path.isfile(json_path), f"File {json_path} is missing."

    with open(json_path, 'r') as f:
        try:
            edges = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    graph = defaultdict(set)
    for edge in edges:
        src = edge.get('src')
        dst = edge.get('dst')
        if src is not None and dst is not None and src != dst:
            # Undirected graph, add both directions
            graph[src].add(dst)
            graph[dst].add(src)

    max_degree = -1
    max_node = -1

    for node, neighbors in graph.items():
        degree = len(neighbors)
        if degree > max_degree:
            max_degree = degree
            max_node = node
        elif degree == max_degree:
            if node < max_node:
                max_node = node

    return f"Max Degree Node: {max_node}, Degree: {max_degree}"

def test_analyze_cpp_exists():
    """Check if the analyze.cpp file was created."""
    path = "/home/user/analyze.cpp"
    assert os.path.isfile(path), f"Required source file {path} is missing."

def test_result_txt_exists_and_correct():
    """Check if result.txt exists and contains the correct output."""
    path = "/home/user/result.txt"
    assert os.path.isfile(path), f"Output file {path} was not generated."

    expected_output = get_expected_result()

    with open(path, 'r') as f:
        content = f.read().strip()

    assert content == expected_output, (
        f"Incorrect content in {path}.\n"
        f"Expected: '{expected_output}'\n"
        f"Got: '{content}'"
    )