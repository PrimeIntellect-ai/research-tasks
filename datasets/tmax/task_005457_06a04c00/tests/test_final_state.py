# test_final_state.py
import os
import json
import sqlite3
import pytest

DB_PATH = '/home/user/backups.db'
JSON_PATH = '/home/user/affected_backups.json'
SCRIPT_PATH = '/home/user/process_lineage.py'

def test_index_created():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} is missing."

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_parent_id';")
    index_row = c.fetchone()

    conn.close()

    assert index_row is not None, "The index 'idx_parent_id' was not created in the database."
    assert index_row[0] == 'idx_parent_id', "The index name does not match 'idx_parent_id'."

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"The script {SCRIPT_PATH} was not created."

def test_json_output_correctness():
    assert os.path.exists(JSON_PATH), f"The output JSON file {JSON_PATH} is missing."

    # Compute the expected result dynamically from the database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    query = """
    WITH RECURSIVE lineage AS (
        SELECT id, file_path, 0 as depth 
        FROM backup_lineage 
        WHERE id = 'bkp_0001'

        UNION ALL

        SELECT b.id, b.file_path, l.depth + 1
        FROM backup_lineage b
        JOIN lineage l ON b.parent_id = l.id
    )
    SELECT id, file_path, depth FROM lineage ORDER BY depth ASC, id ASC;
    """
    c.execute(query)
    rows = c.fetchall()
    conn.close()

    expected_data = [
        {"id": row[0], "file_path": row[1], "depth": row[2]} for row in rows
    ]

    assert len(expected_data) > 0, "Expected data is empty; check the database contents."

    # Load the student's JSON output
    try:
        with open(JSON_PATH, 'r') as f:
            student_data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {JSON_PATH} does not contain valid JSON.")

    assert isinstance(student_data, list), "The JSON output must be a list of objects."

    assert len(student_data) == len(expected_data), (
        f"Expected {len(expected_data)} records in the JSON output, "
        f"but found {len(student_data)}."
    )

    for i, (expected, student) in enumerate(zip(expected_data, student_data)):
        assert student.get("id") == expected["id"], f"Mismatch at index {i}: expected id '{expected['id']}', got '{student.get('id')}'."
        assert student.get("file_path") == expected["file_path"], f"Mismatch at index {i}: expected file_path '{expected['file_path']}', got '{student.get('file_path')}'."
        assert student.get("depth") == expected["depth"], f"Mismatch at index {i}: expected depth {expected['depth']}, got {student.get('depth')}."