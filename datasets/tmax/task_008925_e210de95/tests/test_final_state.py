# test_final_state.py

import os
import pytest

def test_top_nodes_file_content():
    top_nodes_path = "/home/user/top_nodes.txt"
    assert os.path.isfile(top_nodes_path), f"Expected output file at {top_nodes_path} is missing."

    expected_content = "1. Alice - 4\n2. Bob - 3\n3. Dave - 3\n"
    expected_lines = [line.strip() for line in expected_content.strip().split("\n")]

    with open(top_nodes_path, "r") as f:
        actual_lines = [line.strip() for line in f.read().strip().split("\n")]

    assert actual_lines == expected_lines, (
        f"Content of {top_nodes_path} is incorrect.\n"
        f"Expected:\n{expected_lines}\n"
        f"Got:\n{actual_lines}"
    )

def test_graph_db_exists():
    db_path = "/home/user/graph.db"
    assert os.path.isfile(db_path), f"Expected SQLite database at {db_path} is missing."
    assert os.path.getsize(db_path) > 0, f"SQLite database at {db_path} is empty."