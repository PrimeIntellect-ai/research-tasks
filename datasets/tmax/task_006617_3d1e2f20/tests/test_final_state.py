# test_final_state.py
import os
import json
import pytest
from collections import defaultdict

def test_critical_backups_log():
    json_path = "/home/user/backup_query_result.json"
    log_path = "/home/user/critical_backups.log"

    assert os.path.isfile(json_path), f"Input file {json_path} is missing."

    # Dynamically compute the expected output from the JSON file
    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON")

    in_degrees = defaultdict(int)
    for result in data.get("results", []):
        for data_item in result.get("data", []):
            for row in data_item.get("row", []):
                if row.get("type") == "DEPENDS_ON":
                    target = row.get("target")
                    if target:
                        in_degrees[target] += 1

    # Sort descending by count, then ascending by name
    sorted_dbs = sorted(in_degrees.items(), key=lambda x: (-x[1], x[0]))
    top_3 = sorted_dbs[:3]

    expected_lines = []
    for i, (db_name, count) in enumerate(top_3, 1):
        expected_lines.append(f"{i}. {db_name} - {count} dependencies")

    assert os.path.isfile(log_path), f"Output file {log_path} is missing. Did you run the C++ program?"

    with open(log_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), (
        f"Expected {len(expected_lines)} lines in {log_path}, but found {len(actual_lines)}."
    )

    for i, (expected, actual) in enumerate(zip(expected_lines, actual_lines)):
        assert actual == expected, (
            f"Line {i+1} mismatch in {log_path}.\nExpected: '{expected}'\nActual: '{actual}'"
        )