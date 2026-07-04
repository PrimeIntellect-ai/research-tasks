# test_final_state.py

import os
import json
import pytest

GRAPH_PATH = '/home/user/graph.json'
RESULTS_PATH = '/home/user/audit_results.json'

def get_expected_results():
    assert os.path.isfile(GRAPH_PATH), f"Missing {GRAPH_PATH}"

    with open(GRAPH_PATH, 'r') as f:
        data = json.load(f)

    nodes = {n['id']: n for n in data.get('nodes', [])}
    edges = data.get('edges', [])

    # Build adjacency
    # (Employee) -[HAS_ROLE]-> (Role)
    has_role = {}
    # (Role) -[HAS_ACCESS]-> (System)
    has_access = {}

    for edge in edges:
        if edge.get('type') == 'HAS_ROLE':
            has_role.setdefault(edge['source'], []).append(edge['target'])
        elif edge.get('type') == 'HAS_ACCESS':
            has_access.setdefault(edge['source'], []).append(edge['target'])

    results = []

    for emp_id, role_ids in has_role.items():
        emp_node = nodes.get(emp_id)
        if not emp_node or emp_node.get('label') != 'Employee':
            continue

        for role_id in role_ids:
            role_node = nodes.get(role_id)
            if not role_node or role_node.get('label') != 'Role':
                continue

            sys_ids = has_access.get(role_id, [])
            for sys_id in sys_ids:
                sys_node = nodes.get(sys_id)
                if not sys_node or sys_node.get('label') != 'System':
                    continue

                if sys_node.get('sensitivity') == 'HIGH':
                    results.append({
                        "employee": emp_node['name'],
                        "system": sys_node['name']
                    })

    # Sort ascending by employee name, then system name
    results.sort(key=lambda x: (x['employee'], x['system']))

    # Pagination: first 5 records
    return results[:5]

def test_audit_results_exists():
    """Check if /home/user/audit_results.json was created."""
    assert os.path.isfile(RESULTS_PATH), f"File {RESULTS_PATH} is missing. Did the script run?"

def test_audit_results_content():
    """Check if the content of /home/user/audit_results.json is correct."""
    assert os.path.isfile(RESULTS_PATH), f"File {RESULTS_PATH} is missing."

    with open(RESULTS_PATH, 'r') as f:
        try:
            actual_results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {RESULTS_PATH} does not contain valid JSON.")

    expected_results = get_expected_results()

    assert isinstance(actual_results, list), f"Expected the results to be a JSON array (list), got {type(actual_results).__name__}"
    assert len(actual_results) == len(expected_results), f"Expected {len(expected_results)} results, got {len(actual_results)}"

    for i, (actual, expected) in enumerate(zip(actual_results, expected_results)):
        assert actual == expected, f"Mismatch at index {i}. Expected {expected}, but got {actual}"