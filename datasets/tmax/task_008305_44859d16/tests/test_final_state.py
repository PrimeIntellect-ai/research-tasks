# test_final_state.py
import os
import csv

def get_expected_deadlocks(csv_path):
    held_by = {}
    waiting_for = []

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tx_id = int(row['tx_id'])
            res_id = row['resource_id']
            state = row['lock_state']

            if state == 'HELD':
                held_by[res_id] = tx_id
            elif state == 'WAITING':
                waiting_for.append((tx_id, res_id))

    # Build Wait-For Graph (WFG)
    # Edge from waiter to holder
    graph = {}
    nodes = set()
    for w_tx, res_id in waiting_for:
        nodes.add(w_tx)
        if res_id in held_by:
            h_tx = held_by[res_id]
            nodes.add(h_tx)
            if w_tx not in graph:
                graph[w_tx] = set()
            graph[w_tx].add(h_tx)

    # Find all nodes involved in cycles
    deadlocked = set()
    visited = set()
    rec_stack = set()

    def dfs(node, path):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, path)
            elif neighbor in rec_stack:
                # Cycle detected
                cycle_start_idx = path.index(neighbor)
                for n in path[cycle_start_idx:]:
                    deadlocked.add(n)

        rec_stack.remove(node)
        path.pop()

    for node in list(nodes) + list(held_by.values()):
        if node not in visited:
            dfs(node, [])

    return sorted(list(deadlocked))

def test_detect_deadlocks_c_exists():
    assert os.path.isfile('/home/user/detect_deadlocks.c'), "C source file /home/user/detect_deadlocks.c is missing."

def test_detect_binary_exists():
    assert os.path.isfile('/home/user/detect'), "Compiled binary /home/user/detect is missing."
    assert os.access('/home/user/detect', os.X_OK), "Binary /home/user/detect is not executable."

def test_deadlocks_log_correct():
    log_path = '/home/user/deadlocks.log'
    csv_path = '/home/user/locks.csv'

    assert os.path.isfile(log_path), f"Output file {log_path} is missing."
    assert os.path.isfile(csv_path), f"Input file {csv_path} is missing."

    expected_tx_ids = get_expected_deadlocks(csv_path)

    with open(log_path, 'r') as f:
        lines = f.read().strip().splitlines()

    actual_tx_ids = []
    for line in lines:
        line = line.strip()
        if line:
            try:
                actual_tx_ids.append(int(line))
            except ValueError:
                assert False, f"Invalid non-integer content in {log_path}: '{line}'"

    assert actual_tx_ids == expected_tx_ids, f"Expected deadlocked tx_ids {expected_tx_ids}, but got {actual_tx_ids} in {log_path}."