# test_final_state.py

import os
import json
import pytest

def test_debugging_notes():
    notes_path = '/home/user/debugging_notes.txt'
    assert os.path.isfile(notes_path), f"File not found: {notes_path}"

    with open(notes_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in debugging_notes.txt, found {len(lines)}"
    assert lines[0] == "3", f"Expected first line to be '3', got '{lines[0]}'"
    assert lines[1] == "5", f"Expected second line to be '5', got '{lines[1]}'"

def test_parsed_logs_json():
    json_path = '/home/user/parsed_logs.json'
    assert os.path.isfile(json_path), f"File not found: {json_path}"

    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert isinstance(data, list), "Parsed JSON should be a list of objects."
    assert len(data) == 6, f"Expected 6 entries in JSON, found {len(data)}"

    # Check line 3 encoding fix
    line_3 = next((item for item in data if item.get("line") == 3), None)
    assert line_3 is not None, "Line 3 is missing from parsed_logs.json"
    assert "\ufffd" in line_3.get("raw", ""), "Line 3 'raw' field should contain the Unicode replacement character."

    # Check line 5 infinite loop fix
    line_5 = next((item for item in data if item.get("line") == 5), None)
    assert line_5 is not None, "Line 5 is missing from parsed_logs.json"
    tags_5 = line_5.get("tags", [])
    assert "unterminated string" in tags_5, f"Expected 'unterminated string' in line 5 tags, got {tags_5}"