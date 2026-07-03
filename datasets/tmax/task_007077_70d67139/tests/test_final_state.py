# test_final_state.py
import os
import csv
import sqlite3

def test_csv_exists_and_correct():
    """Verify that the CSV file is created with the correct content."""
    csv_path = '/home/user/critical_services.csv'
    assert os.path.exists(csv_path), f"The output CSV file {csv_path} is missing."
    assert os.path.isfile(csv_path), f"{csv_path} is not a file."

    expected_rows = [
        {'rank': '1', 'service_id': '4', 'service_name': 'user_db', 'dependent_count': '6'},
        {'rank': '2', 'service_id': '3', 'service_name': 'auth_service', 'dependent_count': '4'},
        {'rank': '2', 'service_id': '8', 'service_name': 'product_db', 'dependent_count': '4'},
        {'rank': '3', 'service_id': '7', 'service_name': 'inventory_service', 'dependent_count': '2'},
        {'rank': '4', 'service_id': '2', 'service_name': 'api_gateway', 'dependent_count': '1'},
        {'rank': '4', 'service_id': '5', 'service_name': 'payment_service', 'dependent_count': '1'}
    ]

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ['rank', 'service_id', 'service_name', 'dependent_count'], "CSV headers are incorrect."
        actual_rows = list(reader)

    # Sort both lists to compare them regardless of tie-breaker ordering
    expected_rows_sorted = sorted(expected_rows, key=lambda x: (int(x['rank']), int(x['service_id'])))

    try:
        actual_rows_sorted = sorted(actual_rows, key=lambda x: (int(x['rank']), int(x['service_id'])))
    except (ValueError, KeyError) as e:
        assert False, f"CSV contains invalid data types or missing columns: {e}"

    assert actual_rows_sorted == expected_rows_sorted, f"CSV contents do not match the expected top critical services. Expected: {expected_rows_sorted}, Got: {actual_rows_sorted}"

def test_indexes_created():
    """Verify that indexes were applied to the dependencies table to optimize hierarchical querying."""
    db_path = '/home/user/services.db'
    assert os.path.exists(db_path), f"The database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='dependencies'")
    indexes = cursor.fetchall()
    conn.close()

    assert len(indexes) > 0, "No indexes were created on the 'dependencies' table to optimize hierarchical querying."

def test_analyze_script_exists():
    """Verify that the analyze script was created."""
    script_path = '/home/user/analyze.py'
    assert os.path.exists(script_path), f"The script file {script_path} is missing."
    assert os.path.isfile(script_path), f"{script_path} is not a file."