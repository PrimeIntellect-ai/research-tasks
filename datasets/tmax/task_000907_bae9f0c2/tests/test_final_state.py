# test_final_state.py

import os
import json
import sqlite3
import pytest

def test_c_source_exists():
    assert os.path.isfile("/home/user/analyze_backup.c"), "C source file /home/user/analyze_backup.c is missing."

def test_c_binary_exists():
    assert os.path.isfile("/home/user/analyze_backup"), "Compiled binary /home/user/analyze_backup is missing."
    assert os.access("/home/user/analyze_backup", os.X_OK), "Binary /home/user/analyze_backup is not executable."

def test_analytics_jsonl_exists():
    assert os.path.isfile("/home/user/analytics.jsonl"), "Output file /home/user/analytics.jsonl is missing."

def test_analytics_jsonl_content():
    expected_data = [
        {"id": 1, "name": "root", "total_size": 5570, "rank": 1},
        {"id": 3, "name": "var", "total_size": 3800, "rank": 2},
        {"id": 7, "name": "log", "total_size": 3800, "rank": 2},
        {"id": 8, "name": "syslog", "total_size": 3000, "rank": 4},
        {"id": 2, "name": "usr", "total_size": 1700, "rank": 5},
        {"id": 4, "name": "bin", "total_size": 1700, "rank": 5},
        {"id": 5, "name": "bash", "total_size": 1200, "rank": 7},
        {"id": 9, "name": "auth.log", "total_size": 800, "rank": 8},
        {"id": 6, "name": "ls", "total_size": 500, "rank": 9},
        {"id": 10, "name": "etc", "total_size": 70, "rank": 10},
        {"id": 11, "name": "passwd", "total_size": 50, "rank": 11},
        {"id": 12, "name": "hosts", "total_size": 20, "rank": 12}
    ]

    expected_dict = {row["id"]: row for row in expected_data}
    actual_dict = {}

    try:
        with open("/home/user/analytics.jsonl", "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)
                assert "id" in row, f"Missing 'id' in row: {line}"
                assert "name" in row, f"Missing 'name' in row: {line}"
                assert "total_size" in row, f"Missing 'total_size' in row: {line}"
                assert "rank" in row, f"Missing 'rank' in row: {line}"
                actual_dict[row["id"]] = row
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse analytics.jsonl as JSON Lines: {e}")

    assert len(actual_dict) == len(expected_dict), f"Expected {len(expected_dict)} rows, got {len(actual_dict)}"

    for node_id, expected_row in expected_dict.items():
        assert node_id in actual_dict, f"Node id {node_id} missing from output."
        actual_row = actual_dict[node_id]
        assert actual_row["name"] == expected_row["name"], f"Node {node_id} name mismatch: expected {expected_row['name']}, got {actual_row['name']}"
        assert actual_row["total_size"] == expected_row["total_size"], f"Node {node_id} total_size mismatch: expected {expected_row['total_size']}, got {actual_row['total_size']}"
        assert actual_row["rank"] == expected_row["rank"], f"Node {node_id} rank mismatch: expected {expected_row['rank']}, got {actual_row['rank']}"

def test_index_handled():
    # The task requires bypassing or removing the index. If it was removed, it won't be in sqlite_master.
    # If it was bypassed, the C program must contain 'INDEX' or 'DROP' or 'NOT INDEXED' to handle it.
    db_path = "/home/user/backup.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_stale_size'")
    index_exists = cursor.fetchone() is not None
    conn.close()

    if index_exists:
        # If index still exists, the C code must have bypassed it (e.g. NOT INDEXED or similar logic)
        with open("/home/user/analyze_backup.c", "r") as f:
            code = f.read().upper()
        # We look for indications of handling the index
        assert "NOT INDEXED" in code or "DROP INDEX" in code or "INDEX" in code, "The corrupted index idx_stale_size was not dropped and no bypass mechanism was found in the C source."