# test_final_state.py
import os
import json
import pytest

def test_regional_sales_report_json():
    path = "/home/user/regional_sales_report.json"
    assert os.path.isfile(path), f"File not found: {path}"

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} does not contain valid JSON.")

    expected_data = [
        {"region": "East", "category": "Electronics", "total_sales": 600.0},
        {"region": "North", "category": "Electronics", "total_sales": 500.0},
        {"region": "North", "category": "Home", "total_sales": 100.0},
        {"region": "South", "category": "Clothing", "total_sales": 50.0},
        {"region": "South", "category": "Electronics", "total_sales": 150.0},
        {"region": "West", "category": "Clothing", "total_sales": 45.0}
    ]

    # Sort both lists by region and category to compare
    def sort_key(x):
        return (x.get("region", ""), x.get("category", ""))

    assert sorted(data, key=sort_key) == sorted(expected_data, key=sort_key), "JSON data does not match the expected aggregated results."

def test_query_plan_txt():
    path = "/home/user/query_plan.txt"
    assert os.path.isfile(path), f"File not found: {path}"

    with open(path, "r") as f:
        content = f.read().upper()

    # EXPLAIN QUERY PLAN output should contain keywords like SCAN, SEARCH, or COVERING INDEX
    assert any(keyword in content for keyword in ["SCAN", "SEARCH", "COVERING INDEX", "USE TEMP B-TREE", "LIST SUBQUERY"]), "query_plan.txt does not appear to contain valid EXPLAIN QUERY PLAN output."

def test_generate_report_script_indexes():
    path = "/home/user/generate_report.py"
    assert os.path.isfile(path), f"File not found: {path}"

    with open(path, "r") as f:
        content = f.read().upper()

    assert "CREATE INDEX" in content, "generate_report.py is missing CREATE INDEX statement(s)."
    assert "SALES" in content, "generate_report.py does not seem to reference the sales table in the index creation."