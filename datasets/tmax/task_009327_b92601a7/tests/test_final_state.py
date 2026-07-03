# test_final_state.py

import os
import json
import pytest

def test_fixed_transformer_exists():
    path = "/home/user/fixed_transformer.py"
    assert os.path.isfile(path), f"Expected {path} to exist."

def test_test_input_jsonl():
    path = "/home/user/test_input.jsonl"
    assert os.path.isfile(path), f"Expected {path} to exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {path}, found {len(lines)}."

    # Check Line 1
    try:
        obj1 = json.loads(lines[0])
        assert obj1.get("id") == 1, "First line of test_input.jsonl should be valid JSON with id=1."
    except json.JSONDecodeError:
        pytest.fail("First line of test_input.jsonl must be valid JSON.")

    # Check Line 2
    try:
        json.loads(lines[1])
        pytest.fail("Second line of test_input.jsonl must be invalid/corrupted JSON.")
    except json.JSONDecodeError:
        pass

    # Check Line 3
    try:
        obj3 = json.loads(lines[2])
        assert obj3.get("id") == 3, "Third line of test_input.jsonl should be valid JSON with id=3."
    except json.JSONDecodeError:
        pytest.fail("Third line of test_input.jsonl must be valid JSON.")

def test_test_output_jsonl():
    path = "/home/user/test_output.jsonl"
    assert os.path.isfile(path), f"Expected {path} to exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {path}, found {len(lines)}."

    # We expect valid JSON in the output
    parsed_output = []
    for i, line in enumerate(lines):
        try:
            parsed_output.append(json.loads(line))
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in {path} is not valid JSON: {line}")

    # Check contents
    assert parsed_output[0] == {"id": 1, "status": "processed"}, "First output line is incorrect."
    assert parsed_output[1] == {"error": "corrupted"}, "Second output line is incorrect."
    assert parsed_output[2] == {"id": 3, "status": "processed"}, "Third output line is incorrect."