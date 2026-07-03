# test_final_state.py

import os
import json
import sqlite3
import pytest

DB_PATH = '/home/user/research.db'
SCRIPT_PATH = '/home/user/export_graph.py'
JSON_PATH = '/home/user/coauthorship_graph.json'

def test_script_exists():
    """Test that the export_graph.py script exists."""
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

def test_json_output_exists():
    """Test that the coauthorship_graph.json output file exists."""
    assert os.path.isfile(JSON_PATH), f"Output JSON not found at {JSON_PATH}"

def test_json_content_and_structure():
    """Test that the output JSON has the correct structure and derived data."""
    # Derive expected data from the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    min_citations = 50

    # Get valid papers
    cursor.execute("SELECT id, citations FROM papers WHERE citations >= ?", (min_citations,))
    valid_papers = {row[0]: row[1] for row in cursor.fetchall()}

    # Get authors for valid papers
    paper_authors = {}
    for pid in valid_papers:
        cursor.execute("SELECT author_id FROM paper_authors WHERE paper_id = ?", (pid,))
        paper_authors[pid] = [row[0] for row in cursor.fetchall()]

    # Compute edges
    edges_dict = {}
    valid_author_ids = set()

    for pid, authors in paper_authors.items():
        citations = valid_papers[pid]
        # All pairs of authors
        for i in range(len(authors)):
            for j in range(i + 1, len(authors)):
                a1, a2 = sorted([authors[i], authors[j]])
                valid_author_ids.add(a1)
                valid_author_ids.add(a2)
                pair = (a1, a2)
                edges_dict[pair] = edges_dict.get(pair, 0) + citations

    # Get author details for valid authors
    expected_nodes = []
    if valid_author_ids:
        placeholders = ','.join('?' * len(valid_author_ids))
        cursor.execute(f"SELECT id, name FROM authors WHERE id IN ({placeholders}) ORDER BY id ASC", tuple(valid_author_ids))
        for row in cursor.fetchall():
            expected_nodes.append({"id": row[0], "name": row[1]})

    conn.close()

    expected_edges = []
    for (source, target), weight in sorted(edges_dict.items()):
        expected_edges.append({
            "source": source,
            "target": target,
            "weight": weight
        })

    # Read generated JSON
    with open(JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {JSON_PATH} is not valid JSON.")

    assert "nodes" in data, "JSON missing 'nodes' key."
    assert "edges" in data, "JSON missing 'edges' key."

    nodes = data["nodes"]
    edges = data["edges"]

    # Check sorting of nodes
    node_ids = [n.get("id") for n in nodes]
    assert node_ids == sorted(node_ids), "Nodes are not sorted by id ascending."

    # Check sorting of edges
    edge_pairs = [(e.get("source"), e.get("target")) for e in edges]
    assert edge_pairs == sorted(edge_pairs), "Edges are not sorted by source ascending, then target ascending."

    # Check source < target constraint
    for e in edges:
        assert e.get("source") < e.get("target"), f"Edge source must be strictly less than target: {e}"

    # Check exact content
    assert nodes == expected_nodes, f"Nodes mismatch. Expected {expected_nodes}, got {nodes}"
    assert edges == expected_edges, f"Edges mismatch. Expected {expected_edges}, got {edges}"