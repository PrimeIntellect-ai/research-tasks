# test_final_state.py
import os
import json
import sqlite3
import pytest

def test_fixed_query_sql_exists_and_correct():
    query_path = "/home/user/fixed_query.sql"
    db_path = "/home/user/network.db"

    assert os.path.exists(query_path), f"File {query_path} is missing."
    assert os.path.exists(db_path), f"Database {db_path} is missing."

    with open(query_path, 'r') as f:
        query = f.read()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()

        # Verify columns
        col_names = [desc[0].lower() for desc in cursor.description]
        assert "source" in col_names, "Query must return 'source' column"
        assert "target" in col_names, "Query must return 'target' column"
        assert "bandwidth" in col_names, "Query must return 'bandwidth' column"

        source_idx = col_names.index("source")
        target_idx = col_names.index("target")
        bw_idx = col_names.index("bandwidth")

        # Expected results:
        # Start -> N1 (1000)
        # Start -> N2 (800)
        # N1 -> End (100)
        # N2 -> End (200)
        # N3 -> End (10000)
        expected_edges = {
            ("Start", "N1"): 1000.0,
            ("Start", "N2"): 800.0,
            ("N1", "End"): 100.0,
            ("N2", "End"): 200.0,
            ("N3", "End"): 10000.0
        }

        actual_edges = {}
        for row in results:
            actual_edges[(row[source_idx], row[target_idx])] = float(row[bw_idx])

        assert actual_edges == expected_edges, f"Query results did not match expected top-2 links. Got: {actual_edges}"

    except sqlite3.Error as e:
        pytest.fail(f"Executing fixed_query.sql failed: {e}")
    finally:
        conn.close()

def test_graph_json_exists_and_correct():
    json_path = "/home/user/graph.json"
    assert os.path.exists(json_path), f"File {json_path} is missing."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} is not valid JSON.")

    assert isinstance(data, list), f"{json_path} must contain a JSON array."

    expected_edges = {
        ("Start", "N1"): 1000.0,
        ("Start", "N2"): 800.0,
        ("N1", "End"): 100.0,
        ("N2", "End"): 200.0,
        ("N3", "End"): 10000.0
    }

    actual_edges = {}
    for item in data:
        assert "source" in item, "JSON object missing 'source'"
        assert "target" in item, "JSON object missing 'target'"
        assert "bandwidth" in item, "JSON object missing 'bandwidth'"
        actual_edges[(item["source"], item["target"])] = float(item["bandwidth"])

    assert actual_edges == expected_edges, f"Data in {json_path} does not match expected output."

def test_solve_path_py_exists():
    script_path = "/home/user/solve_path.py"
    assert os.path.exists(script_path), f"Script {script_path} is missing."

def test_result_json_exists_and_correct():
    result_path = "/home/user/result.json"
    assert os.path.exists(result_path), f"File {result_path} is missing."

    with open(result_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{result_path} is not valid JSON.")

    assert "path" in data, "Result JSON missing 'path'"
    assert "cost" in data, "Result JSON missing 'cost'"

    assert data["path"] == ["Start", "N2", "End"], f"Incorrect path. Expected ['Start', 'N2', 'End'], got {data['path']}"
    assert abs(data["cost"] - 62.5) < 1e-6, f"Incorrect cost. Expected 62.5, got {data['cost']}"