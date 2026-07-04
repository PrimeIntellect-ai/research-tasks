# test_final_state.py
import os
import sqlite3
from collections import defaultdict

def get_expected_deadlocks(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT waiting_tx, blocking_tx FROM waits_for")
    edges = cursor.fetchall()
    conn.close()

    graph = defaultdict(list)
    nodes = set()
    for u, v in edges:
        graph[u].append(v)
        nodes.add(u)
        nodes.add(v)

    # Tarjan's algorithm for Strongly Connected Components (SCC)
    index = 0
    indices = {}
    lowlinks = {}
    stack = []
    on_stack = set()
    sccs = []

    def strongconnect(v):
        nonlocal index
        indices[v] = index
        lowlinks[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)

        for w in graph[v]:
            if w not in indices:
                strongconnect(w)
                lowlinks[v] = min(lowlinks[v], lowlinks[w])
            elif w in on_stack:
                lowlinks[v] = min(lowlinks[v], indices[w])

        if lowlinks[v] == indices[v]:
            scc = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                scc.append(w)
                if w == v:
                    break
            sccs.append(scc)

    for v in nodes:
        if v not in indices:
            strongconnect(v)

    deadlocked = set()
    for scc in sccs:
        if len(scc) > 1:
            deadlocked.update(scc)
        elif len(scc) == 1:
            # Check for self-loop
            v = scc[0]
            if v in graph[v]:
                deadlocked.add(v)

    return sorted(list(deadlocked))

def test_script_exists_and_executable():
    script_path = '/home/user/detect_deadlocks.sh'
    assert os.path.exists(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

def test_output_file_correctness():
    db_path = '/home/user/locks.db'
    output_path = '/home/user/deadlocked_txs.txt'

    assert os.path.exists(output_path), f"Output file not found at {output_path}"

    expected_deadlocks = get_expected_deadlocks(db_path)

    with open(output_path, 'r') as f:
        lines = f.read().splitlines()

    actual_deadlocks = []
    for line in lines:
        line = line.strip()
        if line:
            try:
                actual_deadlocks.append(int(line))
            except ValueError:
                assert False, f"Output file contains non-integer value: {line}"

    assert actual_deadlocks == expected_deadlocks, (
        f"Deadlocked transactions do not match expected.\n"
        f"Expected: {expected_deadlocks}\n"
        f"Actual: {actual_deadlocks}"
    )