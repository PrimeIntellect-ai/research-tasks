# test_final_state.py

import os
import csv
import sqlite3
import pytest

CSV_PATH = "/home/user/hubs.csv"
DB_PATH = "/home/user/kg_data.db"
TIMESTAMP = 1700000000

def get_expected_hubs():
    if not os.path.exists(DB_PATH):
        pytest.fail(f"Database file {DB_PATH} is missing. Cannot compute expected results.")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Identify active nodes at TIMESTAMP
    c.execute("SELECT id, label FROM nodes WHERE valid_from <= ? AND valid_to > ?", (TIMESTAMP, TIMESTAMP))
    active_nodes = {row['id']: row['label'] for row in c.fetchall()}

    # Identify active edges at TIMESTAMP
    c.execute("SELECT source_id, target_id FROM edges WHERE valid_from <= ? AND valid_to > ?", (TIMESTAMP, TIMESTAMP))

    in_degree = {n: 0 for n in active_nodes}
    out_degree = {n: 0 for n in active_nodes}

    for row in c.fetchall():
        src = row['source_id']
        tgt = row['target_id']
        # An edge is only valid if both source and target are active
        if src in active_nodes and tgt in active_nodes:
            out_degree[src] += 1
            in_degree[tgt] += 1

    conn.close()

    hubs = []
    for n, label in active_nodes.items():
        total = in_degree[n] + out_degree[n]
        if total >= 3:
            hubs.append({
                'node_id': n,
                'label': label,
                'in_degree': in_degree[n],
                'out_degree': out_degree[n],
                'total_degree': total
            })

    # Sort primarily by total_degree DESC, secondarily by node_id ASC
    hubs.sort(key=lambda x: (-x['total_degree'], x['node_id']))
    return hubs

def test_hubs_csv_exists():
    assert os.path.exists(CSV_PATH), f"Expected output file {CSV_PATH} was not found."
    assert os.path.isfile(CSV_PATH), f"{CSV_PATH} is not a valid file."

def test_hubs_csv_contents():
    if not os.path.exists(CSV_PATH):
        pytest.fail(f"Cannot test contents because {CSV_PATH} does not exist.")

    expected_hubs = get_expected_hubs()

    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail(f"{CSV_PATH} is empty.")

        expected_header = ['node_id', 'label', 'in_degree', 'out_degree', 'total_degree']
        assert header == expected_header, f"CSV header is incorrect. Expected {expected_header}, got {header}"

        actual_rows = list(reader)

    assert len(actual_rows) == len(expected_hubs), \
        f"Expected {len(expected_hubs)} hub nodes, but found {len(actual_rows)} in the CSV."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_hubs)):
        try:
            actual_node_id = int(actual[0])
            actual_label = actual[1]
            actual_in = int(actual[2])
            actual_out = int(actual[3])
            actual_total = int(actual[4])
        except (ValueError, IndexError) as e:
            pytest.fail(f"Row {i+1} is malformed: {actual}. Error: {e}")

        assert actual_node_id == expected['node_id'], f"Row {i+1}: expected node_id {expected['node_id']}, got {actual_node_id}"
        assert actual_label == expected['label'], f"Row {i+1}: expected label {expected['label']}, got {actual_label}"
        assert actual_in == expected['in_degree'], f"Row {i+1} (Node {actual_node_id}): expected in_degree {expected['in_degree']}, got {actual_in}"
        assert actual_out == expected['out_degree'], f"Row {i+1} (Node {actual_node_id}): expected out_degree {expected['out_degree']}, got {actual_out}"
        assert actual_total == expected['total_degree'], f"Row {i+1} (Node {actual_node_id}): expected total_degree {expected['total_degree']}, got {actual_total}"