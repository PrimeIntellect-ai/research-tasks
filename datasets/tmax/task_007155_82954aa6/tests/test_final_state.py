# test_final_state.py

import os
import json
import pytest

def test_deadlock_report_exists_and_correct():
    report_path = "/home/user/deadlock_report.json"
    assert os.path.isfile(report_path), f"File {report_path} is missing."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    assert "deadlock_cycle" in data, "Key 'deadlock_cycle' is missing in the report."
    cycle = data["deadlock_cycle"]

    assert isinstance(cycle, list), "'deadlock_cycle' must be an array."

    expected_cycle = ["U_ALICE", "U_BOB", "U_CHARLIE", "U_DIANA"]
    assert cycle == expected_cycle, f"Expected deadlock cycle {expected_cycle}, but got {cycle}."

def test_schema_sql_exists_and_contains_indexes():
    schema_path = "/home/user/schema.sql"
    assert os.path.isfile(schema_path), f"File {schema_path} is missing."

    with open(schema_path, "r") as f:
        content = f.read().upper()

    assert "CREATE TABLE" in content, "schema.sql does not contain CREATE TABLE statements."
    assert "CREATE INDEX" in content, "schema.sql does not contain CREATE INDEX statements as requested to optimize the join."

    # Check if resource_id or state is indexed, or just generally expect index
    assert "INDEX" in content, "No indexes found in schema.sql."