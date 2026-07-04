# test_final_state.py

import os
import stat
import sqlite3
import pytest

SCRIPT_PATH = "/home/user/analyze_fks.sh"
LOG_PATH = "/home/user/deadlock_risk.log"
DB_PATH = "/home/user/legacy_system.db"

def test_script_exists_and_executable():
    """Verify that the bash script exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable by the user."

def get_sccs(graph):
    """Find strongly connected components using Tarjan's algorithm."""
    index_counter = [0]
    index = {}
    lowlink = {}
    stack = []
    on_stack = set()
    sccs = []

    def strongconnect(node):
        index[node] = index_counter[0]
        lowlink[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)
        on_stack.add(node)

        for w in graph.get(node, []):
            if w not in index:
                strongconnect(w)
                lowlink[node] = min(lowlink[node], lowlink[w])
            elif w in on_stack:
                lowlink[node] = min(lowlink[node], index[w])

        if lowlink[node] == index[node]:
            scc = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                scc.append(w)
                if w == node:
                    break
            sccs.append(scc)

    for v in graph:
        if v not in index:
            strongconnect(v)

    return sccs

def test_log_file_contents():
    """Verify that the log file contains the correctly computed cycles and row counts."""
    assert os.path.isfile(LOG_PATH), f"Log file not found at {LOG_PATH}"

    # Derive the expected output directly from the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]

    graph = {t: [] for t in tables}
    for t in tables:
        cursor.execute(f"PRAGMA foreign_key_list('{t}');")
        fks = cursor.fetchall()
        for fk in fks:
            # fk[2] is the referenced table
            ref_table = fk[2]
            if ref_table:
                graph[t].append(ref_table)

    sccs = get_sccs(graph)
    # A cycle must be > 1 node, or 1 node with a self-reference
    cycles = [scc for scc in sccs if len(scc) > 1 or (len(scc) == 1 and scc[0] in graph.get(scc[0], []))]

    expected_lines = []
    for cycle in cycles:
        cycle_sorted = sorted(cycle)
        total_rows = 0
        for t in cycle:
            cursor.execute(f"SELECT COUNT(*) FROM {t};")
            total_rows += cursor.fetchone()[0]

        cycle_str = ",".join(cycle_sorted)
        expected_lines.append(f"Cycle: {cycle_str} | Total Rows: {total_rows}")

    expected_lines.sort()
    conn.close()

    # Read the actual output
    with open(LOG_PATH, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    actual_lines.sort()

    assert actual_lines == expected_lines, (
        f"Log file contents do not match expected results.\n"
        f"Expected:\n{expected_lines}\n"
        f"Got:\n{actual_lines}"
    )