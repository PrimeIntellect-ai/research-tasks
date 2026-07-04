# test_final_state.py

import os
import json
import pytest

def test_analyze_go_exists():
    go_file = "/home/user/analyze.go"
    assert os.path.isfile(go_file), f"Expected Go source file is missing at {go_file}"

def test_anomalies_json_exists_and_correct():
    json_file = "/home/user/anomalies.json"
    assert os.path.isfile(json_file), f"Expected JSON output file is missing at {json_file}"

    with open(json_file, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_file} does not contain valid JSON.")

    assert isinstance(data, list), f"Expected the JSON file to contain a list, but got {type(data).__name__}"

    expected = ["2023-10-01 10:00:25"]
    assert data == expected, f"Expected anomalies list to be {expected}, but got {data}"