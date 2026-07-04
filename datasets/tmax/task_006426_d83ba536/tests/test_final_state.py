# test_final_state.py

import os
import sqlite3
import json
import pytest

REPORT_PATH = "/home/user/report.txt"
DB_PATH = "/home/user/backups.db"

def get_expected_values():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 1. Total Archived Size
    c.execute("SELECT metadata FROM backup_events")
    total_size = 0
    for row in c.fetchall():
        meta = json.loads(row[0])
        if meta.get("status") == "archived":
            total_size += meta.get("size_bytes", 0)

    # 2. Max Restoration Chain Length
    c.execute("SELECT id, parent_id FROM backup_events")
    edges = c.fetchall()

    children_map = {}
    for node_id, parent_id in edges:
        if parent_id is not None:
            children_map.setdefault(parent_id, []).append(node_id)

    def get_max_depth(node_id):
        if node_id not in children_map:
            return 0
        return 1 + max(get_max_depth(child) for child in children_map[node_id])

    c.execute("SELECT id FROM backup_events WHERE type='full'")
    full_backups = [row[0] for row in c.fetchall()]

    max_chain_length = 0
    if full_backups:
        max_chain_length = max(get_max_depth(fb) for fb in full_backups)

    # 3. Latest Full Backups
    c.execute('''
        SELECT dataset, id 
        FROM backup_events 
        WHERE type='full' 
        ORDER BY timestamp DESC
    ''')
    latest_full = {}
    for dataset, backup_id in c.fetchall():
        if dataset not in latest_full:
            latest_full[dataset] = backup_id

    conn.close()

    return total_size, max_chain_length, latest_full

def test_report_exists():
    assert os.path.isfile(REPORT_PATH), f"Report file {REPORT_PATH} does not exist."

def test_report_content():
    total_size, max_chain, latest_full = get_expected_values()

    expected_lines = [
        f"Total Archived Size: {total_size}",
        f"Max Restoration Chain Length: {max_chain}",
        "Latest Full Backups:"
    ]

    for dataset in sorted(latest_full.keys()):
        expected_lines.append(f"{dataset}: {latest_full[dataset]}")

    expected_content = "\n".join(expected_lines).strip()

    with open(REPORT_PATH, 'r') as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"Report content does not match expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Actual:\n{actual_content}"
    )