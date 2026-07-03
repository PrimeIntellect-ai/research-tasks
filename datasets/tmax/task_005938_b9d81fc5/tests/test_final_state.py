# test_final_state.py

import os
import json
import sqlite3
import pytest
from collections import defaultdict

def test_analyze_leak_script_exists():
    script_path = '/home/user/analyze_leak.py'
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_leak_report_matches_expected_data():
    report_path = '/home/user/leak_report.json'
    assert os.path.isfile(report_path), f"The report {report_path} does not exist."

    # 1. Derive expected data from sources
    logs_path = '/home/user/access_logs.jsonl'
    assert os.path.isfile(logs_path), "Access logs missing."

    access_counts = defaultdict(int)
    with open(logs_path, 'r') as f:
        for line in f:
            log = json.loads(line)
            if log.get("doc_id") == "DOC-999":
                access_counts[log["emp_id"]] += 1

    # Find the suspect (max accesses to DOC-999)
    suspect_id = max(access_counts, key=access_counts.get)
    expected_access_count = access_counts[suspect_id]

    # 2. Query DB for employee details and hierarchy
    db_path = '/home/user/employees.db'
    assert os.path.isfile(db_path), "Employees DB missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT e.name, d.name 
        FROM employees e 
        JOIN departments d ON e.dept_id = d.id 
        WHERE e.id = ?
    """, (suspect_id,))
    row = cursor.fetchone()
    assert row is not None, f"Suspect ID {suspect_id} not found in DB."
    suspect_name, department_name = row

    # 3. Compute management path
    # Fetch all employees to build the tree
    cursor.execute("SELECT id, name, manager_id FROM employees")
    employees = cursor.fetchall()
    conn.close()

    emp_dict = {emp[0]: {"name": emp[1], "manager_id": emp[2]} for emp in employees}

    path = []
    current_id = suspect_id
    while current_id is not None:
        path.append(emp_dict[current_id]["name"])
        current_id = emp_dict[current_id]["manager_id"]
    expected_management_path = path[::-1]  # Reverse to start from CEO

    # 4. Read the generated report
    with open(report_path, 'r') as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The report {report_path} is not valid JSON.")

    # 5. Assert fields
    assert report_data.get("suspect_id") == suspect_id, \
        f"Expected suspect_id {suspect_id}, got {report_data.get('suspect_id')}"

    assert report_data.get("suspect_name") == suspect_name, \
        f"Expected suspect_name '{suspect_name}', got '{report_data.get('suspect_name')}'"

    assert report_data.get("department") == department_name, \
        f"Expected department '{department_name}', got '{report_data.get('department')}'"

    assert report_data.get("access_count") == expected_access_count, \
        f"Expected access_count {expected_access_count}, got {report_data.get('access_count')}"

    assert report_data.get("management_path") == expected_management_path, \
        f"Expected management_path {expected_management_path}, got {report_data.get('management_path')}"