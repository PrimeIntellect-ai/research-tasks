# test_final_state.py

import os
import json
import pytest

def test_json_files_created():
    expected_files = [
        "/home/user/processed_notes/meeting1.json",
        "/home/user/processed_notes/tech/backend/api.json",
        "/home/user/processed_notes/personal/todo.json"
    ]
    for f in expected_files:
        assert os.path.isfile(f), f"Expected JSON file missing: {f}"

def test_no_txt_processed():
    not_expected = "/home/user/processed_notes/tech/notes.json"
    assert not os.path.exists(not_expected), f"Text files should not be processed, found: {not_expected}"

def test_json_contents():
    # Map of json path to its corresponding md path
    file_map = {
        "/home/user/processed_notes/meeting1.json": "/home/user/raw_notes/meeting1.md",
        "/home/user/processed_notes/tech/backend/api.json": "/home/user/raw_notes/tech/backend/api.md",
        "/home/user/processed_notes/personal/todo.json": "/home/user/raw_notes/personal/todo.md"
    }

    for json_path, md_path in file_map.items():
        assert os.path.isfile(json_path), f"Missing JSON file: {json_path}"
        assert os.path.isfile(md_path), f"Missing original MD file: {md_path}"

        with open(md_path, "r") as f:
            md_content = f.read()

        # Calculate expected values
        expected_words = len(md_content.split())

        expected_title = "Unknown"
        for line in md_content.splitlines():
            if line.startswith("# "):
                expected_title = line[2:].strip()
                break

        with open(json_path, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON in {json_path}")

        assert "title" in data, f"Missing 'title' key in {json_path}"
        assert "content" in data, f"Missing 'content' key in {json_path}"
        assert "words" in data, f"Missing 'words' key in {json_path}"

        assert data["title"] == expected_title, f"Incorrect title in {json_path}. Expected {expected_title}, got {data['title']}"
        assert data["content"] == md_content, f"Incorrect content in {json_path}."
        assert data["words"] == expected_words, f"Incorrect word count in {json_path}. Expected {expected_words}, got {data['words']}"

def test_log_file():
    log_path = "/home/user/files_processed.log"
    assert os.path.isfile(log_path), f"Log file missing: {log_path}"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "/home/user/processed_notes/meeting1.json",
        "/home/user/processed_notes/personal/todo.json",
        "/home/user/processed_notes/tech/backend/api.json"
    ]
    expected_lines.sort()

    assert lines == expected_lines, f"Log file content incorrect or not sorted properly. Expected {expected_lines}, got {lines}"