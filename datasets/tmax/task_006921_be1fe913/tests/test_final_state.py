# test_final_state.py

import os
import json
import sqlite3
import pytest
from collections import defaultdict

def get_expected_violations():
    # Connect to DB
    db_path = '/home/user/data/hr.db'
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Load employees
    c.execute("SELECT id, department FROM employees")
    employees = {row[0]: row[1] for row in c.fetchall()}

    # Load resources
    c.execute("SELECT id, department_owner FROM resources")
    resources = {row[0]: row[1] for row in c.fetchall()}

    conn.close()

    # Load authorizations
    auth_path = '/home/user/data/authorizations.json'
    with open(auth_path, 'r') as f:
        auth_data = json.load(f)
    authorizations = {(item["user_id"], item["resource_id"]) for item in auth_data}

    # Load access logs
    logs_path = '/home/user/data/access_logs.json'
    with open(logs_path, 'r') as f:
        logs_data = json.load(f)

    # Compute violations
    violations = defaultdict(int)
    for log in logs_data:
        uid = log.get("user_id")
        rid = log.get("resource_id")

        user_dept = employees.get(uid)
        res_owner = resources.get(rid)

        if user_dept and res_owner:
            if user_dept != res_owner:
                if (uid, rid) not in authorizations:
                    violations[user_dept] += 1

    # Remove departments with 0 violations
    return {k: v for k, v in violations.items() if v > 0}

def test_audit_script_exists():
    script_path = '/home/user/audit.py'
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_violations_summary_exists_and_correct():
    summary_path = '/home/user/violations_summary.json'
    assert os.path.isfile(summary_path), f"The output file {summary_path} does not exist."

    with open(summary_path, 'r') as f:
        try:
            actual_summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {summary_path} is not valid JSON.")

    expected_summary = get_expected_violations()

    assert actual_summary == expected_summary, (
        f"The violations summary is incorrect.\n"
        f"Expected: {expected_summary}\n"
        f"Actual: {actual_summary}"
    )