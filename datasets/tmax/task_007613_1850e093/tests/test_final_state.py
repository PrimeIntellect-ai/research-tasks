# test_final_state.py

import os
import pytest

def test_api_proto_exists():
    proto_path = "/home/user/service/api.proto"
    assert os.path.isfile(proto_path), f"Protobuf file {proto_path} is missing."

    with open(proto_path, "r") as f:
        content = f.read()
        assert "syntax" in content and "proto3" in content, "Missing syntax = 'proto3' in proto file."
        assert "package api;" in content, "Missing package declaration in proto file."
        assert "ProcessString" in content, "Missing ProcessString RPC method."
        assert "StringRequest" in content, "Missing StringRequest message."
        assert "StringResponse" in content, "Missing StringResponse message."

def test_go_server_exists():
    go_path = "/home/user/service/main.go"
    assert os.path.isfile(go_path), f"Go server file {go_path} is missing."

def test_rust_tool_compiled():
    tool_path = "/home/user/formatter/format_tool"
    assert os.path.isfile(tool_path), f"Compiled Rust tool {tool_path} is missing."
    assert os.access(tool_path, os.X_OK), f"Rust tool {tool_path} is not executable."

def test_final_result():
    result_path = "/home/user/final_result.txt"
    assert os.path.isfile(result_path), f"Final result file {result_path} is missing."

    # Derive expected result based on legacy Python logic
    original_string = "legacy_python_code"
    reversed_s = original_string[::-1]
    shifted_s = "".join(chr(ord(char) + 1) for char in reversed_s)
    expected_result = f"{shifted_s} [MIGRATED]"

    with open(result_path, "r") as f:
        actual_result = f.read().strip()

    assert actual_result == expected_result, f"Expected final result '{expected_result}', but got '{actual_result}'."