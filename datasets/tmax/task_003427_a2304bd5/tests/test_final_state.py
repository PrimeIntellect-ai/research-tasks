# test_final_state.py
import sqlite3
import json
import os
import pytest

DB_PATH = "/home/user/employees.db"
JSON_PATH = "/home/user/transfers.json"
REPORT_PATH = "/home/user/audit_report.json"

def get_db_data():
    if not os.path.exists(DB_PATH):
        pytest.fail(f"Database file {DB_PATH} is missing.")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, name, department_id FROM employees")
    employees = c.fetchall()
    c.execute("SELECT id, name FROM departments")
    departments = c.fetchall()
    conn.close()
    return employees, departments

def get_transfers():
    if not os.path.exists(JSON_PATH):
        pytest.fail(f"JSON file {JSON_PATH} is missing.")
    with open(JSON_PATH, 'r') as f:
        return json.load(f)

def compute_expected_reach():
    employees, _ = get_db_data()
    emp_ids = [e[0] for e in employees]
    transfers = get_transfers()

    adj = {eid: set() for eid in emp_ids}
    for t in transfers:
        src = t.get('source_emp_id')
        dst = t.get('dest_emp_id')
        if src in adj:
            adj[src].add(dst)

    reach = {}
    for eid in emp_ids:
        visited = set()
        stack = list(adj[eid])
        while stack:
            curr = stack.pop()
            if curr not in visited:
                visited.add(curr)
                if curr in adj:
                    stack.extend(adj[curr])
        visited.discard(eid)
        reach[eid] = len(visited)
    return reach

def compute_expected_report():
    employees, departments = get_db_data()
    dep_map = {d[0]: d[1] for d in departments}
    reach = compute_expected_reach()

    dep_emps = {d[0]: [] for d in departments}
    for e in employees:
        eid, name, did = e
        dep_emps[did].append({
            'emp_id': eid,
            'employee_name': name,
            'reach': reach[eid]
        })

    report = []
    for did, emps in dep_emps.items():
        emps.sort(key=lambda x: (-x['reach'], x['emp_id']))
        curr_rank = 1
        for i, emp in enumerate(emps):
            if i > 0 and emps[i]['reach'] < emps[i-1]['reach']:
                curr_rank += 1
            if curr_rank <= 2:
                report.append({
                    "department_name": dep_map[did],
                    "emp_id": emp['emp_id'],
                    "employee_name": emp['employee_name'],
                    "reach": emp['reach'],
                    "department_rank": curr_rank
                })

    report.sort(key=lambda x: (x['department_name'], x['department_rank'], x['emp_id']))
    return report

def test_reach_metrics_table():
    expected_reach = compute_expected_reach()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='reach_metrics';")
    if not c.fetchone():
        pytest.fail("Table 'reach_metrics' was not created in employees.db.")

    c.execute("SELECT emp_id, reach FROM reach_metrics")
    actual_reach = dict(c.fetchall())
    conn.close()

    for eid, expected_val in expected_reach.items():
        assert eid in actual_reach, f"Employee ID {eid} missing from reach_metrics table."
        assert actual_reach[eid] == expected_val, f"Incorrect reach for employee {eid}. Expected {expected_val}, got {actual_reach[eid]}."

def test_audit_report_json():
    if not os.path.exists(REPORT_PATH):
        pytest.fail(f"Audit report file {REPORT_PATH} is missing.")

    with open(REPORT_PATH, 'r') as f:
        try:
            actual_report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} is not valid JSON.")

    expected_report = compute_expected_report()

    assert isinstance(actual_report, list), "Audit report must be a JSON array."
    assert len(actual_report) == len(expected_report), f"Expected {len(expected_report)} records in audit report, got {len(actual_report)}."

    for i, (actual, expected) in enumerate(zip(actual_report, expected_report)):
        assert actual == expected, f"Mismatch at index {i} in audit report.\nExpected: {expected}\nActual: {actual}"