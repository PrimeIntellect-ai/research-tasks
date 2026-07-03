# test_final_state.py

import os
import sqlite3
import csv
import pytest

DB_PATH = '/home/user/etl_data.db'
CPP_PATH = '/home/user/process_graph.cpp'
CSV_PATH = '/home/user/impact_page_2.csv'

def compute_expected_page():
    """
    Computes the expected downstream impact scores from the SQLite database
    and returns the expected rows for Page 2.
    """
    if not os.path.exists(DB_PATH):
        pytest.fail(f"Database file {DB_PATH} is missing.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM nodes")
    nodes = {row[0]: row[1] for row in cursor.fetchall()}

    cursor.execute("SELECT source, target FROM edges")
    edges = cursor.fetchall()
    conn.close()

    # Build reverse graph (target -> sources) to find ancestors
    parents = {node_id: [] for node_id in nodes}
    for source, target in edges:
        parents[target].append(source)

    def get_ancestors(node_id):
        visited = set()
        stack = [node_id]
        while stack:
            curr = stack.pop()
            for p in parents[curr]:
                if p not in visited:
                    visited.add(p)
                    stack.append(p)
        return visited

    impacts = []
    for node_id, name in nodes.items():
        score = len(get_ancestors(node_id)) + 1
        impacts.append((node_id, name, score))

    # Sort: Downstream Impact descending, then ID ascending
    impacts.sort(key=lambda x: (-x[2], x[0]))

    # Page 2 (items 5-8), indices 4 to 7
    return impacts[4:8]

def test_cpp_file_exists():
    assert os.path.exists(CPP_PATH), f"C++ source file {CPP_PATH} does not exist."
    assert os.path.isfile(CPP_PATH), f"{CPP_PATH} is not a file."

def test_csv_output_exists():
    assert os.path.exists(CSV_PATH), f"Output file {CSV_PATH} does not exist."
    assert os.path.isfile(CSV_PATH), f"{CSV_PATH} is not a file."

def test_csv_output_contents():
    if not os.path.exists(CSV_PATH):
        pytest.fail(f"Cannot verify contents because {CSV_PATH} does not exist.")

    expected_data = compute_expected_page()

    with open(CSV_PATH, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"CSV file {CSV_PATH} is empty."

    expected_header = ['id', 'name', 'impact_score']
    assert rows[0] == expected_header, f"Invalid CSV header. Expected {expected_header}, got {rows[0]}."

    data_rows = rows[1:]
    assert len(data_rows) == len(expected_data), f"Expected {len(expected_data)} rows of data, got {len(data_rows)}."

    for i, (exp_id, exp_name, exp_score) in enumerate(expected_data):
        actual_id, actual_name, actual_score = data_rows[i]

        assert int(actual_id) == exp_id, f"Row {i+1}: expected id {exp_id}, got {actual_id}."
        assert actual_name == exp_name, f"Row {i+1}: expected name '{exp_name}', got '{actual_name}'."
        assert int(actual_score) == exp_score, f"Row {i+1}: expected impact_score {exp_score}, got {actual_score}."