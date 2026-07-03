# test_final_state.py
import os
import json
import sqlite3
import pytest

DB_PATH = "/home/user/audit.db"
REPORT_PATH = "/home/user/suspicious_report.json"
CARGO_TOML_PATH = "/home/user/audit_tool/Cargo.toml"

def test_rust_project_exists():
    """Verify that the Cargo project was created in the correct location."""
    assert os.path.isfile(CARGO_TOML_PATH), f"Cargo.toml missing at {CARGO_TOML_PATH}"
    assert os.path.isfile("/home/user/audit_tool/src/main.rs"), "Rust source file missing at /home/user/audit_tool/src/main.rs"

def test_json_report_exists_and_valid():
    """Verify that the report file exists and is valid JSON."""
    assert os.path.isfile(REPORT_PATH), f"Report file missing at {REPORT_PATH}"
    with open(REPORT_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Report file is not valid JSON")
    assert isinstance(data, list), "JSON output must be an array of objects"

def test_json_report_contents():
    """Verify the contents of the JSON report match the expected database query results."""
    assert os.path.isfile(REPORT_PATH), "Report file missing"

    with open(REPORT_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Report file is not valid JSON")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Recompute the expected results dynamically
    query = """
    WITH EmployeeTotals AS (
        SELECT e.id, e.name, e.manager_id, SUM(ex.amount) as total_spent
        FROM employees e
        JOIN expenses ex ON e.id = ex.emp_id
        GROUP BY e.id, e.name, e.manager_id
    ),
    Ranked AS (
        SELECT name as employee_name, manager_id, total_spent,
               RANK() OVER (PARTITION BY manager_id ORDER BY total_spent DESC) as team_rank
        FROM EmployeeTotals
        WHERE manager_id IS NOT NULL
    )
    SELECT employee_name, manager_id, total_spent, team_rank
    FROM Ranked
    WHERE team_rank <= 2 AND total_spent > 10000.0
    ORDER BY manager_id ASC, total_spent DESC;
    """

    cursor.execute(query)
    expected_rows = [dict(row) for row in cursor.fetchall()]
    conn.close()

    assert len(data) == len(expected_rows), f"Expected {len(expected_rows)} records in the report, but found {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_rows)):
        assert actual.get("employee_name") == expected["employee_name"], f"Record {i}: Expected employee_name '{expected['employee_name']}', got '{actual.get('employee_name')}'"
        assert actual.get("manager_id") == expected["manager_id"], f"Record {i}: Expected manager_id {expected['manager_id']}, got {actual.get('manager_id')}"
        assert float(actual.get("total_spent", 0)) == float(expected["total_spent"]), f"Record {i}: Expected total_spent {expected['total_spent']}, got {actual.get('total_spent')}"
        assert actual.get("team_rank") == expected["team_rank"], f"Record {i}: Expected team_rank {expected['team_rank']}, got {actual.get('team_rank')}"