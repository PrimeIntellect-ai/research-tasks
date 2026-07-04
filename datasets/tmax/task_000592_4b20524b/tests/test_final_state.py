# test_final_state.py

import os
import json
import csv
import pytest
from collections import deque

def test_path_summary_json():
    """Test that the output JSON file exists, is valid, and contains the correct shortest path and total salary."""
    csv_path = "/home/user/employees.csv"
    json_path = "/home/user/path_summary.json"

    assert os.path.isfile(json_path), f"Output file {json_path} does not exist. Did the script run successfully?"

    # Recompute the ground truth from the CSV file
    adj = {}
    salaries = {}

    assert os.path.isfile(csv_path), f"Input file {csv_path} is missing."
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            emp = row['emp_id']
            mgr = row['manager_id']
            salaries[emp] = int(row['salary'])
            if emp not in adj:
                adj[emp] = []
            if mgr:
                if mgr not in adj:
                    adj[mgr] = []
                adj[emp].append(mgr)
                adj[mgr].append(emp)

    # BFS to find the shortest path
    start = "EMP-012"
    end = "EMP-007"
    queue = deque([[start]])
    visited = set([start])

    expected_path = None
    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == end:
            expected_path = path
            break

        for neighbor in adj.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    assert expected_path is not None, f"Could not find a path between {start} and {end}."

    expected_salary = sum(salaries[node] for node in expected_path)

    # Read and validate the output JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            result = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert "path" in result, "JSON is missing the 'path' key."
    assert "total_salary" in result, "JSON is missing the 'total_salary' key."

    actual_path = result["path"]
    actual_salary = result["total_salary"]

    assert isinstance(actual_path, list), "'path' must be a list of employee IDs."

    # The prompt asks for the path between EMP-012 and EMP-007. We will accept either direction.
    assert actual_path == expected_path or actual_path == expected_path[::-1], \
        f"Expected path {expected_path} (or reverse), but got {actual_path}."

    assert actual_salary == expected_salary, \
        f"Expected total_salary of {expected_salary}, but got {actual_salary}."