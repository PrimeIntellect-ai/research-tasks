# test_final_state.py

import os
import sqlite3
import pytest

def test_sql_files_exist():
    assert os.path.isfile("/home/user/query.sql"), "/home/user/query.sql is missing."
    assert os.path.isfile("/home/user/optimize.sql"), "/home/user/optimize.sql is missing."

def test_cpp_files_and_executable_exist():
    assert os.path.isfile("/home/user/report_generator.cpp"), "/home/user/report_generator.cpp is missing."
    assert os.path.isfile("/home/user/report_generator"), "/home/user/report_generator executable is missing."
    assert os.access("/home/user/report_generator", os.X_OK), "/home/user/report_generator is not executable."

def test_indexes_created():
    db_path = "/home/user/ecommerce.db"
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index';")
    indexes = cursor.fetchall()
    conn.close()

    assert len(indexes) >= 2, f"Expected at least 2 indexes to be created, but found {len(indexes)}."

def test_csv_output_exact_match():
    csv_path = "/home/user/top_products.csv"
    assert os.path.isfile(csv_path), f"CSV output file {csv_path} is missing."

    with open(csv_path, "r") as f:
        # Read lines and strip trailing whitespace/newlines
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "category_name,product_name,revenue,rank",
        "Books,Sci-Fi Novel,150.00,1",
        "Books,History Book,44.00,2",
        "Clothing,Jacket,120.00,1",
        "Electronics,Laptop,1999.98,1",
        "Electronics,Monitor,600.00,2"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in CSV, got {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Mismatch at line {i+1}. Expected '{expected}', got '{actual}'."