# test_final_state.py

import os
import json
import pytest

def test_decoded_files_exist():
    temp_dir = "/home/user/temp"
    expected_files = ["decoded_us.csv", "decoded_de.csv", "decoded_jp.csv"]

    for filename in expected_files:
        filepath = os.path.join(temp_dir, filename)
        assert os.path.isfile(filepath), f"Phase 1 failed: Expected intermediate file {filepath} is missing."

def test_aligned_files_exist():
    temp_dir = "/home/user/temp"
    expected_files = ["aligned_us.csv", "aligned_de.csv", "aligned_jp.csv"]

    for filename in expected_files:
        filepath = os.path.join(temp_dir, filename)
        assert os.path.isfile(filepath), f"Phase 2 failed: Expected intermediate file {filepath} is missing."

def test_final_output_exists_and_minified():
    filepath = "/home/user/final_output.json"
    assert os.path.isfile(filepath), f"Phase 3 failed: Final output file {filepath} is missing."

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    assert content.strip() != "", f"Final output file {filepath} is empty."

    # Check for minification (no newlines or unnecessary spaces)
    # A simple check: no newlines in the file content
    assert "\n" not in content.strip(), f"Final output file {filepath} must be minified (no extra whitespace or newlines)."

def test_final_output_content_and_ordering():
    filepath = "/home/user/final_output.json"
    assert os.path.isfile(filepath), f"Final output file {filepath} is missing."

    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Final output file {filepath} is not valid JSON.")

    assert isinstance(data, list), f"Final output must be a JSON array, got {type(data).__name__}."

    expected_data = [
        {"timestamp": "2023-12-31T21:00:00Z", "key": "login_btn", "comment": "Anmelden ist verwirrend"},
        {"timestamp": "2023-12-31T22:00:00Z", "key": "login_btn", "comment": "ログインがわかりにくい"},
        {"timestamp": "2024-01-01T00:30:00Z", "key": "login_btn", "comment": "Login is confusing"},
        {"timestamp": "2024-01-01T09:00:00Z", "key": "logout_btn", "comment": "Funktioniert gut"},
        {"timestamp": "2024-01-01T09:30:00Z", "key": "logout_btn", "comment": "よく機能する"},
        {"timestamp": "2024-01-01T17:15:00Z", "key": "logout_btn", "comment": "Works well"}
    ]

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} records in final output, but found {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert actual.get("timestamp") == expected["timestamp"], f"Record {i} timestamp mismatch. Expected {expected['timestamp']}, got {actual.get('timestamp')}."
        assert actual.get("key") == expected["key"], f"Record {i} key mismatch. Expected {expected['key']}, got {actual.get('key')}."
        assert actual.get("comment") == expected["comment"], f"Record {i} comment mismatch. Expected {expected['comment']}, got {actual.get('comment')}."