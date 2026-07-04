# test_final_state.py

import os
import json
import pytest

def test_top_sales_json():
    file_path = "/home/user/top_sales.json"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not valid JSON.")

    expected_data = [
        {"department": "Engineering", "name": "Eve", "total_sales": 200},
        {"department": "Engineering", "name": "David", "total_sales": 200},
        {"department": "Executive", "name": "Alice", "total_sales": 1000},
        {"department": "Sales", "name": "Heidi", "total_sales": 500},
        {"department": "Sales", "name": "Grace", "total_sales": 350}
    ]

    # Sort both lists by department and then by total_sales descending, then name to ensure stable comparison
    def sort_key(x):
        return (x.get("department", ""), -x.get("total_sales", 0), x.get("name", ""))

    sorted_data = sorted(data, key=sort_key)
    sorted_expected = sorted(expected_data, key=sort_key)

    assert sorted_data == sorted_expected, f"Content of {file_path} does not match the expected top sales data."

def test_ceo_sales_txt():
    file_path = "/home/user/ceo_sales.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == "2650", f"Content of {file_path} is incorrect. Expected '2650', got '{content}'."