# test_final_state.py
import os
import sqlite3
import json
import pytest

DB_PATH = "/home/user/company_data.db"
OUTPUT_JSON_PATH = "/home/user/org_metrics.json"

def get_expected_metrics():
    """Derive the expected organizational metrics directly from the database."""
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} is missing."

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Query to get the latest active employees and calculate their total org salary
    query = """
    WITH RankedEvents AS (
        SELECT emp_id, manager_id, salary, status,
               ROW_NUMBER() OVER (PARTITION BY emp_id ORDER BY event_timestamp DESC) as rn
        FROM employee_events
    ),
    LatestActive AS (
        SELECT emp_id, manager_id, salary
        FROM RankedEvents
        WHERE rn = 1 AND status = 'active'
    ),
    Hierarchy AS (
        -- Base case: every active employee is the root of their own hierarchy
        SELECT emp_id AS root_id, emp_id, salary
        FROM LatestActive

        UNION ALL

        -- Recursive step: find direct reports of the current level
        SELECT h.root_id, c.emp_id, c.salary
        FROM Hierarchy h
        JOIN LatestActive c ON c.manager_id = h.emp_id
    )
    SELECT root_id AS emp_id, 
           (SELECT salary FROM LatestActive WHERE emp_id = root_id) AS salary,
           SUM(salary) AS total_org_salary
    FROM Hierarchy
    GROUP BY root_id
    ORDER BY root_id ASC;
    """

    cur.execute(query)
    rows = cur.fetchall()
    conn.close()

    expected = []
    for row in rows:
        expected.append({
            "emp_id": row["emp_id"],
            "salary": row["salary"],
            "total_org_salary": row["total_org_salary"]
        })

    return expected

def test_json_file_exists():
    """Verify that the output JSON file exists."""
    assert os.path.exists(OUTPUT_JSON_PATH), f"The output file {OUTPUT_JSON_PATH} was not found."
    assert os.path.isfile(OUTPUT_JSON_PATH), f"The path {OUTPUT_JSON_PATH} is not a file."

def test_json_contents_match():
    """Verify that the JSON file contains the correct organizational metrics."""
    assert os.path.exists(OUTPUT_JSON_PATH), "Cannot check contents because JSON file is missing."

    with open(OUTPUT_JSON_PATH, 'r') as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {OUTPUT_JSON_PATH} does not contain valid JSON.")

    assert isinstance(actual_data, list), "The JSON output must be a list of dictionaries."

    expected_data = get_expected_metrics()

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} records, but found {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert isinstance(actual, dict), f"Item at index {i} is not a dictionary."

        assert "emp_id" in actual, f"Item at index {i} is missing 'emp_id'."
        assert "salary" in actual, f"Item at index {i} is missing 'salary'."
        assert "total_org_salary" in actual, f"Item at index {i} is missing 'total_org_salary'."

        assert actual["emp_id"] == expected["emp_id"], f"Mismatch at index {i}: expected emp_id {expected['emp_id']}, got {actual['emp_id']}."
        assert actual["salary"] == expected["salary"], f"Mismatch at index {i} for emp_id {expected['emp_id']}: expected salary {expected['salary']}, got {actual['salary']}."
        assert actual["total_org_salary"] == expected["total_org_salary"], f"Mismatch at index {i} for emp_id {expected['emp_id']}: expected total_org_salary {expected['total_org_salary']}, got {actual['total_org_salary']}."