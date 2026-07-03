# test_final_state.py

import os
import json
import pytest

def test_settings_chunks_directory_exists():
    """Verify that the settings_chunks directory was created."""
    target_dir = "/home/user/settings_chunks"
    assert os.path.isdir(target_dir), f"Directory {target_dir} is missing. The script did not create it or created it in the wrong place."

def test_settings_chunks_files_exist():
    """Verify that exactly the expected chunk files exist in the directory."""
    target_dir = "/home/user/settings_chunks"
    assert os.path.isdir(target_dir), "Target directory missing."

    files = set(os.listdir(target_dir))
    expected_files = {"chunk_1.json", "chunk_2.json", "chunk_3.json"}

    assert files == expected_files, f"Expected exactly files {expected_files} in {target_dir}, but found {files}."

def test_settings_chunks_content_and_format():
    """Verify the parsed contents and formatting of each chunk file."""
    target_dir = "/home/user/settings_chunks"

    expected_data = {
        "chunk_1.json": {"debug": "false", "host": "127.0.0.1"},
        "chunk_2.json": {"mode": "silent", "port": "9090"},
        "chunk_3.json": {"retry": "5", "timeout": "30"}
    }

    for filename, expected_json in expected_data.items():
        filepath = os.path.join(target_dir, filename)
        assert os.path.isfile(filepath), f"File {filepath} is missing."

        with open(filepath, "r") as f:
            raw_content = f.read()

        try:
            parsed_json = json.loads(raw_content)
        except json.JSONDecodeError:
            pytest.fail(f"File {filename} does not contain valid JSON.")

        assert parsed_json == expected_json, f"Content of {filename} is incorrect. Expected {expected_json}, got {parsed_json}."

        # Check formatting (2 spaces for indentation)
        # We can do this by dumping the parsed JSON with indent=2 and comparing to the raw content (ignoring trailing newlines)
        expected_raw = json.dumps(expected_json, indent=2)
        assert raw_content.strip() == expected_raw.strip(), f"File {filename} is not formatted with exactly 2 spaces of indentation as expected."