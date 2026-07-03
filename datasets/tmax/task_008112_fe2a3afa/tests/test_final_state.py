# test_final_state.py

import os
import json
import csv
import sqlite3
import pytest

def test_phase1_top_communicators_csv():
    csv_path = "/home/user/top_communicators.csv"
    assert os.path.exists(csv_path), f"File {csv_path} does not exist."

    # Calculate truth from database
    db_path = "/home/user/audit.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get message counts per employee
    cursor.execute("""
        SELECT e.department, e.id, COUNT(c.sender_id) as message_count
        FROM employees e
        JOIN communications c ON e.id = c.sender_id
        GROUP BY e.id, e.department
    """)
    counts = cursor.fetchall()
    conn.close()

    # Find max per department
    dept_max = {}
    for dept, emp_id, count in counts:
        if dept not in dept_max or count > dept_max[dept]['count']:
            dept_max[dept] = {'id': emp_id, 'count': count}

    # Read CSV
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['department', 'employee_id', 'message_count'], "CSV header is incorrect."

        rows = list(reader)
        assert len(rows) == len(dept_max), "CSV does not have the correct number of rows."

        for row in rows:
            dept, emp_id, count = row[0], int(row[1]), int(row[2])
            assert dept in dept_max, f"Unexpected department {dept} in CSV."
            assert dept_max[dept]['count'] == count, f"Incorrect message count for department {dept}."
            # If there's a tie, any tied employee is fine, but based on our setup, it's unique.
            # We just check if the count matches the max count for that department.

def test_phase2_highest_centrality_json():
    json_path = "/home/user/highest_centrality.json"
    assert os.path.exists(json_path), f"File {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert "employee_id" in data, "JSON missing 'employee_id' key."
    assert "centrality" in data, "JSON missing 'centrality' key."

    # Node 8 is the guaranteed highest centrality node
    assert data["employee_id"] == 8, f"Expected employee_id 8, got {data['employee_id']}."
    assert isinstance(data["centrality"], (int, float)), "Centrality must be a number."

def test_phase3_shortest_path_json():
    json_path = "/home/user/shortest_path.json"
    assert os.path.exists(json_path), f"File {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert "path" in data, "JSON missing 'path' key."

    expected_path = [3, 8, 15, 18]
    assert data["path"] == expected_path, f"Expected path {expected_path}, got {data['path']}."