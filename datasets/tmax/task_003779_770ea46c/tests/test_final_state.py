# test_final_state.py
import os
import json

def test_buggy_line_file():
    buggy_file = "/home/user/buggy_line.txt"
    assert os.path.exists(buggy_file), f"File {buggy_file} does not exist."

    with open(buggy_file, "r") as f:
        content = f.read().strip()

    expected = "192.168.1.100 - [2023-10-12T10:00:00Z] - GET - /api/status"
    assert content == expected, f"Contents of {buggy_file} do not match the expected malformed line."

def test_output_jsonl_file():
    output_file = "/home/user/output.jsonl"
    assert os.path.exists(output_file), f"File {output_file} does not exist."

    with open(output_file, "r") as f:
        lines = f.readlines()

    assert len(lines) == 4999, f"Expected exactly 4999 lines in {output_file}, but found {len(lines)}."

    for i, line in enumerate(lines):
        assert "192.168.1.100" not in line, f"Malformed line IP '192.168.1.100' found in {output_file} at line {i+1}."

        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            assert False, f"Line {i+1} in {output_file} is not valid JSON."

        assert "ip" in record, f"Missing 'ip' field in JSON record at line {i+1}."
        assert "timestamp" in record, f"Missing 'timestamp' field in JSON record at line {i+1}."
        assert "method" in record, f"Missing 'method' field in JSON record at line {i+1}."
        assert "path" in record, f"Missing 'path' field in JSON record at line {i+1}."
        assert "status" in record, f"Missing 'status' field in JSON record at line {i+1}."