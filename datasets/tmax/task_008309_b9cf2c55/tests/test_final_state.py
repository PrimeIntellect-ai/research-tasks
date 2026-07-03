# test_final_state.py

import os
import json
import sqlite3
import pytest

DB_PATH = '/home/user/audit.db'
SCRIPT_PATH = '/home/user/find_cycles.py'
OUTPUT_PATH = '/home/user/violators.json'

def get_expected_violators():
    """Derive the expected violators directly from the database."""
    if not os.path.exists(DB_PATH):
        pytest.fail(f"Database file {DB_PATH} is missing.")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT document FROM logs")
    rows = cursor.fetchall()
    conn.close()

    graph = {}
    for (doc_str,) in rows:
        try:
            doc = json.loads(doc_str)
            if doc.get("type") == "approval":
                details = doc.get("details", {})
                req = details.get("requester")
                app = details.get("approver")
                if req and app:
                    if req not in graph:
                        graph[req] = []
                    graph[req].append(app)
                    if app not in graph:
                        graph[app] = []
        except Exception:
            pass

    # Find Strongly Connected Components (Tarjan's algorithm)
    index_counter = [0]
    stack = []
    lowlink = {}
    index = {}
    cyclic_users = []

    def strongconnect(node):
        index[node] = index_counter[0]
        lowlink[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)

        for w in graph.get(node, []):
            if w not in index:
                strongconnect(w)
                lowlink[node] = min(lowlink[node], lowlink[w])
            elif w in stack:
                lowlink[node] = min(lowlink[node], index[w])

        if lowlink[node] == index[node]:
            scc = []
            while True:
                w = stack.pop()
                scc.append(w)
                if w == node:
                    break
            # A cycle exists if SCC has > 1 node, or 1 node with a self-loop
            if len(scc) > 1 or (node in graph.get(node, [])):
                cyclic_users.extend(scc)

    for v in graph:
        if v not in index:
            strongconnect(v)

    return sorted(list(set(cyclic_users)))

def test_script_exists():
    """Test that the python script was created."""
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."

def test_output_exists():
    """Test that the output JSON file was created."""
    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} does not exist."

def test_output_content():
    """Test that the output JSON file contains the correct violators."""
    expected = get_expected_violators()

    with open(OUTPUT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {OUTPUT_PATH} is not valid JSON.")

    assert isinstance(data, list), f"Expected a JSON array, got {type(data).__name__}"
    assert data == expected, f"Expected violators {expected}, but got {data}"