# test_final_state.py

import os
import sqlite3
import pytest
import requests
import time
import subprocess
import json

def test_hyperquery_fixed():
    engine_path = "/app/hyperquery/engine.py"
    assert os.path.exists(engine_path), f"File {engine_path} does not exist."

    with open(engine_path, "r") as f:
        content = f.read()

    assert "HYPER_DB_PATHH" not in content, f"The typo 'HYPER_DB_PATHH' is still present in {engine_path}."
    assert "HYPER_DB_PATH" in content, f"'HYPER_DB_PATH' was not found in {engine_path}."

def test_optimize_sql_exists():
    sql_path = "/home/user/optimize.sql"
    assert os.path.exists(sql_path), f"File {sql_path} does not exist."
    with open(sql_path, "r") as f:
        content = f.read().lower()
    assert "create index" in content, "No CREATE INDEX statement found in optimize.sql."

def test_indexes_applied():
    db_path = "/home/user/graph_data.db"
    assert os.path.exists(db_path), f"Database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='index';")
    indexes = cursor.fetchall()
    conn.close()

    # We expect indexes on edges(source, rel_type), edges(target, rel_type), nodes(json_extract(properties, '$.category'))
    # Since the exact names and syntax can vary, we will look for keywords in the SQL of the indexes.

    edges_source_idx = False
    edges_target_idx = False
    nodes_json_idx = False

    for name, sql in indexes:
        if not sql:
            continue
        sql_lower = sql.lower()
        if "edges" in sql_lower and "source" in sql_lower and "rel_type" in sql_lower:
            edges_source_idx = True
        if "edges" in sql_lower and "target" in sql_lower and "rel_type" in sql_lower:
            edges_target_idx = True
        if "nodes" in sql_lower and "json_extract" in sql_lower and "category" in sql_lower:
            nodes_json_idx = True

    assert edges_source_idx, "Index on edges(source, rel_type) is missing."
    assert edges_target_idx, "Index on edges(target, rel_type) is missing."
    assert nodes_json_idx, "Index on nodes(json_extract(properties, '$.category')) is missing."

def test_server_api():
    url = "http://127.0.0.1:8080/api/query"

    # Wait briefly for server to be up if it was just started
    for _ in range(5):
        try:
            requests.get("http://127.0.0.1:8080/")
            break
        except requests.ConnectionError:
            time.sleep(0.5)

    # 1. No auth -> 401
    resp_no_auth = requests.post(url, json={"query": "SELECT 1", "params": []})
    assert resp_no_auth.status_code == 401, f"Expected 401 Unauthorized without auth, got {resp_no_auth.status_code}."

    # 2. Bad auth -> 401
    headers_bad = {"Authorization": "Bearer wrong-token"}
    resp_bad_auth = requests.post(url, json={"query": "SELECT 1", "params": []}, headers=headers_bad)
    assert resp_bad_auth.status_code == 401, f"Expected 401 Unauthorized with bad auth, got {resp_bad_auth.status_code}."

    # 3. Good auth, valid query
    headers_good = {"Authorization": "Bearer super-secret-dba-token"}
    payload = {
        "query": "SELECT target FROM edges WHERE source = ? AND rel_type = ?",
        "params": ["n2", "PURCHASED"]
    }
    resp_good = requests.post(url, json=payload, headers=headers_good)
    assert resp_good.status_code == 200, f"Expected 200 OK, got {resp_good.status_code}. Body: {resp_good.text}"

    try:
        data = resp_good.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp_good.text}")

    assert data == [["n1"]], f"Expected [['n1']], got {data}"

    # 4. Malformed JSON -> 400
    resp_bad_json = requests.post(url, data="not a json", headers=headers_good)
    assert resp_bad_json.status_code == 400, f"Expected 400 Bad Request for malformed JSON, got {resp_bad_json.status_code}."
    try:
        err_data = resp_bad_json.json()
        assert err_data.get("error") == "Invalid payload", "Expected error message 'Invalid payload'."
    except ValueError:
        pass # If it doesn't return JSON error, at least the status code was 400