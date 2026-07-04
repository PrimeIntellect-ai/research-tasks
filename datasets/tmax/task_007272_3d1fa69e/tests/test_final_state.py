# test_final_state.py
import os
import json
import sqlite3
import pytest

JSON_PATH = "/home/user/vulnerable_graph.json"
DB_PATH = "/home/user/infrastructure.db"

def test_json_file_exists():
    assert os.path.isfile(JSON_PATH), f"Output JSON file missing at {JSON_PATH}"

def test_json_content():
    with open(JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File at {JSON_PATH} is not valid JSON.")

    assert "vulnerable_nodes" in data, "JSON missing 'vulnerable_nodes' key"
    assert "impacted_edges" in data, "JSON missing 'impacted_edges' key"

    # Compute expected values from DB to be robust
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Vulnerable Services: active services with NO 'SUCCESS' backup
    c.execute("""
        SELECT service_id, service_name 
        FROM services 
        WHERE is_active = 1 
          AND service_id NOT IN (
              SELECT service_id FROM backups WHERE status = 'SUCCESS'
          )
    """)
    expected_vulnerable = [{"service_id": row["service_id"], "service_name": row["service_name"]} for row in c.fetchall()]

    # Impacted Consumers: active services that depend on vulnerable services
    c.execute("""
        SELECT d.provider_id, d.consumer_id
        FROM dependencies d
        JOIN services p ON d.provider_id = p.service_id
        JOIN services c ON d.consumer_id = c.service_id
        WHERE p.is_active = 1 
          AND p.service_id NOT IN (
              SELECT service_id FROM backups WHERE status = 'SUCCESS'
          )
          AND c.is_active = 1
    """)
    expected_edges = [{"provider_id": row["provider_id"], "consumer_id": row["consumer_id"]} for row in c.fetchall()]
    conn.close()

    # Sort lists to compare ignoring order
    actual_vulnerable = sorted(data["vulnerable_nodes"], key=lambda x: x.get("service_id", -1))
    expected_vulnerable_sorted = sorted(expected_vulnerable, key=lambda x: x["service_id"])

    assert actual_vulnerable == expected_vulnerable_sorted, f"Expected vulnerable_nodes: {expected_vulnerable_sorted}, but got: {actual_vulnerable}"

    actual_edges = sorted(data["impacted_edges"], key=lambda x: (x.get("provider_id", -1), x.get("consumer_id", -1)))
    expected_edges_sorted = sorted(expected_edges, key=lambda x: (x["provider_id"], x["consumer_id"]))

    assert actual_edges == expected_edges_sorted, f"Expected impacted_edges: {expected_edges_sorted}, but got: {actual_edges}"