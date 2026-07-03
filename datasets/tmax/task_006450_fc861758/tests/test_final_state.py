# test_final_state.py

import os
import json
import sqlite3
import pytest

def get_expected_results(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    SELECT 
      A.name as employee_name,
      B.name as department_name,
      C.name as project_name,
      M.name as manager_name,
      D.name as manager_department
    FROM Entity A
    JOIN Relation R1 ON A.id = R1.source_id AND R1.rel_type = 'WORKS_FOR'
    JOIN Entity B ON R1.target_id = B.id AND B.label = 'Department'

    JOIN Relation R2 ON B.id = R2.source_id AND R2.rel_type = 'MANAGES'
    JOIN Entity C ON R2.target_id = C.id AND C.label = 'Project'

    JOIN Relation R3 ON A.id = R3.source_id AND R3.rel_type = 'ASSIGNED_TO' AND R3.target_id = C.id

    JOIN Relation R4 ON A.id = R4.source_id AND R4.rel_type = 'REPORTS_TO'
    JOIN Entity M ON R4.target_id = M.id AND M.label = 'Person'

    JOIN Relation R5 ON M.id = R5.source_id AND R5.rel_type = 'WORKS_FOR'
    JOIN Entity D ON R5.target_id = D.id AND D.label = 'Department'

    WHERE A.label = 'Person' AND B.id != D.id
    ORDER BY A.name ASC;
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    expected = []
    for row in rows:
        expected.append({
            "employee_name": row[0],
            "department_name": row[1],
            "project_name": row[2],
            "manager_name": row[3],
            "manager_department": row[4]
        })
    return expected

def test_output_json_exists_and_correct():
    output_path = "/home/user/output.json"
    db_path = "/home/user/graph.db"

    assert os.path.exists(output_path), f"Output file is missing at {output_path}"

    with open(output_path, "r") as f:
        try:
            output_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_path} is not valid JSON")

    assert isinstance(output_data, list), "Output JSON must be a list of objects"

    expected_data = get_expected_results(db_path)

    assert len(output_data) == len(expected_data), f"Expected {len(expected_data)} results, but got {len(output_data)}"

    for i, (actual, expected) in enumerate(zip(output_data, expected_data)):
        assert isinstance(actual, dict), f"Item at index {i} is not a JSON object"
        for key in ["employee_name", "department_name", "project_name", "manager_name", "manager_department"]:
            assert key in actual, f"Missing key '{key}' in result object at index {i}"
            assert actual[key] == expected[key], f"Mismatch for key '{key}' at index {i}: expected '{expected[key]}', got '{actual[key]}'"