# test_final_state.py

import os
import json
import sqlite3
import heapq
import pytest

DB_PATH = "/home/user/backup_network.db"
BACKUP_ID = "BKP-9001"
OUTPUT_FILE = f"/home/user/route_{BACKUP_ID}.json"

def compute_expected_route(db_path, backup_id):
    if not os.path.exists(db_path):
        pytest.fail(f"Database file missing: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT source_dc_id, dest_dc_id FROM pending_backups WHERE backup_id = ?", (backup_id,))
    row = cursor.fetchone()
    if not row:
        pytest.fail(f"Backup ID {backup_id} not found in pending_backups")
    src, dest = row

    cursor.execute("SELECT source_id, dest_id, latency_ms FROM network_links WHERE status = 'UP'")
    links = cursor.fetchall()

    cursor.execute("SELECT id, name FROM datacenters")
    dc_names = dict(cursor.fetchall())
    conn.close()

    graph = {}
    for u, v, w in links:
        graph.setdefault(u, []).append((v, w))

    pq = [(0, src, [src])]
    visited = set()

    while pq:
        dist, current, path = heapq.heappop(pq)

        if current == dest:
            return dist, [dc_names[n] for n in path]

        if current in visited:
            continue
        visited.add(current)

        for neighbor, weight in graph.get(current, []):
            if neighbor not in visited:
                heapq.heappush(pq, (dist + weight, neighbor, path + [neighbor]))

    return None, None

def test_json_output():
    assert os.path.exists(OUTPUT_FILE), f"Expected output file not found: {OUTPUT_FILE}"
    assert os.path.isfile(OUTPUT_FILE), f"{OUTPUT_FILE} is not a file"

    with open(OUTPUT_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {OUTPUT_FILE} does not contain valid JSON")

    expected_latency, expected_path = compute_expected_route(DB_PATH, BACKUP_ID)
    if expected_latency is None:
        pytest.fail("Could not compute a valid path from the database")

    assert "backup_id" in data, "Missing 'backup_id' in JSON output"
    assert data["backup_id"] == BACKUP_ID, f"Expected backup_id '{BACKUP_ID}', got '{data['backup_id']}'"

    assert "total_latency_ms" in data, "Missing 'total_latency_ms' in JSON output"
    assert data["total_latency_ms"] == expected_latency, f"Expected total_latency_ms {expected_latency}, got {data['total_latency_ms']}"

    assert "path" in data, "Missing 'path' in JSON output"
    assert data["path"] == expected_path, f"Expected path {expected_path}, got {data['path']}"