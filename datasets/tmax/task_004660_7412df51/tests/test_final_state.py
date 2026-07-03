# test_final_state.py

import os
import pytest

def test_total_sales_csv_content():
    file_path = "/home/user/total_sales.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} does not exist. Did you run the program?"

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_content = """emp_id,total_sales
1,1350
2,550
3,700
4,300
5,50
6,550
7,150"""

    assert content == expected_content, f"Content of {file_path} does not match the expected aggregated sales data."

def test_query_result_txt_content():
    file_path = "/home/user/query_result.txt"
    assert os.path.isfile(file_path), f"Output file {file_path} does not exist. Did you run the program with --target-id 2?"

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == "550", f"Content of {file_path} does not match the expected query result for Employee 2. Expected '550', got '{content}'."

def test_source_and_binary_exist():
    source_path = "/home/user/aggregate.cpp"
    binary_path = "/home/user/aggregate"

    assert os.path.isfile(source_path), f"Source file {source_path} does not exist."
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"File {binary_path} is not executable."