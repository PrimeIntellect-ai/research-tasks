# test_final_state.py
import os
import json
import sqlite3
import pytest

DB_PATH = '/home/user/audit.db'
REPORT_PATH = '/home/user/compliance_report.json'
SCRIPT_PATH = '/home/user/audit_report.py'
PLAN_PATH = '/home/user/query_plan.txt'

def test_files_exist():
    assert os.path.isfile(SCRIPT_PATH), f"Script missing: {SCRIPT_PATH}"
    assert os.path.isfile(REPORT_PATH), f"Report missing: {REPORT_PATH}"
    assert os.path.isfile(PLAN_PATH), f"Query plan missing: {PLAN_PATH}"

def test_compliance_report_content():
    assert os.path.isfile(REPORT_PATH), "Report file does not exist."

    with open(REPORT_PATH, 'r') as f:
        try:
            agent_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("compliance_report.json is not valid JSON.")

    required_keys = {"unauthorized_access_log_ids", "anomalous_employee_ids", "toxic_employee_ids"}
    assert set(agent_data.keys()) == required_keys, f"Report keys mismatch. Expected {required_keys}, got {set(agent_data.keys())}"

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 1. Toxic
    c.execute("SELECT id FROM employees WHERE permissions LIKE '%APPROVE_FUNDS%' AND permissions LIKE '%REQUEST_FUNDS%' ORDER BY id")
    toxic = [r[0] for r in c.fetchall()]
    assert agent_data['toxic_employee_ids'] == toxic, "toxic_employee_ids do not match the expected output."

    # 2. Anomalous
    c.execute("""
        SELECT DISTINCT employee_id FROM (
            SELECT employee_id, count(*) OVER (
                PARTITION BY employee_id 
                ORDER BY strftime('%s', timestamp)
                RANGE BETWEEN 259200 PRECEDING AND CURRENT ROW
            ) as cnt
            FROM access_logs
        ) WHERE cnt > 5 ORDER BY employee_id
    """)
    anomalous = [r[0] for r in c.fetchall()]
    assert agent_data['anomalous_employee_ids'] == anomalous, "anomalous_employee_ids do not match the expected output."

    # 3. Unauthorized
    c.execute("""
        WITH RECURSIVE
        management_chain AS (
            SELECT id as owner_id, manager_id as boss_id FROM employees WHERE manager_id IS NOT NULL
            UNION ALL
            SELECT mc.owner_id, e.manager_id 
            FROM management_chain mc
            JOIN employees e ON mc.boss_id = e.id
            WHERE e.manager_id IS NOT NULL
        )
        SELECT a.id 
        FROM access_logs a
        LEFT JOIN management_chain mc ON a.resource_owner_id = mc.owner_id AND a.employee_id = mc.boss_id
        WHERE a.employee_id != a.resource_owner_id
        AND mc.boss_id IS NULL
        ORDER BY a.id
    """)
    unauth = [r[0] for r in c.fetchall()]
    assert agent_data['unauthorized_access_log_ids'] == unauth, "unauthorized_access_log_ids do not match the expected output."

    conn.close()

def test_database_optimized():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%';")
    indexes = [row[0] for row in c.fetchall()]
    conn.close()

    assert len(indexes) > 0, "No custom indexes were created in the database to optimize the queries."

def test_query_plan_output():
    assert os.path.isfile(PLAN_PATH), "Query plan file does not exist."
    with open(PLAN_PATH, 'r') as f:
        content = f.read().strip()
    assert len(content) > 0, "query_plan.txt is empty."
    assert "SCAN" in content or "SEARCH" in content or "EXECUTE" in content, "query_plan.txt does not look like a valid EXPLAIN QUERY PLAN output."