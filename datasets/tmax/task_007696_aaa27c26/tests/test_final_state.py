# test_final_state.py
import os
import json
import csv
import math
import pytest

EDGES_CSV_PATH = "/home/user/edges.csv"
TOP_AUTHORS_JSON_PATH = "/home/user/top_authors.json"

def test_edges_csv_exists_and_format():
    assert os.path.exists(EDGES_CSV_PATH), f"Edges file missing at {EDGES_CSV_PATH}"
    assert os.path.isfile(EDGES_CSV_PATH), f"Expected a file at {EDGES_CSV_PATH}"

    with open(EDGES_CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail(f"{EDGES_CSV_PATH} is empty.")

        # Header should be author1,author2
        assert [h.strip() for h in header] == ["author1", "author2"], \
            f"Expected header ['author1', 'author2'], found {header}"

        edges = []
        for row in reader:
            if not row:
                continue
            assert len(row) == 2, f"Expected 2 columns in row, found {len(row)}: {row}"
            u, v = row[0].strip(), row[1].strip()
            assert u != v, f"Self-loop found in edges: {u} - {v}"
            # Store as a canonical sorted tuple to ignore direction
            edges.append(tuple(sorted([u, v])))

    # Check for duplicates
    unique_edges = set(edges)
    assert len(edges) == len(unique_edges), "Duplicate edges found in the CSV (graph should be unweighted/undirected)."

    # There should be exactly 7 unique edges based on the setup
    assert len(unique_edges) == 7, f"Expected exactly 7 edges, found {len(unique_edges)}"

def test_top_authors_json():
    assert os.path.exists(TOP_AUTHORS_JSON_PATH), f"JSON file missing at {TOP_AUTHORS_JSON_PATH}"
    assert os.path.isfile(TOP_AUTHORS_JSON_PATH), f"Expected a file at {TOP_AUTHORS_JSON_PATH}"

    with open(TOP_AUTHORS_JSON_PATH, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Invalid JSON in {TOP_AUTHORS_JSON_PATH}: {e}")

    assert isinstance(data, list), f"Expected JSON root to be a list, found {type(data).__name__}"
    assert len(data) == 3, f"Expected exactly 3 top authors, found {len(data)}"

    expected = [
        {"name": "Alice Smith", "centrality": 0.8},
        {"name": "Bob Jones", "centrality": 0.6},
        {"name": "Charlie Brown", "centrality": 0.4}
    ]

    for i, (actual_item, expected_item) in enumerate(zip(data, expected)):
        assert isinstance(actual_item, dict), f"Item at index {i} is not a dictionary."
        assert "name" in actual_item, f"Missing 'name' key in item at index {i}."
        assert "centrality" in actual_item, f"Missing 'centrality' key in item at index {i}."

        actual_name = actual_item["name"]
        expected_name = expected_item["name"]
        assert actual_name == expected_name, \
            f"Rank {i+1} expected name '{expected_name}', found '{actual_name}'."

        actual_cent = actual_item["centrality"]
        expected_cent = expected_item["centrality"]
        assert isinstance(actual_cent, (int, float)), \
            f"Centrality for {actual_name} should be a number, found {type(actual_cent).__name__}."

        assert math.isclose(actual_cent, expected_cent, rel_tol=1e-3, abs_tol=1e-3), \
            f"Rank {i+1} expected centrality ~{expected_cent}, found {actual_cent}."