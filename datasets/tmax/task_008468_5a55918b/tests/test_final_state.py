# test_final_state.py
import os
import sqlite3
import json

def test_index_created():
    db_path = '/home/user/data.db'
    assert os.path.isfile(db_path), f"{db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='index' AND name='idx_events_user';")
    count = cursor.fetchone()[0]
    conn.close()

    assert count == 1, "The index 'idx_events_user' was not created in the database."

def test_output_na_jsonl():
    file_path = '/home/user/output_NA.jsonl'
    assert os.path.isfile(file_path), f"{file_path} was not created."

    with open(file_path, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 2, f"Expected 2 lines in {file_path}, found {len(lines)}."

    parsed_data = []
    for line in lines:
        try:
            parsed_data.append(json.loads(line))
        except json.JSONDecodeError:
            assert False, f"Line in {file_path} is not valid JSON: {line}"

    # Sort by user_id to ensure consistent comparison
    parsed_data.sort(key=lambda x: x.get('user_id', 0))

    expected_data = [
        {"user_id": 1, "name": "Alice", "total_events": 3, "event_types": ["login", "click", "logout"]},
        {"user_id": 3, "name": "Charlie", "total_events": 2, "event_types": ["login", "purchase"]}
    ]

    assert parsed_data == expected_data, f"Data in {file_path} does not match expected output."

def test_output_eu_jsonl():
    file_path = '/home/user/output_EU.jsonl'
    assert os.path.isfile(file_path), f"{file_path} was not created."

    with open(file_path, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 2, f"Expected 2 lines in {file_path}, found {len(lines)}."

    parsed_data = []
    for line in lines:
        try:
            parsed_data.append(json.loads(line))
        except json.JSONDecodeError:
            assert False, f"Line in {file_path} is not valid JSON: {line}"

    # Sort by user_id to ensure consistent comparison
    parsed_data.sort(key=lambda x: x.get('user_id', 0))

    expected_data = [
        {"user_id": 2, "name": "Bob", "total_events": 1, "event_types": ["login"]},
        {"user_id": 4, "name": "Diana", "total_events": 2, "event_types": ["login", "click"]}
    ]

    assert parsed_data == expected_data, f"Data in {file_path} does not match expected output."

def test_summary_txt():
    file_path = '/home/user/summary.txt'
    assert os.path.isfile(file_path), f"{file_path} was not created."

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "Region: NA | Top User: Alice | Events: 3",
        "Region: EU | Top User: Diana | Events: 2"
    ]

    for expected in expected_lines:
        assert expected in lines, f"Expected summary line '{expected}' not found in {file_path}."