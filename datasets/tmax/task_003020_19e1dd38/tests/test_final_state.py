# test_final_state.py
import os
import json
import ast
import pytest

SCRIPT_PATH = "/home/user/analyze_impact.py"
OUTPUT_PATH = "/home/user/impact.json"

def test_output_json_exists_and_correct():
    assert os.path.exists(OUTPUT_PATH), f"Output file {OUTPUT_PATH} is missing."
    assert os.path.isfile(OUTPUT_PATH), f"{OUTPUT_PATH} is not a file."

    with open(OUTPUT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{OUTPUT_PATH} does not contain valid JSON.")

    assert "target" in data, "JSON output is missing the 'target' key."
    assert data["target"] == "PaymentGateway", f"Expected target 'PaymentGateway', got '{data['target']}'."

    assert "impacted" in data, "JSON output is missing the 'impacted' key."
    expected_impacted = ["AnalyticsService", "CartService", "OrderService"]

    assert isinstance(data["impacted"], list), "'impacted' should be a list."
    assert data["impacted"] == expected_impacted, f"Expected impacted list {expected_impacted}, got {data['impacted']}."

def test_script_exists_and_uses_parameterized_queries():
    assert os.path.exists(SCRIPT_PATH), f"Script file {SCRIPT_PATH} is missing."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."

    with open(SCRIPT_PATH, 'r') as f:
        content = f.read()

    # Basic check to ensure the script doesn't use string formatting for SQL queries
    # and uses parameterized queries instead.
    try:
        tree = ast.parse(content)
    except SyntaxError:
        pytest.fail(f"Script {SCRIPT_PATH} contains syntax errors.")

    # Check if '?' or named parameters are likely used in execute calls
    # We will do a simple text check for '?' or ':' in the script, as parsing SQL from AST is complex.
    assert '?' in content or ':' in content, "Script does not appear to use strictly parameterized queries (missing '?' or ':name' placeholders)."

    # Check if sqlite3 is imported
    assert 'sqlite3' in content, "Script does not appear to import sqlite3."