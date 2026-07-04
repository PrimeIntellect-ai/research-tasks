# test_final_state.py

import os
import json
import pytest

OUTPUT_JSON = "/home/user/output.json"
GRAPH_ANALYZER_DIR = "/home/user/graph_analyzer"
CARGO_TOML = os.path.join(GRAPH_ANALYZER_DIR, "Cargo.toml")

def test_rust_project_exists():
    assert os.path.isdir(GRAPH_ANALYZER_DIR), f"Rust project directory {GRAPH_ANALYZER_DIR} is missing."
    assert os.path.isfile(CARGO_TOML), f"Cargo.toml is missing in {GRAPH_ANALYZER_DIR}."

def test_output_json_exists():
    assert os.path.isfile(OUTPUT_JSON), f"Output file {OUTPUT_JSON} was not created."

def test_output_json_content():
    assert os.path.isfile(OUTPUT_JSON), f"Output file {OUTPUT_JSON} is missing."

    with open(OUTPUT_JSON, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {OUTPUT_JSON} does not contain valid JSON.")

    expected_data = [
        {"id": "N5", "name": "StationE", "cost": 20},
        {"id": "N4", "name": "StationD", "cost": 10}
    ]

    assert isinstance(data, list), f"Expected a JSON array, but got {type(data).__name__}."
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} items, but got {len(data)}."

    # Check each item
    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert actual.get("id") == expected["id"], f"Item at index {i} has incorrect id. Expected {expected['id']}, got {actual.get('id')}."
        assert actual.get("name") == expected["name"], f"Item at index {i} has incorrect name. Expected {expected['name']}, got {actual.get('name')}."
        assert actual.get("cost") == expected["cost"], f"Item at index {i} has incorrect cost. Expected {expected['cost']}, got {actual.get('cost')}."

def test_output_json_format():
    assert os.path.isfile(OUTPUT_JSON), f"Output file {OUTPUT_JSON} is missing."

    with open(OUTPUT_JSON, "r") as f:
        content = f.read()

    # Check that it's a single line (no newlines other than a possible trailing one)
    content_stripped = content.strip()
    assert "\n" not in content_stripped, "Output JSON should be a single line, not pretty-printed."