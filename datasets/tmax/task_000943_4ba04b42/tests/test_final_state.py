# test_final_state.py
import os
import json
import sqlite3
import pytest

def test_db_duplicates_removed():
    db_path = '/home/user/citation_graph.db'
    assert os.path.isfile(db_path), f"Database {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT source_id, target_id, COUNT(*) 
        FROM citations 
        GROUP BY source_id, target_id 
        HAVING COUNT(*) > 1
    """)
    duplicates = cursor.fetchall()
    conn.close()

    assert len(duplicates) == 0, f"Found {len(duplicates)} duplicate pairs in the citations table. Duplicates were not removed."

def test_db_unique_index_created():
    db_path = '/home/user/citation_graph.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query all indexes on the citations table
    cursor.execute("PRAGMA index_list('citations')")
    indexes = cursor.fetchall()

    unique_index_found = False
    for idx in indexes:
        idx_name = idx[1]
        is_unique = idx[2]

        if is_unique:
            # Check the columns of this index
            cursor.execute(f"PRAGMA index_info('{idx_name}')")
            cols = cursor.fetchall()
            col_names = {col[2] for col in cols}
            if col_names == {'source_id', 'target_id'}:
                unique_index_found = True
                break

    conn.close()
    assert unique_index_found, "A UNIQUE index on (source_id, target_id) was not found in the citations table."

def test_c_source_file_exists():
    c_path = '/home/user/graph_analyzer.c'
    assert os.path.isfile(c_path), f"C source file {c_path} is missing."

def test_json_output_correct():
    json_path = '/home/user/top_nodes.json'
    assert os.path.isfile(json_path), f"Output JSON file {json_path} is missing."

    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse JSON in {json_path}: {e}")

    expected = {
        "top_nodes": [
            {"node_id": 3, "degree": 7},
            {"node_id": 1, "degree": 5},
            {"node_id": 2, "degree": 4}
        ]
    }

    assert data == expected, f"JSON content mismatch. Expected {expected}, but got {data}."