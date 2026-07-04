# test_final_state.py

import csv
import json
import os
import heapq
import pytest

def compute_expected_summary():
    nodes = {}
    with open('/home/user/nodes.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            nodes[row['id']] = int(row['cost'])

    edges = {}
    with open('/home/user/edges.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            src = row['src']
            dst = row['dst']
            weight = int(row['weight'])
            if src not in edges:
                edges[src] = []
            edges[src].append((dst, weight))

    # Dijkstra's algorithm
    distances = {'ROOT': 0}
    pq = [(0, 'ROOT')]
    while pq:
        dist, current = heapq.heappop(pq)
        if dist > distances.get(current, float('inf')):
            continue
        for neighbor, weight in edges.get(current, []):
            new_dist = dist + weight
            if new_dist < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))

    # Filter reachable nodes and sort by distance ASC, id ASC
    reachable = []
    for node, dist in distances.items():
        reachable.append({
            'id': node,
            'distance': dist,
            'cost': nodes[node]
        })

    reachable.sort(key=lambda x: (x['distance'], x['id']))

    # Compute cumulative cost
    cumulative_cost = 0
    for node in reachable:
        cumulative_cost += node['cost']
        node['cumulative_cost'] = cumulative_cost

    # Compute cost rank partitioned by distance
    distance_groups = {}
    for node in reachable:
        distance_groups.setdefault(node['distance'], []).append(node)

    for dist, group in distance_groups.items():
        # Sort group by cost DESC to compute rank
        group_sorted = sorted(group, key=lambda x: x['cost'], reverse=True)
        ranks = {}
        rank = 1
        for j, n in enumerate(group_sorted):
            if j > 0 and n['cost'] < group_sorted[j-1]['cost']:
                rank = j + 1
            ranks[n['id']] = rank

        for n in group:
            n['cost_rank'] = ranks[n['id']]

    return reachable

def test_summary_json_exists():
    """Test that the summary.json file was created."""
    assert os.path.isfile("/home/user/summary.json"), "/home/user/summary.json is missing. The Go program did not produce the expected output file."

def test_summary_json_content():
    """Test that summary.json contains the correct data and structure."""
    expected_data = compute_expected_summary()

    with open("/home/user/summary.json", "r") as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/home/user/summary.json is not a valid JSON file.")

    assert isinstance(actual_data, list), "The JSON output should be an array of objects."
    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} reachable nodes, but got {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual.get("id") == expected["id"], f"Record {i}: Expected id '{expected['id']}', got '{actual.get('id')}'"
        assert actual.get("distance") == expected["distance"], f"Record {i} ({expected['id']}): Expected distance {expected['distance']}, got {actual.get('distance')}"
        assert actual.get("cost") == expected["cost"], f"Record {i} ({expected['id']}): Expected cost {expected['cost']}, got {actual.get('cost')}"
        assert actual.get("cumulative_cost") == expected["cumulative_cost"], f"Record {i} ({expected['id']}): Expected cumulative_cost {expected['cumulative_cost']}, got {actual.get('cumulative_cost')}"
        assert actual.get("cost_rank") == expected["cost_rank"], f"Record {i} ({expected['id']}): Expected cost_rank {expected['cost_rank']}, got {actual.get('cost_rank')}"