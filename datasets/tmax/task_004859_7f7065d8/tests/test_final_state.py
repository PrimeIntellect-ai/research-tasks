# test_final_state.py

import os
import json
import subprocess
import pytest

def test_output_json_exists():
    """Check if the output.json file was created."""
    output_path = "/home/user/output.json"
    assert os.path.isfile(output_path), f"Output file missing: {output_path}"

def test_output_json_content():
    """Check if the output.json contains the correct parsed events."""
    output_path = "/home/user/output.json"
    assert os.path.isfile(output_path), f"Output file missing: {output_path}"

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("output.json is not valid JSON")

    assert isinstance(data, list), "output.json should contain a JSON array"

    expected = [
        {"code": 200, "data": "login_success"},
        {"code": 150, "data": "processing"}
    ]

    assert len(data) == len(expected), f"Expected {len(expected)} events, but got {len(data)}"

    for i, expected_event in enumerate(expected):
        assert data[i] == expected_event, f"Event at index {i} mismatch: expected {expected_event}, got {data[i]}"

def test_libfilter_so_is_shared_object():
    """Check if libfilter.so was built as a shared object."""
    lib_path = "/home/user/pipeline/c_src/libfilter.so"
    assert os.path.isfile(lib_path), f"Shared library missing: {lib_path}"

    # Use the 'file' command to check if it's a shared object
    result = subprocess.run(["file", lib_path], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to run 'file' command"

    output = result.stdout.lower()
    assert "shared object" in output, f"libfilter.so is not a shared object. 'file' output: {output}"

def test_rust_binary_compiled():
    """Check if the Rust binary was compiled successfully."""
    # Since they ran `cargo run`, the binary should exist in the target/debug directory
    binary_path = "/home/user/pipeline/rust_src/target/debug/parser"
    assert os.path.isfile(binary_path), "Rust binary was not compiled successfully (expected at target/debug/parser)"