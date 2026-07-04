# test_final_state.py

import os
import re
import sqlite3
import pytest

def test_output_csv_content():
    output_csv_path = "/home/user/output.csv"
    assert os.path.isfile(output_csv_path), f"{output_csv_path} is missing."

    with open(output_csv_path, "r") as f:
        content = f.read().strip()

    expected_content = "src,dst\n1,5\n2,4\n3,5\n4,6"
    assert content == expected_content, f"The content of {output_csv_path} does not match the expected output. Got:\n{content}"

def test_cpp_file_modifications():
    cpp_path = "/home/user/project_graph.cpp"
    assert os.path.isfile(cpp_path), f"{cpp_path} is missing."

    with open(cpp_path, "r") as f:
        content = f.read().lower()

    assert "limit" in content and "offset" in content, "The C++ program does not appear to implement pagination using LIMIT and OFFSET."

    # Check for loop constructs (while or for)
    assert re.search(r'\b(while|for)\b', content), "The C++ program does not appear to contain a loop construct for pagination."

def test_fixed_query_sql_exists():
    sql_path = "/home/user/fixed_query.sql"
    assert os.path.isfile(sql_path), f"{sql_path} is missing."

def test_query_plan_exists_and_content():
    plan_path = "/home/user/query_plan.txt"
    assert os.path.isfile(plan_path), f"{plan_path} is missing."

    with open(plan_path, "r") as f:
        content = f.read().upper()

    assert "SCAN" in content or "SEARCH" in content, f"The query plan in {plan_path} does not contain expected EXPLAIN QUERY PLAN output like SCAN or SEARCH."