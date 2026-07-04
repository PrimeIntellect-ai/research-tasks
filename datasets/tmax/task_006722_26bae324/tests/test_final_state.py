# test_final_state.py
import os
import csv
import sqlite3
import heapq
import pytest

DB_PATH = "/home/user/network.db"
C_SOURCE_PATH = "/home/user/analyze_network.c"
EXECUTABLE_PATH = "/home/user/analyze_network"
CSV_PATH = "/home/user/optimized_path_stats.csv"

def get_expected_data(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM nodes")
    nodes = {row['id']: row['hostname'] for row in cur.fetchall()}

    cur.execute("SELECT * FROM edges")
    edges = cur.fetchall()

    gateway_id = next((k for k, v in nodes.items() if v == 'Gateway'), None)
    db_id = next((k for k, v in nodes.items() if v == 'Database'), None)

    if gateway_id is None or db_id is None:
        pytest.fail("Database missing 'Gateway' or 'Database' nodes.")

    queue = [(0, gateway_id, [gateway_id])]
    visited = set()
    shortest_path = []

    while queue:
        cost, curr, path = heapq.heappop(queue)
        if curr == db_id:
            shortest_path = path
            break
        if curr in visited:
            continue
        visited.add(curr)
        for e in edges:
            if e['source_id'] == curr:
                heapq.heappush(queue, (cost + e['latency'], e['target_id'], path + [e['target_id']]))

    cur.execute("SELECT * FROM bandwidth_logs ORDER BY timestamp")
    logs = cur.fetchall()

    expected_csv = []
    for node_id in shortest_path:
        node_logs = [log for log in logs if log['node_id'] == node_id]
        node_logs.sort(key=lambda x: x['timestamp'])

        for i, log in enumerate(node_logs):
            start = max(0, i - 1)
            end = min(len(node_logs), i + 2)
            window = node_logs[start:end]
            avg = sum(w['bytes_transferred'] for w in window) / len(window)

            expected_csv.append([
                str(node_id),
                nodes[node_id],
                log['timestamp'],
                f"{avg:.2f}"
            ])

    conn.close()
    return expected_csv

def test_c_source_exists():
    assert os.path.isfile(C_SOURCE_PATH), f"C source file missing at {C_SOURCE_PATH}"

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE_PATH), f"Compiled executable missing at {EXECUTABLE_PATH}"
    assert os.access(EXECUTABLE_PATH, os.X_OK), f"File at {EXECUTABLE_PATH} is not executable"

def test_csv_output_exists_and_correct():
    assert os.path.isfile(CSV_PATH), f"CSV output file missing at {CSV_PATH}"

    expected_data = get_expected_data(DB_PATH)

    with open(CSV_PATH, 'r', newline='') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail(f"CSV file {CSV_PATH} is empty.")

        expected_header = ['node_id', 'hostname', 'timestamp', 'smoothed_bytes']
        assert header == expected_header, f"CSV header mismatch. Expected {expected_header}, got {header}"

        actual_data = list(reader)

        assert len(actual_data) == len(expected_data), f"CSV row count mismatch. Expected {len(expected_data)} rows, got {len(actual_data)}"

        for i, (actual_row, expected_row) in enumerate(zip(actual_data, expected_data)):
            assert actual_row == expected_row, f"Row {i+1} mismatch. Expected {expected_row}, got {actual_row}"