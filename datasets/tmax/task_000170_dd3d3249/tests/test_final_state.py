# test_final_state.py
import os
import json
import sqlite3

def test_analytics_db_exists():
    assert os.path.isfile("/home/user/analytics.db"), "/home/user/analytics.db does not exist."

def test_analytics_db_records():
    conn = sqlite3.connect("/home/user/analytics.db")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT user_id, total_actions FROM user_summary ORDER BY user_id")
        rows = cursor.fetchall()
    except sqlite3.OperationalError as e:
        conn.close()
        assert False, f"Failed to query user_summary table: {e}"

    conn.close()

    expected = [("U001", 3), ("U002", 2), ("U003", 1)]
    assert rows == expected, f"Expected records {expected}, but got {rows}. Pydantic validation or insertion logic is incorrect."

def test_query_plan_exists_and_contains_stats():
    plan_path = "/home/user/query_plan.json"
    assert os.path.isfile(plan_path), f"{plan_path} does not exist."

    with open(plan_path, "r") as f:
        content = f.read()

    assert "executionStats" in content, "query_plan.json does not contain 'executionStats'."

    # Try to parse it as JSON to ensure it is validly formatted
    try:
        json.loads(content)
    except json.JSONDecodeError:
        assert False, "query_plan.json is not a valid JSON file."