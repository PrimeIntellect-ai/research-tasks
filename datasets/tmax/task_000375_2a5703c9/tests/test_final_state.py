# test_final_state.py

import os
import json
import sqlite3
import pytest

def test_run_pipeline_exists_and_executable():
    script_path = '/home/user/run_pipeline.sh'
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_violations_json_correctness():
    json_path = '/home/user/violations.json'
    db_path = '/home/user/audit.db'

    assert os.path.exists(json_path), f"Output file {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            actual_violations = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} does not contain valid JSON.")

    assert isinstance(actual_violations, list), f"JSON root in {json_path} must be a list."

    # Compute expected violations from the database
    assert os.path.exists(db_path), f"Database {db_path} is missing."
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    query = """
        SELECT 
            a.log_id,
            e.name as employee_name,
            s.sys_name as system_name,
            e.clearance_level,
            s.required_clearance,
            e.termination_date,
            a.access_timestamp
        FROM access_logs a
        JOIN employees e ON a.emp_id = e.emp_id
        JOIN systems s ON a.sys_id = s.sys_id
    """
    c.execute(query)
    rows = c.fetchall()

    expected_violations = []
    for row in rows:
        log_id = row['log_id']
        emp_name = row['employee_name']
        sys_name = row['system_name']
        clearance = row['clearance_level']
        req_clearance = row['required_clearance']
        term_date = row['termination_date']
        access_ts = row['access_timestamp']

        access_date = access_ts.split(' ')[0]

        is_terminated = False
        if term_date is not None and access_date > term_date:
            is_terminated = True

        is_clearance_violation = False
        if clearance < req_clearance:
            is_clearance_violation = True

        if is_terminated:
            violation_type = "TERMINATED"
        elif is_clearance_violation:
            violation_type = "CLEARANCE"
        else:
            continue

        expected_violations.append({
            "log_id": log_id,
            "employee_name": emp_name,
            "system_name": sys_name,
            "violation_type": violation_type
        })

    conn.close()

    expected_violations.sort(key=lambda x: x['log_id'])

    assert len(actual_violations) == len(expected_violations), f"Expected {len(expected_violations)} violations, but found {len(actual_violations)}."

    for i, (actual, expected) in enumerate(zip(actual_violations, expected_violations)):
        assert actual.get('log_id') == expected['log_id'], f"Mismatch at index {i}: expected log_id {expected['log_id']}, got {actual.get('log_id')}"
        assert actual.get('employee_name') == expected['employee_name'], f"Mismatch at index {i}: expected employee_name {expected['employee_name']}, got {actual.get('employee_name')}"
        assert actual.get('system_name') == expected['system_name'], f"Mismatch at index {i}: expected system_name {expected['system_name']}, got {actual.get('system_name')}"
        assert actual.get('violation_type') == expected['violation_type'], f"Mismatch at index {i}: expected violation_type {expected['violation_type']}, got {actual.get('violation_type')}"