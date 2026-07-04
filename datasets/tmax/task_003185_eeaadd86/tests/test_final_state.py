# test_final_state.py

import os
import sqlite3
import json
import subprocess
import pytest

def test_database_migration_applied():
    db_file = "/home/user/qa_env/test_db.sqlite"
    assert os.path.isfile(db_file), f"Database file {db_file} is missing."

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Check if version column exists
        cursor.execute("PRAGMA table_info(state)")
        columns = [col[1] for col in cursor.fetchall()]
        assert 'version' in columns, "Column 'version' was not added to the 'state' table. Migration was not applied correctly."

        # Check the updated values
        cursor.execute("SELECT id, status, version FROM state WHERE id = 1")
        row = cursor.fetchone()
        assert row is not None, "Row with id=1 is missing from the 'state' table."
        assert row[0] == 1, "Row id is incorrect."
        assert row[1] == 'init', "Row status is incorrect."
        assert row[2] == 2, f"Row version is {row[2]}, expected 2. Migration data update was not applied correctly."
    except sqlite3.Error as e:
        pytest.fail(f"Database error while verifying migration: {e}")
    finally:
        conn.close()

def test_e2e_result_file():
    result_file = "/home/user/qa_env/e2e_result.json"
    assert os.path.isfile(result_file), f"Result file {result_file} is missing. Did you save the client output?"

    try:
        with open(result_file, 'r') as f:
            content = f.read().strip()

        assert content, f"File {result_file} is empty."

        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            pytest.fail(f"Content of {result_file} is not valid JSON. Found: {content}")

        expected_data = {"response": {"id": 1, "status": "init", "version": 2}}
        assert data == expected_data, f"JSON content in {result_file} does not match expected output. Got: {data}"
    except IOError as e:
        pytest.fail(f"Failed to read {result_file}: {e}")

def test_server_process_terminated():
    # Check if mock_server.py is still running
    try:
        # pgrep returns 0 if matches found, 1 if none found
        result = subprocess.run(["pgrep", "-f", "mock_server.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        assert result.returncode != 0, "The mock_server.py process is still running. You must terminate the background server process to clean up."
    except Exception as e:
        pytest.fail(f"Failed to check for running processes: {e}")