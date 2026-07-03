# test_final_state.py

import os
import csv
import requests

def test_csv_exists_and_format():
    csv_path = "/home/user/processed_graph.csv"
    assert os.path.isfile(csv_path), f"Processed CSV file {csv_path} does not exist. Did you create it?"

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            assert False, f"CSV file {csv_path} is empty."

        expected_header = ['backup_id', 'parent_backup_id', 'size_bytes', 'status']
        assert header == expected_header, f"Incorrect CSV header. Expected {expected_header}, got {header}"

        rows = list(reader)
        assert len(rows) == 5, f"Expected 5 data rows in CSV, found {len(rows)}."

        # Check a couple of rows to ensure correct mapping
        assert rows[0] == ['bck_001', '', '1024', 'SUCCESS'], f"Incorrect first row mapping: {rows[0]}"
        assert rows[1] == ['bck_002', 'bck_001', '2048', 'SUCCESS'], f"Incorrect second row mapping: {rows[1]}"

def test_server_endpoints():
    base_url = "http://127.0.0.1:9090/lineage/"

    # Check if server is reachable
    try:
        requests.get(base_url + "bck_001", timeout=3)
    except requests.exceptions.RequestException as e:
        assert False, f"Server is not reachable on 127.0.0.1:9090. Exception: {e}"

    test_cases = {
        "bck_001": [],
        "bck_002": ["bck_001"],
        "bck_004": ["bck_003", "bck_002", "bck_001"]
    }

    for b_id, expected in test_cases.items():
        resp = requests.get(base_url + b_id, timeout=3)
        assert resp.status_code == 200, f"Expected HTTP 200 for {b_id}, got {resp.status_code}. Response body: {resp.text}"

        try:
            data = resp.json()
        except ValueError:
            assert False, f"Response for {b_id} is not valid JSON. Response body: {resp.text}"

        assert isinstance(data, list), f"Expected a JSON array response for {b_id}, got {type(data).__name__}"

        # Compare as sets since graph traversal order might vary
        assert set(data) == set(expected), f"Expected lineage ancestors {expected} for {b_id}, got {data}"