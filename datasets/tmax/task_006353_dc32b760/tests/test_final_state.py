# test_final_state.py

import os
import json
import math
import pytest

def test_makefile_exists():
    assert os.path.isfile("/home/user/Makefile"), "Makefile is missing in /home/user/"

def test_warehouse_db_exists():
    assert os.path.isfile("/home/user/data/warehouse.db"), "warehouse.db is missing in /home/user/data/"

def test_final_output_jsonl():
    output_file = "/home/user/data/final_output.jsonl"
    assert os.path.isfile(output_file), f"{output_file} is missing. Did the ETL pipeline run and produce the file?"

    expected = [
        {"id": 1, "city": "NewYork", "ts": "2023-01-01", "val": 10.0, "rolling_avg": 10.00},
        {"id": 1, "city": "NewYork", "ts": "2023-01-02", "val": 12.0, "rolling_avg": 11.00},
        {"id": 1, "city": "NewYork", "ts": "2023-01-03", "val": 14.0, "rolling_avg": 12.00},
        {"id": 1, "city": "NewYork", "ts": "2023-01-04", "val": 16.0, "rolling_avg": 14.00},
        {"id": 1, "city": "NewYork", "ts": "2023-01-05", "val": 10.0, "rolling_avg": 13.33},
        {"id": 2, "city": "London", "ts": "2023-01-01", "val": 5.0, "rolling_avg": 5.00},
        {"id": 2, "city": "London", "ts": "2023-01-02", "val": 6.0, "rolling_avg": 5.50},
        {"id": 2, "city": "London", "ts": "2023-01-03", "val": 7.0, "rolling_avg": 6.00},
        {"id": 2, "city": "London", "ts": "2023-01-04", "val": 8.0, "rolling_avg": 7.00},
        {"id": 2, "city": "London", "ts": "2023-01-06", "val": 11.0, "rolling_avg": 8.67},
    ]

    with open(output_file, "r") as f:
        content = f.read().strip()

    assert content, f"{output_file} is empty."

    lines = content.split("\n")
    assert len(lines) == len(expected), f"Expected {len(expected)} lines in JSONL, got {len(lines)}"

    for i, (line, exp) in enumerate(zip(lines, expected)):
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} is not valid JSON: {line}")

        # Check required keys
        for key in ["id", "city", "ts", "val", "rolling_avg"]:
            assert key in data, f"Line {i+1} is missing key '{key}'"

        assert data["id"] == exp["id"], f"Line {i+1}: expected id {exp['id']}, got {data['id']}"
        assert data["city"] == exp["city"], f"Line {i+1}: expected city '{exp['city']}', got '{data['city']}'"
        assert data["ts"] == exp["ts"], f"Line {i+1}: expected ts '{exp['ts']}', got '{data['ts']}'"
        assert math.isclose(data["val"], exp["val"], rel_tol=1e-5), f"Line {i+1}: expected val {exp['val']}, got {data['val']}"
        assert math.isclose(data["rolling_avg"], exp["rolling_avg"], abs_tol=0.01), f"Line {i+1}: expected rolling_avg {exp['rolling_avg']}, got {data['rolling_avg']}"