# test_final_state.py
import os
import json
import sqlite3
import pytest

def test_violations_json_correct():
    violations_path = "/home/user/violations.json"
    assert os.path.exists(violations_path), f"File {violations_path} does not exist."
    assert os.path.isfile(violations_path), f"{violations_path} is not a file."

    # Load graph data
    graph_path = "/home/user/graph.json"
    assert os.path.exists(graph_path), f"File {graph_path} is missing."
    with open(graph_path, 'r') as f:
        graph_data = json.load(f)

    # Compute valid access from graph
    user_roles = {}
    role_resources = {}

    for edge in graph_data.get("edges", []):
        if edge.get("relation") == "HAS_ROLE":
            user_roles.setdefault(edge["source"], set()).add(edge["target"])
        elif edge.get("relation") == "CAN_ACCESS":
            role_resources.setdefault(edge["source"], set()).add(edge["target"])

    valid_access = set()
    for user, roles in user_roles.items():
        for role in roles:
            for resource in role_resources.get(role, set()):
                valid_access.add((user, resource))

    # Load reported access from DB
    db_path = "/home/user/audit.db"
    assert os.path.exists(db_path), f"File {db_path} is missing."

    reported_access = set()
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, resource_id FROM reported_access")
        for row in cursor.fetchall():
            reported_access.add((row[0], row[1]))
    finally:
        conn.close()

    # Compute expected violations
    violations = reported_access - valid_access
    expected_violations = [
        {"user_id": user, "resource_id": resource}
        for user, resource in violations
    ]
    # Sort by user_id, then resource_id
    expected_violations.sort(key=lambda x: (x["user_id"], x["resource_id"]))

    # Load actual violations
    try:
        with open(violations_path, 'r') as f:
            actual_violations = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"{violations_path} does not contain valid JSON.")

    # Ensure it's a list
    assert isinstance(actual_violations, list), f"Expected a JSON array in {violations_path}."

    # Compare
    assert actual_violations == expected_violations, (
        f"Violations mismatch. Expected: {expected_violations}, Got: {actual_violations}"
    )