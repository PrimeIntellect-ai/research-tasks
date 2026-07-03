# test_final_state.py
import os
import sqlite3
import json
import subprocess

DB_PATH = "/home/user/ecommerce.db"
SCRIPT_PATH = "/home/user/analyze.sh"
REPORT_PATH = "/home/user/report.json"

def test_database_exists():
    assert os.path.isfile(DB_PATH), f"{DB_PATH} does not exist"

def test_tables_exist():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()

    assert "customers" in tables, "Table 'customers' is missing"
    assert "products" in tables, "Table 'products' is missing"
    assert "transactions" in tables, "Table 'transactions' is missing"

def test_indexes_exist():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index';")
    indexes = [row[0] for row in cursor.fetchall()]
    conn.close()

    assert "idx_transactions_date" in indexes, "Index 'idx_transactions_date' is missing"
    assert "idx_products_category" in indexes, "Index 'idx_products_category' is missing"
    assert "idx_transactions_customer" in indexes, "Index 'idx_transactions_customer' is missing"

def test_script_executable_and_runs():
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} does not exist"
    assert os.access(SCRIPT_PATH, os.X_OK), f"{SCRIPT_PATH} is not executable"

    # Remove report.json if it exists to ensure the script creates it
    if os.path.exists(REPORT_PATH):
        os.remove(REPORT_PATH)

    result = subprocess.run([SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to run. Return code: {result.returncode}, Stderr: {result.stderr}"
    assert os.path.isfile(REPORT_PATH), f"Script did not create {REPORT_PATH}"

def test_report_json_content():
    # If the previous test failed or was skipped, we still check if the file exists
    assert os.path.isfile(REPORT_PATH), f"{REPORT_PATH} does not exist"

    with open(REPORT_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{REPORT_PATH} does not contain valid JSON"

    expected_data = [
        {"segment": "Premium", "total_revenue": 1650.0},
        {"segment": "Standard", "total_revenue": 50.0}
    ]

    assert isinstance(data, list), "JSON output should be a list"
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} items, got {len(data)}"

    # Sort both to be safe, though the prompt requires descending total_revenue
    # We'll check the exact order as required by the prompt
    assert data == expected_data, f"JSON content is incorrect. Expected {expected_data}, got {data}"