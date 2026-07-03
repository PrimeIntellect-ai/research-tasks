# test_final_state.py

import os
import json
import csv
import heapq
import pytest

def compute_expected_results():
    nodes_path = "/home/user/nodes.csv"
    edges_path = "/home/user/edges.csv"

    if not os.path.exists(nodes_path) or not os.path.exists(edges_path):
        return []

    nodes = {}
    with open(nodes_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            nodes[row['id']] = {'name': row['name'], 'type': row['type']}

    graph = {}
    for node in nodes:
        graph[node] = []

    with open(edges_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            u = row['source']
            v = row['target']
            w = int(row['distance'])
            if u not in graph:
                graph[u] = []
            graph[u].append((v, w))

    # Dijkstra from N001
    distances = {n: float('inf') for n in graph}
    distances['N001'] = 0
    pq = [(0, 'N001')]

    while pq:
        d, u = heapq.heappop(pq)
        if d > distances.get(u, float('inf')):
            continue
        for v, w in graph.get(u, []):
            if distances.get(u, float('inf')) + w < distances.get(v, float('inf')):
                distances[v] = distances[u] + w
                heapq.heappush(pq, (distances[v], v))

    # Filter and format
    results = []
    for node_id, dist in distances.items():
        if node_id in nodes and nodes[node_id]['type'] == 'warehouse' and dist <= 150:
            results.append({
                "id": node_id,
                "name": nodes[node_id]['name'],
                "distance": dist
            })

    # Sort: distance DESC, id ASC
    results.sort(key=lambda x: (-x['distance'], x['id']))

    # Paginate: Page 2, size 3
    page_size = 3
    page_idx = 2
    start = (page_idx - 1) * page_size
    end = start + page_size

    return results[start:end]

def test_results_json():
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"File {results_path} is missing."

    with open(results_path, 'r', encoding='utf-8') as f:
        try:
            actual_results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} does not contain valid JSON.")

    expected_results = compute_expected_results()

    assert actual_results == expected_results, f"Expected results {expected_results}, but got {actual_results}."

def test_cypher_query():
    query_path = "/home/user/query.cypher"
    assert os.path.isfile(query_path), f"File {query_path} is missing."

    with open(query_path, 'r', encoding='utf-8') as f:
        content = f.read().upper()

    required_keywords = [
        "MATCH", "WHERE", "ORDER BY", "DESC", "SKIP 3", "LIMIT 3"
    ]

    for kw in required_keywords:
        assert kw in content, f"Expected keyword '{kw}' missing in {query_path}."

    content_lower = content.lower()
    assert "n001" in content_lower, f"Expected starting node 'N001' missing in {query_path}."
    assert "warehouse" in content_lower, f"Expected node type 'warehouse' missing in {query_path}."
    assert "150" in content_lower, f"Expected distance limit '150' missing in {query_path}."