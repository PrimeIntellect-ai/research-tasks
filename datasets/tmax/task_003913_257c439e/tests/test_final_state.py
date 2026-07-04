# test_final_state.py
import os
import json
import pytest

def test_analyze_py_exists():
    file_path = '/home/user/analyze.py'
    assert os.path.isfile(file_path), f"Expected script {file_path} is missing."

def test_page2_json_valid():
    file_path = '/home/user/page2.json'
    assert os.path.isfile(file_path), f"Expected output file {file_path} is missing."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not valid JSON.")

    assert isinstance(data, list), f"Expected JSON in {file_path} to be a list of objects."

    expected_data = [
        {"id": 4, "name": "David", "dept_name": "Engineering", "salary": 80000, "depth": 2},
        {"id": 9, "name": "Ivan", "dept_name": "Executive", "salary": 75000, "depth": 2},
        {"id": 16, "name": "Victor", "dept_name": "Engineering", "salary": 71000, "depth": 2},
        {"id": 6, "name": "Frank", "dept_name": "Sales", "salary": 60000, "depth": 2},
        {"id": 8, "name": "Heidi", "dept_name": "Marketing", "salary": 55000, "depth": 2}
    ]

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} records in {file_path}, but got {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert isinstance(actual, dict), f"Record at index {i} is not a JSON object."
        for key in ["id", "name", "dept_name", "salary", "depth"]:
            assert key in actual, f"Record at index {i} is missing key '{key}'."
            assert actual[key] == expected[key], f"Mismatch at index {i} for key '{key}': expected {expected[key]}, got {actual[key]}."

def test_query_plan_txt_valid():
    file_path = '/home/user/query_plan.txt'
    assert os.path.isfile(file_path), f"Expected output file {file_path} is missing."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert len(content) > 0, f"File {file_path} is empty."
    # The output of EXPLAIN QUERY PLAN typically contains words like SCAN, SEARCH, or USE TEMP B-TREE
    assert any(keyword in content.upper() for keyword in ["SCAN", "SEARCH", "COROUTINE", "CTE", "B-TREE", "COMPOUND"]), \
        f"File {file_path} does not appear to contain a valid EXPLAIN QUERY PLAN output."