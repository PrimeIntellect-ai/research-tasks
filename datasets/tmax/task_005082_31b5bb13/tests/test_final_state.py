# test_final_state.py
import os
import csv
import re
import pytest

OUTPUT_FILE = '/home/user/output.csv'
SCRIPT_FILE = '/home/user/process_data.py'

def test_output_csv_exists_and_correct():
    assert os.path.isfile(OUTPUT_FILE), f"The output file {OUTPUT_FILE} was not created."

    with open(OUTPUT_FILE, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    expected_rows = [
        ['id', 'timestamp', 'category', 'price', 'user_id'],
        ['10', '2023-01-01T10:45:00', 'electronics', '399.99', '110'],
        ['1', '2023-01-01T10:00:00', 'electronics', '299.99', '101']
    ]

    assert rows == expected_rows, f"The contents of {OUTPUT_FILE} do not match the expected output for the given arguments. Expected {expected_rows}, got {rows}."

def test_script_exists_and_contains_requirements():
    assert os.path.isfile(SCRIPT_FILE), f"The script file {SCRIPT_FILE} was not created."

    with open(SCRIPT_FILE, 'r') as f:
        content = f.read()

    # Check for index creation
    assert "idx_category_price" in content, "The script must create a composite index named 'idx_category_price'."

    # Check for parameterized queries
    # Look for execution with parameters, e.g., execute(..., (...)) or execute(..., {...})
    # Since checking AST might be complex for a simple script, we'll check for ? or : placeholders
    has_qmark = "?" in content
    has_named = re.search(r':\w+', content)
    assert has_qmark or has_named, "The script must use parameterized SQL queries (e.g., using '?' or named parameters)."

    # Check for argparse usage
    assert "argparse" in content, "The script must use the 'argparse' module."
    assert "sqlite3" in content, "The script must use the 'sqlite3' module."