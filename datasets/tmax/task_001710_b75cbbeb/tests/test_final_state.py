# test_final_state.py
import os
import csv

def test_pipeline_log_exists():
    assert os.path.isfile("/home/user/pipeline.log"), "/home/user/pipeline.log is missing."

def test_pipeline_log_content():
    expected_log = [
        "[INFO] Initial records: 6",
        "[INFO] Duplicates removed: 2",
        "[INFO] Missing scores interpolated: 1",
        "[INFO] Final records: 4"
    ]
    with open("/home/user/pipeline.log", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_log, f"Log file contents do not match expected. Got: {lines}"

def test_clean_data_exists():
    assert os.path.isfile("/home/user/clean_data.csv"), "/home/user/clean_data.csv is missing."

def test_clean_data_content():
    with open("/home/user/clean_data.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 4, f"Expected 4 data rows in clean_data.csv, got {len(rows)}"

    # Check headers
    expected_headers = ['id', 'timestamp', 'user_name', 'email', 'score', 'retry_run_id', 'email_domain']
    assert set(expected_headers).issubset(set(reader.fieldnames)), f"Missing expected headers. Got: {reader.fieldnames}"

    # Sort rows by id to match the expected sorted order
    rows.sort(key=lambda x: int(x['id']))

    # Check ID 1
    assert rows[0]['id'] == '1'
    assert rows[0]['user_name'] == 'René', f"Expected 'René', got '{rows[0]['user_name']}'"
    assert float(rows[0]['score']) == 85.0
    assert rows[0]['email_domain'] == 'example.com'

    # Check ID 2
    assert rows[1]['id'] == '2'
    assert rows[1]['user_name'] == 'José', f"Expected 'José', got '{rows[1]['user_name']}'"
    assert float(rows[1]['score']) == 90.0, f"Expected interpolated score 90.0, got {rows[1]['score']}"
    assert rows[1]['email_domain'] == 'test.org'

    # Check ID 3
    assert rows[2]['id'] == '3'
    assert rows[2]['user_name'] == 'Alice'
    assert float(rows[2]['score']) == 95.0
    assert rows[2]['email_domain'] == 'domain.com'

    # Check ID 4
    assert rows[3]['id'] == '4'
    assert rows[3]['user_name'] == 'Bob'
    assert float(rows[3]['score']) == 100.0
    assert rows[3]['email_domain'] == 'test.org'