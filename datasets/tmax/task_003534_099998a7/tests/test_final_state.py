# test_final_state.py

import os
import json
import time
import sqlite3
import subprocess
import pytest

DB_PATH = "/home/user/audit.db"
REPORT_PATH = "/home/user/compliance_report.json"
SCRIPT_PATH = "/home/user/generate_report.py"
OPTIMIZE_SCRIPT_PATH = "/home/user/optimize.py"

GOLDEN_QUERY = """
WITH OutOfDept AS (
    SELECT a.emp_uid, a.access_time, a.severity
    FROM access_logs a
    JOIN employees e ON a.emp_uid = e.emp_uid
    WHERE a.resource_dept_id != e.dept_id
),
RollingSums AS (
    SELECT emp_uid,
           SUM(severity) OVER (
               PARTITION BY emp_uid
               ORDER BY access_time
               RANGE BETWEEN 1209600 PRECEDING AND CURRENT ROW
           ) as rolling_sev
    FROM OutOfDept
)
SELECT emp_uid, MAX(rolling_sev) as max_rolling_severity
FROM RollingSums
GROUP BY emp_uid
HAVING MAX(rolling_sev) > 100
ORDER BY max_rolling_severity DESC, emp_uid ASC;
"""

def get_golden_data():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(GOLDEN_QUERY)
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "emp_uid": row["emp_uid"],
            "max_rolling_severity": row["max_rolling_severity"]
        }
        for row in rows
    ]

def test_optimize_script_exists():
    assert os.path.exists(OPTIMIZE_SCRIPT_PATH), f"Missing optimization script: {OPTIMIZE_SCRIPT_PATH}"
    assert os.path.isfile(OPTIMIZE_SCRIPT_PATH), f"Not a file: {OPTIMIZE_SCRIPT_PATH}"

def test_compliance_report_correctness():
    assert os.path.exists(REPORT_PATH), f"Missing report file: {REPORT_PATH}"

    with open(REPORT_PATH, "r") as f:
        try:
            agent_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} is not valid JSON.")

    golden_data = get_golden_data()

    assert agent_data == golden_data, "The generated compliance report does not match the expected output."

def test_performance_metric():
    # First, ensure correctness before measuring performance
    with open(REPORT_PATH, "r") as f:
        agent_data = json.load(f)
    golden_data = get_golden_data()
    if agent_data != golden_data:
        pytest.fail("Cannot measure performance: JSON output is incorrect.")

    start_time = time.time()
    result = subprocess.run(["python3", SCRIPT_PATH], capture_output=True, text=True)
    duration = time.time() - start_time

    assert result.returncode == 0, f"Script failed to run: {result.stderr}"
    assert duration <= 1.5, f"Execution time {duration:.3f}s exceeded the 1.5s threshold."