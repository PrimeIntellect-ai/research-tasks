# test_final_state.py

import os
import json
import pytest

def test_fuzz_test_exists():
    parser_test_path = "/home/user/log_processor/parser_test.go"
    assert os.path.isfile(parser_test_path), f"Fuzz test file {parser_test_path} is missing."

    with open(parser_test_path, "r") as f:
        content = f.read()

    assert "func Fuzz" in content, "The file parser_test.go does not contain a Fuzz test function ('func Fuzz')."

def test_processed_logs_json():
    json_path = "/home/user/processed_logs.json"
    assert os.path.isfile(json_path), f"Output JSON file {json_path} is missing."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    assert isinstance(data, list), "The JSON output should be a list of log entries."
    assert len(data) == 3, f"Expected exactly 3 valid log lines in JSON, but got {len(data)}."

def test_go_mod_updated():
    go_mod_path = "/home/user/log_processor/go.mod"
    assert os.path.isfile(go_mod_path), f"The file {go_mod_path} is missing."

    with open(go_mod_path, "r") as f:
        content = f.read()

    # The original go.mod had v1.0.0 which caused a conflict.
    # It should have been updated to a newer version (e.g., v1.1.0 or higher).
    assert "github.com/google/uuid v1.0.0" not in content, "The go.mod file still contains the outdated 'github.com/google/uuid v1.0.0' dependency. It must be updated."