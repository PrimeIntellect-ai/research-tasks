# test_final_state.py

import os
import csv
import stat
from collections import defaultdict
import pytest

def get_expected_audit_report(csv_path):
    adj = defaultdict(list)
    nodes = set()

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Status') == 'WAITING':
                try:
                    u = int(row['WaitingTxID'])
                    v = int(row['HoldingTxID'])
                    adj[u].append(v)
                    nodes.add(u)
                    nodes.add(v)
                except ValueError:
                    continue

    # Tarjan's SCC algorithm to find all nodes in cycles
    index = 0
    indices = {}
    lowlink = {}
    on_stack = set()
    stack = []
    deadlocked = set()

    def strongconnect(v):
        nonlocal index
        indices[v] = index
        lowlink[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)

        for w in adj[v]:
            if w not in indices:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], indices[w])

        if lowlink[v] == indices[v]:
            scc = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                scc.append(w)
                if w == v:
                    break
            if len(scc) > 1 or (len(scc) == 1 and v in adj[v]):
                deadlocked.update(scc)

    for v in nodes:
        if v not in indices:
            strongconnect(v)

    sorted_deadlocked = sorted(list(deadlocked), reverse=True)
    return sorted_deadlocked[:4]

def test_build_and_run_script_exists_and_executable():
    script_path = "/home/user/build_and_run.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable by the user."

def test_c_program_exists():
    c_path = "/home/user/detect_cycles.c"
    assert os.path.exists(c_path), f"C program source {c_path} does not exist."
    assert os.path.isfile(c_path), f"{c_path} is not a file."

def test_audit_report_content():
    report_path = "/home/user/audit_report.txt"
    csv_path = "/home/user/lock_events.csv"

    assert os.path.exists(report_path), f"Audit report {report_path} does not exist."
    assert os.path.isfile(report_path), f"{report_path} is not a file."

    expected_top_4 = get_expected_audit_report(csv_path)
    expected_lines = [str(x) for x in expected_top_4]

    with open(report_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"Audit report contents mismatch. Expected: {expected_lines}, Got: {actual_lines}"