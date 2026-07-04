# test_final_state.py

import os
import json
import sqlite3
import heapq
import pytest

def get_expected_restore_order():
    db_path = '/home/user/backups.sqlite'
    json_path = '/home/user/services.json'

    assert os.path.isfile(db_path), f"Database {db_path} is missing."
    assert os.path.isfile(json_path), f"JSON file {json_path} is missing."

    # 1. Get failed services
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT service_id FROM backups WHERE status = 'FAILED'")
    failed_services = set(row[0] for row in c.fetchall())
    conn.close()

    # 2. Get dependencies
    with open(json_path, 'r') as f:
        services_data = json.load(f)

    # 3. Build graph
    adj = {svc: [] for svc in failed_services}
    in_degree = {svc: 0 for svc in failed_services}

    for item in services_data:
        svc = item['service_id']
        if svc not in failed_services:
            continue
        for dep in item['depends_on']:
            if dep in failed_services:
                adj[dep].append(svc)
                in_degree[svc] += 1

    # 4. Topological sort with alphabetical tie-breaking
    pq = []
    for svc in failed_services:
        if in_degree[svc] == 0:
            heapq.heappush(pq, svc)

    restore_order = []
    while pq:
        curr = heapq.heappop(pq)
        restore_order.append(curr)
        for neighbor in adj[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                heapq.heappush(pq, neighbor)

    return restore_order

def test_restore_order_json_exists():
    output_path = '/home/user/restore_order.json'
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

def test_restore_order_json_content():
    output_path = '/home/user/restore_order.json'
    expected_order = get_expected_restore_order()

    with open(output_path, 'r') as f:
        try:
            actual_order = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_path} is not valid JSON.")

    assert isinstance(actual_order, list), "The output JSON must be a list of strings."
    assert actual_order == expected_order, (
        f"Restoration order is incorrect.\n"
        f"Expected: {expected_order}\n"
        f"Actual:   {actual_order}"
    )

def test_restore_plan_script_exists():
    script_path = '/home/user/restore_plan.py'
    assert os.path.isfile(script_path), f"Python script {script_path} does not exist."