# test_final_state.py

import os
import json
import pytest

SCRIPT_PATH = '/home/user/analyze_backups.py'
OUTPUT_JSON_PATH = '/home/user/failed_chains_page2.json'

def test_script_exists_and_uses_not_indexed():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

    with open(SCRIPT_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "NOT INDEXED" in content.upper(), "The script must contain 'NOT INDEXED' to bypass the corrupted index."

def test_output_json_exists_and_correct():
    assert os.path.isfile(OUTPUT_JSON_PATH), f"Output JSON file not found at {OUTPUT_JSON_PATH}"

    with open(OUTPUT_JSON_PATH, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File at {OUTPUT_JSON_PATH} is not valid JSON.")

    expected_data = [[7, 8, 9], [4, 5, 6]]

    assert data == expected_data, f"JSON output mismatch. Expected {expected_data}, but got {data}"