# test_final_state.py

import os
import json
import sqlite3
import pytest

APP_DIR = "/home/user/app"

def test_requirements_fixed():
    req_path = os.path.join(APP_DIR, "requirements.txt")
    assert os.path.isfile(req_path), f"File {req_path} does not exist."

    with open(req_path, 'r') as f:
        content = f.read()

    assert "fake-broken-package-999" not in content, "The broken package 'fake-broken-package-999' is still in requirements.txt."

def test_results_json_correctness():
    db_path = os.path.join(APP_DIR, "db", "data.db")
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    # Derive expected results from the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT users.name, SUM(transactions.amount) as total
        FROM users
        JOIN transactions ON users.id = transactions.user_id
        WHERE users.status = 'active'
        GROUP BY users.name
        HAVING total > 0
        ORDER BY total DESC
    """)
    expected_results = [{"name": row[0], "total": row[1]} for row in cursor.fetchall()]
    conn.close()

    json_path = os.path.join(APP_DIR, "output", "results.json")
    assert os.path.isfile(json_path), f"Output file {json_path} does not exist. The script may have crashed or not run."

    with open(json_path, 'r') as f:
        try:
            actual_results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    assert isinstance(actual_results, list), "The JSON output should be a list of dictionaries."
    assert actual_results == expected_results, (
        f"The output JSON does not match the expected results. "
        f"Expected: {expected_results}, but got: {actual_results}. "
        "Ensure filtering (active users, total > 0) and descending sorting by total are correct."
    )