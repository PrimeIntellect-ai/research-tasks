# test_final_state.py
import os
import json
import csv
import sqlite3
import pytest
from collections import deque

def get_expected_data():
    conn = sqlite3.connect('/home/user/data.db')
    c = conn.cursor()

    query = """
    SELECT 
        sender, 
        receiver, 
        amount, 
        timestamp,
        SUM(amount) OVER (PARTITION BY sender ORDER BY timestamp ASC) as cumulative_sent
    FROM transactions
    ORDER BY tx_id ASC
    """
    c.execute(query)
    rows = c.fetchall()
    conn.close()

    return rows

def compute_shortest_path(edges, start_node, end_node):
    graph = {}
    for sender, receiver, _, _, _ in edges:
        if sender not in graph:
            graph[sender] = []
        graph[sender].append(receiver)

    queue = deque([[start_node]])
    visited = set([start_node])

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == end_node:
            return path

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    return None

def test_edges_csv_exists_and_correct():
    csv_path = '/home/user/edges.csv'
    assert os.path.exists(csv_path), f"{csv_path} does not exist."

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        expected_header = ['sender', 'receiver', 'amount', 'timestamp', 'cumulative_sent']
        assert header == expected_header, f"Expected header {expected_header}, got {header}"

        rows = list(reader)

    expected_rows = get_expected_data()
    assert len(rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in CSV, got {len(rows)}"

    # Check data correctness (ignoring order)
    expected_set = set()
    for r in expected_rows:
        expected_set.add((str(r[0]), str(r[1]), float(r[2]), str(r[3]), float(r[4])))

    actual_set = set()
    for r in rows:
        actual_set.add((str(r[0]), str(r[1]), float(r[2]), str(r[3]), float(r[4])))

    assert actual_set == expected_set, "Data in edges.csv does not match expected output."

def test_final_output_json():
    json_path = '/home/user/final_output.json'
    assert os.path.exists(json_path), f"{json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} is not valid JSON.")

    assert "shortest_path" in data, "Key 'shortest_path' missing in final_output.json"
    assert "user_9_max_cumulative_sent" in data, "Key 'user_9_max_cumulative_sent' missing in final_output.json"

    expected_rows = get_expected_data()
    expected_path = compute_shortest_path(expected_rows, 'user_1', 'user_9')

    user_9_cumulative_sents = [r[4] for r in expected_rows if r[0] == 'user_9']
    expected_max_cumulative = max(user_9_cumulative_sents) if user_9_cumulative_sents else 0.0

    assert data["shortest_path"] == expected_path, f"Expected shortest_path {expected_path}, got {data['shortest_path']}"
    assert float(data["user_9_max_cumulative_sent"]) == expected_max_cumulative, f"Expected user_9_max_cumulative_sent {expected_max_cumulative}, got {data['user_9_max_cumulative_sent']}"