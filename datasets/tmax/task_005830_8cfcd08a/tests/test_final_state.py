# test_final_state.py
import os
import json
import sqlite3
from collections import defaultdict

def test_restore_plan_json_exists_and_correct():
    json_path = "/home/user/restore_plan.json"
    assert os.path.exists(json_path), f"File {json_path} does not exist. The script must create this file."
    assert os.path.isfile(json_path), f"{json_path} is not a file."

    db_path = "/home/user/backup_meta.db"
    assert os.path.exists(db_path), f"Database {db_path} is missing."

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Target parameters based on the prompt
    target_db_name = "db_alpha"
    target_timestamp = 1690000050

    cursor.execute('''
        SELECT id FROM backups 
        WHERE db_name = ? AND timestamp <= ? 
        ORDER BY timestamp DESC, id DESC LIMIT 1
    ''', (target_db_name, target_timestamp))
    row = cursor.fetchone()
    assert row is not None, "Could not find target backup in database."
    target_id = row['id']

    # Fetch all backups to memory
    cursor.execute('SELECT id, timestamp, file_path FROM backups')
    backups = {r['id']: dict(r) for r in cursor.fetchall()}

    # Fetch all dependencies
    cursor.execute('SELECT backup_id, depends_on_id FROM dependencies')
    deps = cursor.fetchall()

    # Build graph
    # depends_on_id -> backup_id (edges go from dependency to dependent)
    adj = defaultdict(list)
    rev_adj = defaultdict(list)
    for b_id, dep_id in deps:
        adj[dep_id].append(b_id)
        rev_adj[b_id].append(dep_id)

    # Find all required nodes (ancestors of target_id + target_id itself)
    required_nodes = set()
    stack = [target_id]
    while stack:
        curr = stack.pop()
        if curr not in required_nodes:
            required_nodes.add(curr)
            stack.extend(rev_adj[curr])

    # Compute in-degrees for required nodes
    in_degree = {node: 0 for node in required_nodes}
    for node in required_nodes:
        for dep in rev_adj[node]:
            if dep in required_nodes:
                in_degree[node] += 1

    # Topological sort
    available = [node for node in required_nodes if in_degree[node] == 0]
    result_ids = []

    while available:
        # Sort by timestamp ASC, then id ASC
        available.sort(key=lambda x: (backups[x]['timestamp'], x))
        curr = available.pop(0)
        result_ids.append(curr)

        for child in adj[curr]:
            if child in required_nodes:
                in_degree[child] -= 1
                if in_degree[child] == 0:
                    available.append(child)

    expected_paths = [backups[node]['file_path'] for node in result_ids]

    with open(json_path, 'r') as f:
        try:
            actual_paths = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_path} is not valid JSON."

    assert isinstance(actual_paths, list), f"Expected a JSON array in {json_path}."
    assert actual_paths == expected_paths, (
        f"Restoration plan is incorrect.\n"
        f"Expected: {expected_paths}\n"
        f"Got:      {actual_paths}"
    )

def test_script_exists():
    script_path = "/home/user/generate_plan.py"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."