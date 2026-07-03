# test_final_state.py
import os
import csv
import sqlite3
import pytest

CSV_PATH = "/home/user/deadlocks.csv"
DB_PATH = "/home/user/etl_locks.db"

def get_expected_deadlocks():
    if not os.path.exists(DB_PATH):
        return []

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT tx_id, resource_id FROM locks WHERE status='WAITING'")
    waiting = cur.fetchall()

    cur.execute("SELECT tx_id, resource_id FROM locks WHERE status='GRANTED'")
    granted = cur.fetchall()

    resource_holders = {res: tx for tx, res in granted}

    graph = {}
    for tx_wait, res in waiting:
        if res in resource_holders:
            tx_hold = resource_holders[res]
            graph.setdefault(tx_wait, []).append(tx_hold)

    visited = set()
    rec_stack = set()
    deadlocked_txs = set()

    def dfs(node, path):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, path)
            elif neighbor in rec_stack:
                idx = path.index(neighbor)
                for n in path[idx:]:
                    deadlocked_txs.add(n)

        rec_stack.remove(node)
        path.pop()

    for node in list(graph.keys()):
        if node not in visited:
            dfs(node, [])

    if not deadlocked_txs:
        return []

    placeholders = ",".join("?" for _ in deadlocked_txs)
    cur.execute(f"SELECT tx_id, start_time, query FROM transactions WHERE tx_id IN ({placeholders}) ORDER BY start_time ASC", list(deadlocked_txs))

    results = []
    for rank, (tx_id, start_time, query) in enumerate(cur.fetchall(), start=1):
        results.append({
            "tx_id": tx_id,
            "rank": str(rank),
            "query": query
        })

    conn.close()
    return results

def test_csv_exists():
    assert os.path.exists(CSV_PATH), f"Expected output file {CSV_PATH} does not exist."
    assert os.path.isfile(CSV_PATH), f"{CSV_PATH} is not a valid file."

def test_csv_content():
    expected_data = get_expected_deadlocks()

    assert os.path.exists(CSV_PATH), "Cannot test content because CSV is missing."

    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail("CSV file is empty.")

        assert header == ["tx_id", "rank", "query"], f"CSV header is incorrect. Expected ['tx_id', 'rank', 'query'], got {header}"

        rows = list(reader)

    assert len(rows) == len(expected_data), f"Expected {len(expected_data)} rows in CSV, but found {len(rows)}."

    for i, expected_row in enumerate(expected_data):
        actual_row = rows[i]
        assert len(actual_row) == 3, f"Row {i+1} does not have exactly 3 columns: {actual_row}"
        assert actual_row[0] == expected_row["tx_id"], f"Row {i+1} tx_id mismatch. Expected {expected_row['tx_id']}, got {actual_row[0]}"
        assert actual_row[1] == expected_row["rank"], f"Row {i+1} rank mismatch. Expected {expected_row['rank']}, got {actual_row[1]}"
        assert actual_row[2] == expected_row["query"], f"Row {i+1} query mismatch. Expected '{expected_row['query']}', got '{actual_row[2]}'"