# test_final_state.py

import os
import sqlite3
import json
import re
import pytest
from collections import defaultdict

def get_subgraph_members(ttl_path, manager):
    if not os.path.exists(ttl_path):
        pytest.fail(f"RDF file missing: {ttl_path}")

    with open(ttl_path, 'r') as f:
        content = f.read()

    # Simple regex to parse triples like: ex:Alice ex:manages ex:Bob .
    pattern = re.compile(r'ex:(\w+)\s+ex:manages\s+ex:(\w+)\s*\.')

    graph = defaultdict(list)
    for match in pattern.finditer(content):
        mgr, sub = match.groups()
        graph[mgr].append(sub)

    members = set([manager])
    queue = [manager]

    while queue:
        current = queue.pop(0)
        for sub in graph.get(current, []):
            if sub not in members:
                members.add(sub)
                queue.append(sub)

    return sorted(list(members))

def get_expected_rolling_avg(db_path, members):
    if not os.path.exists(db_path):
        pytest.fail(f"Database file missing: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    WITH RollingData AS (
        SELECT employee_name, sale_date,
               AVG(amount) OVER (
                   PARTITION BY employee_name 
                   ORDER BY sale_date 
                   ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
               ) as rolling_avg
        FROM transactions
    ),
    LatestData AS (
        SELECT employee_name, rolling_avg,
               ROW_NUMBER() OVER (
                   PARTITION BY employee_name 
                   ORDER BY sale_date DESC
               ) as rn
        FROM RollingData
    )
    SELECT employee_name, rolling_avg
    FROM LatestData
    WHERE rn = 1
    """

    try:
        cursor.execute(query)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        pytest.fail(f"Failed to query database: {e}")
    finally:
        conn.close()

    total = 0.0
    for emp, avg in results:
        if emp in members:
            total += avg

    return round(total, 2)

def test_result_json_exists_and_valid():
    result_path = "/home/user/result.json"
    assert os.path.exists(result_path), f"Output file missing: {result_path}"

    with open(result_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File is not valid JSON: {result_path}")

    assert "manager" in data, "Missing 'manager' key in JSON"
    assert "subgraph_members" in data, "Missing 'subgraph_members' key in JSON"
    assert "total_latest_rolling_avg" in data, "Missing 'total_latest_rolling_avg' key in JSON"

def test_result_json_content():
    ttl_path = "/home/user/org_graph.ttl"
    db_path = "/home/user/sales.db"
    result_path = "/home/user/result.json"

    expected_members = get_subgraph_members(ttl_path, "Alice")
    expected_total = get_expected_rolling_avg(db_path, expected_members)

    with open(result_path, 'r') as f:
        data = json.load(f)

    assert data["manager"] == "Alice", f"Expected manager 'Alice', got {data.get('manager')}"

    actual_members = data.get("subgraph_members", [])
    assert isinstance(actual_members, list), "subgraph_members must be a list"
    assert actual_members == expected_members, f"Expected subgraph members {expected_members}, got {actual_members}"

    actual_total = data.get("total_latest_rolling_avg")
    assert isinstance(actual_total, (int, float)), "total_latest_rolling_avg must be a number"
    assert round(actual_total, 2) == expected_total, f"Expected total_latest_rolling_avg {expected_total}, got {actual_total}"