# test_final_state.py

import os
import json
import pytest

def test_extract_script_exists():
    path = "/home/user/extract.py"
    assert os.path.isfile(path), f"Expected script {path} does not exist."

def test_output_person_json():
    path = "/home/user/output_Person.json"
    assert os.path.isfile(path), f"Expected output file {path} does not exist."

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    expected_data = [
        {"connection_count": 3, "entity": "http://example.org/Alice"},
        {"connection_count": 1, "entity": "http://example.org/Bob"},
        {"connection_count": 0, "entity": "http://example.org/Charlie"}
    ]

    assert isinstance(data, list), f"Data in {path} must be a JSON array."
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} items in {path}, got {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert actual.get("entity") == expected["entity"], f"Item {i} in {path} has wrong entity. Expected {expected['entity']}, got {actual.get('entity')}."
        assert actual.get("connection_count") == expected["connection_count"], f"Item {i} in {path} has wrong connection_count. Expected {expected['connection_count']}, got {actual.get('connection_count')}."

def test_output_organization_json():
    path = "/home/user/output_Organization.json"
    assert os.path.isfile(path), f"Expected output file {path} does not exist."

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    expected_data = [
        {"connection_count": 4, "entity": "http://example.org/DataInc"},
        {"connection_count": 2, "entity": "http://example.org/TechCorp"},
        {"connection_count": 0, "entity": "http://example.org/WebLLC"}
    ]

    assert isinstance(data, list), f"Data in {path} must be a JSON array."
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} items in {path}, got {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert actual.get("entity") == expected["entity"], f"Item {i} in {path} has wrong entity. Expected {expected['entity']}, got {actual.get('entity')}."
        assert actual.get("connection_count") == expected["connection_count"], f"Item {i} in {path} has wrong connection_count. Expected {expected['connection_count']}, got {actual.get('connection_count')}."