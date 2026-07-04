# test_final_state.py
import os
import csv
import json
import sqlite3
import pytest

CSV_PATH = '/home/user/violations.csv'
DB_PATH = '/home/user/employees.db'
JSONL_PATH = '/home/user/access_logs.jsonl'

def test_csv_exists():
    assert os.path.exists(CSV_PATH), f"Output file {CSV_PATH} does not exist."

def test_csv_content():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} is missing."
    assert os.path.exists(JSONL_PATH), f"Log file {JSONL_PATH} is missing."

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT id, name, role FROM users")
    users = {row[0]: {'name': row[1], 'role': row[2]} for row in c.fetchall()}

    c.execute("SELECT role, resource FROM permissions")
    perms = set(c.fetchall())

    conn.close()

    expected_violations = []
    with open(JSONL_PATH, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            log = json.loads(line)
            user_id = log['user_id']
            resource = log['resource']
            timestamp = log['timestamp']

            user = users.get(user_id)
            if not user:
                continue

            role = user['role']
            name = user['name']

            if (role, resource) not in perms:
                expected_violations.append({
                    'timestamp': timestamp,
                    'user_id': str(user_id),
                    'name': name,
                    'role': role,
                    'resource': resource
                })

    expected_violations.sort(key=lambda x: x['timestamp'])

    with open(CSV_PATH, 'r', newline='') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail("CSV file is empty.")

        assert header == ['timestamp', 'user_id', 'name', 'role', 'resource'], \
            f"CSV header is incorrect: {header}"

        rows = list(reader)
        assert len(rows) == len(expected_violations), \
            f"Expected {len(expected_violations)} violations, found {len(rows)}."

        for i, (row, expected) in enumerate(zip(rows, expected_violations)):
            assert row[0] == expected['timestamp'], f"Row {i+1} timestamp mismatch: expected {expected['timestamp']}, got {row[0]}"
            assert row[1] == expected['user_id'], f"Row {i+1} user_id mismatch: expected {expected['user_id']}, got {row[1]}"
            assert row[2] == expected['name'], f"Row {i+1} name mismatch: expected {expected['name']}, got {row[2]}"
            assert row[3] == expected['role'], f"Row {i+1} role mismatch: expected {expected['role']}, got {row[3]}"
            assert row[4] == expected['resource'], f"Row {i+1} resource mismatch: expected {expected['resource']}, got {row[4]}"