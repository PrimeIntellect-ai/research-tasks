# test_final_state.py

import os
import json
import sqlite3
import pytest

DB_PATH = '/home/user/routing.db'
JSON_PATH = '/home/user/top_paths.json'

def test_json_output_exists_and_correct():
    assert os.path.exists(JSON_PATH), f"Output file {JSON_PATH} does not exist."
    assert os.path.isfile(JSON_PATH), f"Path {JSON_PATH} is not a file."

    with open(JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {JSON_PATH} is not valid JSON.")

    assert isinstance(data, list), "JSON output must be a list of objects."
    assert len(data) == 3, f"Expected exactly 3 paths, got {len(data)}."

    expected_paths = [
        {
            "path_names": "Router_START,Router_A,Router_C,Router_D,Router_END",
            "total_weight": 16.0,
            "hop_count": 4
        },
        {
            "path_names": "Router_START,Router_C,Router_D,Router_END",
            "total_weight": 19.0,
            "hop_count": 3
        },
        {
            "path_names": "Router_START,Router_A,Router_D,Router_END",
            "total_weight": 21.0,
            "hop_count": 3
        }
    ]

    for i, expected in enumerate(expected_paths):
        actual = data[i]
        assert "path_names" in actual, f"Missing 'path_names' in result {i+1}."
        assert "total_weight" in actual, f"Missing 'total_weight' in result {i+1}."
        assert "hop_count" in actual, f"Missing 'hop_count' in result {i+1}."

        assert actual["path_names"] == expected["path_names"], f"Result {i+1} 'path_names' mismatch. Expected {expected['path_names']}, got {actual['path_names']}."
        assert float(actual["total_weight"]) == expected["total_weight"], f"Result {i+1} 'total_weight' mismatch. Expected {expected['total_weight']}, got {actual['total_weight']}."
        assert int(actual["hop_count"]) == expected["hop_count"], f"Result {i+1} 'hop_count' mismatch. Expected {expected['hop_count']}, got {actual['hop_count']}."

def test_database_indexes():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} does not exist."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check that idx_bad is dropped
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_bad'")
    assert cursor.fetchone() is None, "The bad index 'idx_bad' was not dropped."

    # Check for indexes on edges table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='edges'")
    indexes = cursor.fetchall()

    assert len(indexes) == 1, f"Expected exactly 1 index on 'edges', found {len(indexes)}."

    index_name = indexes[0][0]

    # Check that the index starts with source_id
    cursor.execute(f"PRAGMA index_info('{index_name}')")
    columns = cursor.fetchall()

    assert len(columns) >= 1, f"Index {index_name} has no columns."

    # Pragma index_info returns (seqno, cid, name)
    # We want the first column (seqno=0) to be source_id
    first_col = next(col[2] for col in columns if col[0] == 0)
    assert first_col == 'source_id', f"The optimal index must start with 'source_id', but starts with '{first_col}'."

    conn.close()