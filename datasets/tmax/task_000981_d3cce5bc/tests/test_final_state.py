# test_final_state.py
import os
import json
import sqlite3
import pytest
from collections import deque

def get_expected_data():
    db_path = "/home/user/ecommerce.db"
    assert os.path.exists(db_path), "Database file is missing."

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Build graph
    c.execute("SELECT referrer_id, referred_id FROM referrals")
    referrals = c.fetchall()

    graph = {}
    for u, v in referrals:
        if u not in graph:
            graph[u] = []
        graph[u].append(v)

    # BFS to find users within 2 hops from user 1
    queue = deque([(1, 0)])
    visited = {1}
    valid_users = {1}

    while queue:
        curr, dist = queue.popleft()
        if dist < 2:
            for neighbor in graph.get(curr, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    valid_users.add(neighbor)
                    queue.append((neighbor, dist + 1))

    # Query expected sums
    placeholders = ",".join(["?"] * len(valid_users))
    query = f"""
        SELECT u.id, u.name, ROUND(SUM(t.amount), 2)
        FROM users u
        INNER JOIN transactions t ON u.id = t.user_id
        WHERE u.id IN ({placeholders})
        GROUP BY u.id, u.name
        ORDER BY u.id ASC
    """
    c.execute(query, list(valid_users))
    results = c.fetchall()
    conn.close()

    expected_output = []
    for row in results:
        expected_output.append({
            "user_id": row[0],
            "name": row[1],
            "total_spent": row[2]
        })

    return expected_output

def test_final_report_exists_and_correct():
    report_path = "/home/user/final_report.json"
    assert os.path.exists(report_path), f"Expected report file {report_path} was not found."

    with open(report_path, "r") as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The file final_report.json does not contain valid JSON.")

    expected_data = get_expected_data()

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} records, found {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual.get("user_id") == expected["user_id"], f"Record {i} user_id mismatch: expected {expected['user_id']}, got {actual.get('user_id')}"
        assert actual.get("name") == expected["name"], f"Record {i} name mismatch: expected {expected['name']}, got {actual.get('name')}"
        assert isinstance(actual.get("total_spent"), float), f"Record {i} total_spent should be a float."
        assert abs(actual.get("total_spent") - expected["total_spent"]) < 0.01, f"Record {i} total_spent mismatch: expected {expected['total_spent']}, got {actual.get('total_spent')}"

def test_script_uses_parameterized_queries():
    script_path = "/home/user/etl_pipeline.py"
    assert os.path.exists(script_path), f"Script file {script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read()

    # Ensure no f-string or .format is used to inject the user IDs directly
    # A basic check to see if '?' is used for the IN clause
    assert "?" in content, "The script does not appear to use parameterized queries (missing '?')."
    assert "user_ids_str" not in content or "f\"\"\"" not in content or "{user_ids_str}" not in content, "The script still uses unsafe string formatting for the SQL query."