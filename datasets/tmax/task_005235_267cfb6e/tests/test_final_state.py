# test_final_state.py

import os
import json
import pytest

def test_process_sales_script_exists():
    script_path = "/home/user/process_sales.py"
    assert os.path.isfile(script_path), f"Expected script {script_path} is missing."

def test_output_file_exists():
    output_path = "/home/user/high_value_active_sales.jsonl"
    assert os.path.isfile(output_path), f"Expected output file {output_path} is missing."

def test_output_file_content():
    output_path = "/home/user/high_value_active_sales.jsonl"
    assert os.path.isfile(output_path), f"Cannot check content, {output_path} is missing."

    expected = [
        {"transaction_id": "T1001", "user": "U99", "category": "Electronics", "total_value": 150.0},
        {"transaction_id": "T1004", "user": "U45", "category": "Home", "total_value": 120.5},
        {"transaction_id": "T1006", "user": "U88", "category": "Home", "total_value": 130.0}
    ]

    with open(output_path, 'r') as f:
        lines = f.read().strip().split('\n')

    # Filter out any empty lines just in case
    lines = [line for line in lines if line.strip()]

    assert len(lines) == len(expected), f"Expected {len(expected)} lines in the output, but got {len(lines)}."

    parsed = []
    for i, line in enumerate(lines):
        try:
            parsed.append(json.loads(line))
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} is not valid JSON: {line}")

    for i, (p, e) in enumerate(zip(parsed, expected)):
        assert p == e, f"Mismatch at line {i+1}:\nExpected: {e}\nGot: {p}"