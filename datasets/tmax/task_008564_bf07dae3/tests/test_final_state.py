# test_final_state.py

import os
import csv
import json
import pytest

def test_pipeline_go_exists():
    assert os.path.isfile("/home/user/pipeline.go"), "/home/user/pipeline.go does not exist. You must write your Go program here."

def test_page3_json_matches_expected():
    valid_rels_path = "/home/user/data/valid_relationships.csv"
    corrupted_path = "/home/user/data/corrupted_export.csv"
    output_path = "/home/user/page3.json"

    assert os.path.isfile(output_path), f"{output_path} does not exist. Did you run your Go program?"

    # Recompute the expected valid relationships
    valid_rels = set()
    with open(valid_rels_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            valid_rels.add((row['UserID'], row['DepartmentID']))

    # Filter the corrupted export
    valid_events = []
    with open(corrupted_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (row['UserID'], row['DepartmentID']) in valid_rels:
                valid_events.append({
                    "event_id": row['EventID'],
                    "user_id": row['UserID'],
                    "department_id": row['DepartmentID'],
                    "timestamp": row['Timestamp'],
                    "action": row['Action']
                })

    # Sort by Timestamp DESC, then EventID ASC
    # Python's list.sort is stable, so we can sort by the secondary key first, then the primary key
    valid_events.sort(key=lambda x: x['event_id'])
    valid_events.sort(key=lambda x: x['timestamp'], reverse=True)

    # Pagination: Page 3, size 15 (1-based page 3 means items 31 to 45, which is index 30 to 45)
    page_size = 15
    start_idx = (3 - 1) * page_size
    end_idx = start_idx + page_size
    expected_page3 = valid_events[start_idx:end_idx]

    # Load the student's output
    with open(output_path, 'r', encoding='utf-8') as f:
        try:
            actual_page3 = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {output_path} does not contain valid JSON.")

    assert isinstance(actual_page3, list), f"Expected the output in {output_path} to be a JSON array."
    assert len(actual_page3) == len(expected_page3), f"Expected {len(expected_page3)} items in Page 3, but found {len(actual_page3)}."

    # Verify each item in the output
    for i, (actual, expected) in enumerate(zip(actual_page3, expected_page3)):
        assert actual.get("event_id") == expected["event_id"], f"Item at index {i} has incorrect event_id. Expected {expected['event_id']}, got {actual.get('event_id')}."
        assert actual.get("user_id") == expected["user_id"], f"Item at index {i} has incorrect user_id. Expected {expected['user_id']}, got {actual.get('user_id')}."
        assert actual.get("department_id") == expected["department_id"], f"Item at index {i} has incorrect department_id. Expected {expected['department_id']}, got {actual.get('department_id')}."
        assert actual.get("timestamp") == expected["timestamp"], f"Item at index {i} has incorrect timestamp. Expected {expected['timestamp']}, got {actual.get('timestamp')}."
        assert actual.get("action") == expected["action"], f"Item at index {i} has incorrect action. Expected {expected['action']}, got {actual.get('action')}."