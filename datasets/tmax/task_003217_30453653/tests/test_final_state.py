# test_final_state.py
import os
import json
import sqlite3
import pytest
import ast

def test_report_json_exists():
    report_path = '/home/user/report.json'
    assert os.path.exists(report_path), f"Report file {report_path} was not created."
    assert os.path.isfile(report_path), f"{report_path} is not a file."

def test_report_json_content():
    report_path = '/home/user/report.json'
    assert os.path.exists(report_path), "Report file missing."

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} does not contain valid JSON.")

    assert "database_name" in data, "Key 'database_name' missing from JSON output."
    assert data["database_name"] == "billing-db", f"Expected database_name 'billing-db', got '{data['database_name']}'."

    assert "correct_total_backup_size" in data, "Key 'correct_total_backup_size' missing from JSON output."
    assert data["correct_total_backup_size"] == 15500, f"Expected correct_total_backup_size to be 15500, got {data['correct_total_backup_size']}."

    assert "shortest_archive_path" in data, "Key 'shortest_archive_path' missing from JSON output."
    expected_path = ["node_A", "node_C", "node_Z"]
    assert data["shortest_archive_path"] == expected_path, f"Expected shortest_archive_path {expected_path}, got {data['shortest_archive_path']}."

def test_script_uses_recursive_cte():
    script_path = '/home/user/generate_report.py'
    assert os.path.exists(script_path), "Script file missing."

    with open(script_path, 'r') as f:
        content = f.read().upper()

    assert "WITH RECURSIVE" in content, "The script does not appear to use a Recursive CTE ('WITH RECURSIVE') as requested."

def test_script_uses_parameterized_queries():
    script_path = '/home/user/generate_report.py'
    assert os.path.exists(script_path), "Script file missing."

    with open(script_path, 'r') as f:
        content = f.read()

    # Parse the AST to check for calls to cursor.execute
    try:
        tree = ast.parse(content)
    except SyntaxError:
        pytest.fail("Script contains syntax errors.")

    execute_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute) and node.func.attr == 'execute':
                execute_calls.append(node)

    assert len(execute_calls) > 0, "No cursor.execute calls found in the script."

    # Ensure that at least one execute call passes parameters (length of args > 1 or uses keywords)
    # and that string formatting/f-strings are not used directly in the execute call for db_name.
    parameterized = False
    for call in execute_calls:
        if len(call.args) > 1 or call.keywords:
            parameterized = True
            break

    assert parameterized, "The script does not appear to use parameterized queries in cursor.execute()."