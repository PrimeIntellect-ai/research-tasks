# test_final_state.py

import os
import sqlite3
import json
import pytest

def test_phase1_index_created():
    db_path = "/home/user/logistics.db"
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if an index exists on deliveries table for duration_hours
    cursor.execute("PRAGMA index_list('deliveries');")
    indexes = cursor.fetchall()

    index_found = False
    for idx in indexes:
        idx_name = idx[1]
        cursor.execute(f"PRAGMA index_info('{idx_name}');")
        columns = cursor.fetchall()
        for col in columns:
            if col[2] == 'duration_hours':
                index_found = True
                break
        if index_found:
            break

    conn.close()
    assert index_found, "Optimal index on deliveries.duration_hours was not created."

def test_phase1_query_plan():
    plan_path = "/home/user/query_plan.txt"
    assert os.path.isfile(plan_path), f"Query plan file {plan_path} is missing."

    with open(plan_path, 'r') as f:
        content = f.read().upper()

    assert "USING INDEX" in content and "DELIVERIES" in content, \
        "The query plan does not indicate that an index on the deliveries table was used."

def test_phase2_slow_hubs():
    jsonl_path = "/home/user/events.jsonl"
    csv_path = "/home/user/slow_hubs.csv"

    assert os.path.isfile(jsonl_path), f"{jsonl_path} is missing."
    assert os.path.isfile(csv_path), f"{csv_path} is missing."

    # Recompute truth
    hub_times = {}
    hub_counts = {}
    with open(jsonl_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)
            hid = data['hub_id']
            ts = data['time_spent']
            hub_times[hid] = hub_times.get(hid, 0.0) + ts
            hub_counts[hid] = hub_counts.get(hid, 0) + 1

    expected_slow_hubs = []
    for hid in sorted(hub_times.keys()):
        avg = hub_times[hid] / hub_counts[hid]
        if avg > 10.0:
            expected_slow_hubs.append(f"{hid},{avg:.2f}")

    with open(csv_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_slow_hubs, \
        f"slow_hubs.csv content is incorrect. Expected: {expected_slow_hubs}, Got: {actual_lines}"

def test_phase3_slow_graph():
    db_path = "/home/user/logistics.db"
    csv_path = "/home/user/slow_graph.csv"
    jsonl_path = "/home/user/events.jsonl"

    assert os.path.isfile(db_path), f"{db_path} is missing."
    assert os.path.isfile(csv_path), f"{csv_path} is missing."

    # Recompute slow hubs
    hub_times = {}
    hub_counts = {}
    with open(jsonl_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)
            hid = data['hub_id']
            ts = data['time_spent']
            hub_times[hid] = hub_times.get(hid, 0.0) + ts
            hub_counts[hid] = hub_counts.get(hid, 0) + 1

    slow_hubs = set()
    for hid, total_time in hub_times.items():
        if (total_time / hub_counts[hid]) > 10.0:
            slow_hubs.add(hid)

    # Recompute graph
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT src_hub, dst_hub, distance FROM routes;")
    routes = cursor.fetchall()
    conn.close()

    expected_graph = []
    for src, dst, dist in routes:
        if src in slow_hubs and dst in slow_hubs:
            expected_graph.append((src, dst, dist))

    expected_graph.sort(key=lambda x: (x[0], x[1]))
    expected_lines = [f"{src},{dst},{dist}" for src, dst, dist in expected_graph]

    with open(csv_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, \
        f"slow_graph.csv content is incorrect. Expected: {expected_lines}, Got: {actual_lines}"