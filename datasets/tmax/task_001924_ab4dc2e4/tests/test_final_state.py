# test_final_state.py

import os
import sqlite3
import requests
import pytest
import math

def test_api_backup_1():
    url = "http://127.0.0.1:8080/validate"
    payload = {"backup_id": 1}
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to or get valid response from API: {e}")

    data = response.json()
    assert data.get("backup_id") == 1, f"Expected backup_id 1, got {data.get('backup_id')}"
    assert data.get("top_centrality_node") == "A", f"Expected top_centrality_node 'A', got {data.get('top_centrality_node')}"

    avg_clustering = data.get("avg_clustering")
    assert avg_clustering is not None, "avg_clustering is missing in response"
    assert math.isclose(avg_clustering, 0.3333, rel_tol=1e-3), f"Expected avg_clustering ~0.3333, got {avg_clustering}"

def test_api_backup_2():
    url = "http://127.0.0.1:8080/validate"
    payload = {"backup_id": 2}
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to or get valid response from API: {e}")

    data = response.json()
    assert data.get("backup_id") == 2, f"Expected backup_id 2, got {data.get('backup_id')}"
    assert data.get("top_centrality_node") == "X", f"Expected top_centrality_node 'X', got {data.get('top_centrality_node')}"

    avg_clustering = data.get("avg_clustering")
    assert avg_clustering is not None, "avg_clustering is missing in response"
    assert math.isclose(avg_clustering, 0.0, rel_tol=1e-3), f"Expected avg_clustering 0.0, got {avg_clustering}"

def test_database_indexes():
    db_path = "/home/user/backup.db"
    assert os.path.exists(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    def has_index_on_column(table_name, column_name):
        cursor.execute(f"PRAGMA index_list('{table_name}')")
        indexes = cursor.fetchall()
        for idx in indexes:
            index_name = idx[1]
            cursor.execute(f"PRAGMA index_info('{index_name}')")
            cols = cursor.fetchall()
            if any(col[2] == column_name for col in cols):
                return True
        return False

    assert has_index_on_column('nodes', 'backup_id'), "Missing index on 'backup_id' in 'nodes' table."
    assert has_index_on_column('edges', 'backup_id'), "Missing index on 'backup_id' in 'edges' table."

    conn.close()

def test_extract_graph_sql_fixed():
    sql_path = "/home/user/extract_graph.sql"
    assert os.path.exists(sql_path), f"SQL script {sql_path} is missing."

    with open(sql_path, 'r') as f:
        content = f.read()

    # Check for parameterization (e.g. ?, $1, :backup_id, @backup_id)
    parameterized = any(char in content for char in ['?', '$', ':', '@'])
    assert parameterized, f"The query in {sql_path} does not appear to be parameterized."

    # Check that implicit cross join is removed
    # The original buggy query had 'FROM nodes n1, nodes n2, edges e'
    # We check that there are no comma-separated table lists in the FROM clause
    # A simple heuristic is to check for multiple commas after FROM, or just look for the original pattern
    lower_content = content.lower()
    assert "nodes n1, nodes n2" not in lower_content, "The query still contains the implicit cross join 'nodes n1, nodes n2'."