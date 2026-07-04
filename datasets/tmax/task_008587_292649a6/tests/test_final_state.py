# test_final_state.py

import os
import stat
import json
import csv
import math
import hashlib
import pytest

def test_run_pipeline_sh_exists_and_executable():
    path = '/home/user/run_pipeline.sh'
    assert os.path.isfile(path), f"File {path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable."

def test_artifacts_exist():
    csv_path = '/home/user/artifacts/processed_data.csv'
    json_path = '/home/user/artifacts/schema.json'
    assert os.path.isfile(csv_path), f"File {csv_path} does not exist."
    assert os.path.isfile(json_path), f"File {json_path} does not exist."

def test_schema_json():
    json_path = '/home/user/artifacts/schema.json'
    with open(json_path, 'r') as f:
        try:
            schema = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} is not a valid JSON file.")

    assert 'customer_id' in schema, "schema.json does not contain 'customer_id' key."
    dtype_str = str(schema['customer_id']).lower()
    assert 'int' in dtype_str, f"customer_id dtype is not integer, got: {dtype_str}"

def test_processed_data_csv():
    csv_path = '/home/user/artifacts/processed_data.csv'
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) > 0, "processed_data.csv is empty."
    assert 'txn_id' in rows[0], "txn_id column missing."
    assert 'customer_id' in rows[0], "customer_id column missing."
    assert 'log_transaction_value' in rows[0], "log_transaction_value column missing."

    txn_2_found = False
    txn_1_found = False

    for row in rows:
        if row['txn_id'] == '2':
            txn_2_found = True
            assert row['customer_id'] == '0', f"Missing customer_id not filled with '0', got {row['customer_id']} instead."

        if row['txn_id'] == '1':
            txn_1_found = True
            try:
                actual_log = float(row['log_transaction_value'])
            except ValueError:
                pytest.fail(f"log_transaction_value for txn_id 1 is not a valid float: {row['log_transaction_value']}")

            # transaction_value for txn_id 1 is 50.5
            expected_log = math.log(50.5 + 1)
            assert math.isclose(actual_log, expected_log, rel_tol=1e-4), \
                f"log_transaction_value calculated incorrectly for txn_id 1. Expected {expected_log}, got {actual_log}"

    assert txn_2_found, "txn_id 2 not found in processed_data.csv."
    assert txn_1_found, "txn_id 1 not found in processed_data.csv."

def test_run_log_md5():
    csv_path = '/home/user/artifacts/processed_data.csv'
    log_path = '/home/user/artifacts/run_log.txt'

    assert os.path.isfile(log_path), f"File {log_path} does not exist."

    # Calculate md5sum of the csv file
    hash_md5 = hashlib.md5()
    with open(csv_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    expected_md5 = hash_md5.hexdigest()

    with open(log_path, 'r') as f:
        log_content = f.read()

    assert expected_md5 in log_content, \
        f"run_log.txt does not contain the correct MD5 checksum of processed_data.csv. Expected {expected_md5} to be in the log."