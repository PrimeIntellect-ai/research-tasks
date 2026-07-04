# test_final_state.py

import os
import json
import csv
import pytest

def get_expected_data(csv_path):
    nodes = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            nodes[int(row['id'])] = {
                'id': int(row['id']),
                'parent_id': int(row['parent_id']) if row['parent_id'] else None,
                'name': row['name'],
                'sales': int(row['sales'])
            }

    # Compute paths
    for node_id, node in nodes.items():
        path = []
        curr = node_id
        while curr is not None:
            path.append(nodes[curr]['name'])
            curr = nodes[curr]['parent_id']
        node['path'] = path[::-1]

    # Compute sibling ranks
    from collections import defaultdict
    siblings = defaultdict(list)
    for node_id, node in nodes.items():
        siblings[node['parent_id']].append(node)

    for parent_id, group in siblings.items():
        # Sort by sales descending, then id ascending
        group.sort(key=lambda x: (-x['sales'], x['id']))
        for rank, node in enumerate(group, start=1):
            nodes[node['id']]['sibling_rank'] = rank

    # Format expected output
    expected = []
    for node_id in sorted(nodes.keys()):
        node = nodes[node_id]
        expected.append({
            'id': node['id'],
            'name': node['name'],
            'sales': node['sales'],
            'path': node['path'],
            'sibling_rank': node['sibling_rank']
        })
    return expected

def test_result_json_exists():
    """Check if /home/user/result.json exists."""
    assert os.path.isfile('/home/user/result.json'), "/home/user/result.json does not exist."

def test_result_json_content():
    """Verify the content of /home/user/result.json against the expected computed data."""
    csv_path = '/home/user/data.csv'
    assert os.path.isfile(csv_path), "Original data.csv is missing."

    expected_data = get_expected_data(csv_path)

    json_path = '/home/user/result.json'
    assert os.path.isfile(json_path), f"File {json_path} is missing."

    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} does not contain valid JSON.")

    assert isinstance(actual_data, list), "The root JSON structure must be a list (array)."
    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} items, got {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert isinstance(actual, dict), f"Item at index {i} is not an object."

        # Check required keys
        for key in ['id', 'name', 'sales', 'path', 'sibling_rank']:
            assert key in actual, f"Item at index {i} is missing key '{key}'."
            assert actual[key] == expected[key], f"Mismatch at index {i} for key '{key}': expected {expected[key]}, got {actual[key]}."