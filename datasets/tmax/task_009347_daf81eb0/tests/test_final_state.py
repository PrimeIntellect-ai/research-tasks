# test_final_state.py

import os
import sqlite3
import pytest
import heapq

DB_PATH = "/home/user/etl_data.db"
RESULT_PATH = "/home/user/aggregation_result.txt"

def get_true_shortest_paths(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id, weight FROM nodes")
    nodes = {row[0]: row[1] for row in cursor.fetchall()}

    cursor.execute("SELECT source, target FROM edges")
    edges = cursor.fetchall()

    adj = {u: [] for u in nodes}
    for u, v in edges:
        if u in adj:
            adj[u].append(v)

    def dijkstra(start):
        dist = {u: float('inf') for u in nodes}
        dist[start] = nodes[start]
        pq = [(nodes[start], start)]

        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v in adj.get(u, []):
                new_d = d + nodes[v]
                if new_d < dist[v]:
                    dist[v] = new_d
                    heapq.heappush(pq, (new_d, v))
        return dist

    shortest_paths = {}
    for start in nodes:
        shortest_paths[start] = dijkstra(start)

    conn.close()
    return shortest_paths

def test_database_updated_correctly():
    """Test that the materialized_paths table is correctly updated."""
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} is missing."

    true_paths = get_true_shortest_paths(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT source, target, total_weight, is_valid FROM materialized_paths")
    rows = cursor.fetchall()

    for source, target, total_weight, is_valid in rows:
        expected_weight = true_paths.get(source, {}).get(target, float('inf'))

        if expected_weight != float('inf'):
            assert is_valid == 1, f"Path {source}->{target} exists but is_valid is not 1."
            assert total_weight == expected_weight, f"Path {source}->{target} weight is {total_weight}, expected {expected_weight}."
        else:
            assert is_valid == 0, f"Path {source}->{target} does not exist but is_valid is not 0."

    conn.close()

def test_aggregation_result_file():
    """Test that the aggregation result file contains the correct sum."""
    assert os.path.exists(RESULT_PATH), f"Result file {RESULT_PATH} is missing."

    with open(RESULT_PATH, "r") as f:
        content = f.read().strip()

    assert content.isdigit(), f"Result file content '{content}' is not a valid integer."

    # Recompute the expected sum based on the database state
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(total_weight) FROM materialized_paths WHERE is_valid = 1")
    expected_sum = cursor.fetchone()[0]
    conn.close()

    assert int(content) == expected_sum, f"Result file contains {content}, expected {expected_sum}."