# test_final_state.py

import os
import json
import re
import pytest

def test_v2_proto_exists_and_migrated():
    """Test that the v2 proto file exists and has the correct schema migrations."""
    v2_proto = "/home/user/src/protos/v2/user.proto"
    assert os.path.isfile(v2_proto), f"Failed: v2 proto file {v2_proto} does not exist."

    with open(v2_proto, 'r') as f:
        content = f.read()

    # Check package update
    assert re.search(r"package\s+v2\s*;", content), "Failed: package not updated to v2 in v2/user.proto"

    # Check user_id migrated to string
    assert re.search(r"string\s+user_id\s*=\s*1\s*;", content), "Failed: user_id not migrated to string in v2/user.proto"

    # Check group_id migrated to string
    assert re.search(r"string\s+group_id\s*=\s*3\s*;", content), "Failed: group_id not migrated to string in v2/user.proto"

    # Check age is still int32
    assert re.search(r"int32\s+age\s*=\s*5\s*;", content), "Failed: age was modified but shouldn't have been in v2/user.proto"

def test_proto_index():
    """Test that the proto index file contains the correct sorted paths."""
    index_file = "/home/user/proto_index.txt"
    assert os.path.isfile(index_file), f"Failed: index file {index_file} does not exist."

    with open(index_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "/home/user/src/protos/v1/user.proto",
        "/home/user/src/protos/v2/user.proto"
    ]

    # The list must be sorted alphabetically and match the expected exact paths
    assert lines == sorted(expected_lines), f"Failed: {index_file} does not contain the expected sorted paths. Got: {lines}"

def test_ws_mock_stream():
    """Test that the WebSocket mock stream file is valid JSONL and has correct data."""
    mock_file = "/home/user/ws_mock_stream.jsonl"
    assert os.path.isfile(mock_file), f"Failed: mock stream file {mock_file} does not exist."

    with open(mock_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Failed: {mock_file} should contain exactly 3 lines of JSON."

    expected_data = [
        {"user_id": "uuid-1", "username": "alpha", "group_id": "group-1", "is_active": True},
        {"user_id": "uuid-2", "username": "beta", "group_id": "group-2", "is_active": False},
        {"user_id": "uuid-3", "username": "gamma", "group_id": "group-3", "is_active": True}
    ]

    for i, (line, expected) in enumerate(zip(lines, expected_data), 1):
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Failed: Line {i} in {mock_file} is not valid JSON.")

        assert parsed == expected, f"Failed: JSON row {i} incorrect. Expected {expected}, got {parsed}"