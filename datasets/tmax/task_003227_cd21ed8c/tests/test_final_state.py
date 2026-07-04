# test_final_state.py

import os
import json
import pytest

NODES_PATH = '/home/user/graph/nodes.jsonl'
EDGES_PATH = '/home/user/graph/edges.jsonl'
TARGET_PATH = '/home/user/target_customers.txt'

def test_nodes_file():
    """Test that nodes.jsonl exists and contains the correct number and format of nodes."""
    assert os.path.isfile(NODES_PATH), f"Nodes file missing at {NODES_PATH}"

    nodes = []
    with open(NODES_PATH, 'r') as f:
        for line in f:
            if line.strip():
                nodes.append(json.loads(line))

    assert len(nodes) == 9, f"Expected 9 nodes, found {len(nodes)}"

    customers = [n for n in nodes if n.get('type') == 'customer']
    items = [n for n in nodes if n.get('type') == 'item']

    assert len(customers) == 5, f"Expected 5 customer nodes, found {len(customers)}"
    assert len(items) == 4, f"Expected 4 item nodes, found {len(items)}"

    # Check prefixes
    for c in customers:
        assert c['id'].startswith('c_'), f"Customer ID {c['id']} does not start with 'c_'"
        assert 'properties' in c, "Customer node missing 'properties'"
        assert 'name' in c['properties'], "Customer properties missing 'name'"

    for i in items:
        assert i['id'].startswith('i_'), f"Item ID {i['id']} does not start with 'i_'"
        assert 'properties' in i, "Item node missing 'properties'"
        assert 'name' in i['properties'], "Item properties missing 'name'"

def test_edges_file():
    """Test that edges.jsonl exists and contains the correct number and format of edges."""
    assert os.path.isfile(EDGES_PATH), f"Edges file missing at {EDGES_PATH}"

    edges = []
    with open(EDGES_PATH, 'r') as f:
        for line in f:
            if line.strip():
                edges.append(json.loads(line))

    assert len(edges) == 11, f"Expected 11 edges (5 purchases + 6 ratings), found {len(edges)}"

    purchases = [e for e in edges if e.get('type') == 'PURCHASED']
    ratings = [e for e in edges if e.get('type') == 'RATED']

    assert len(purchases) == 5, f"Expected 5 PURCHASED edges, found {len(purchases)}"
    assert len(ratings) == 6, f"Expected 6 RATED edges, found {len(ratings)}"

    for e in edges:
        assert 'src' in e, "Edge missing 'src'"
        assert 'dst' in e, "Edge missing 'dst'"
        assert e['src'].startswith('c_'), f"Edge src {e['src']} should be a customer ID"
        assert e['dst'].startswith('i_'), f"Edge dst {e['dst']} should be an item ID"
        assert 'properties' in e, "Edge missing 'properties'"

def test_target_customers():
    """Test that target_customers.txt contains the correct output."""
    assert os.path.isfile(TARGET_PATH), f"Target output file missing at {TARGET_PATH}"

    with open(TARGET_PATH, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in target_customers.txt, found {len(lines)}"
    assert lines[0] == 'Alice', f"Expected first line to be 'Alice', got '{lines[0]}'"
    assert lines[1] == 'Diana', f"Expected second line to be 'Diana', got '{lines[1]}'"