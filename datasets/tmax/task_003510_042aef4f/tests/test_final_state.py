# test_final_state.py

import os
import json
import pytest

def test_rust_file_exists():
    """Verify that the Rust source file exists."""
    rust_file = "/home/user/src/parser.rs"
    assert os.path.isfile(rust_file), f"Rust source file {rust_file} is missing."

def test_python_script_exists():
    """Verify that the Python script exists."""
    python_file = "/home/user/app.py"
    assert os.path.isfile(python_file), f"Python script {python_file} is missing."

def test_shared_library_exists_and_is_elf():
    """Verify that the compiled shared library exists and is an ELF file."""
    lib_file = "/home/user/libparser.so"
    assert os.path.isfile(lib_file), f"Shared library {lib_file} is missing."

    with open(lib_file, "rb") as f:
        magic = f.read(4)
    assert magic == b"\x7fELF", f"File {lib_file} is not a valid ELF shared object."

def test_output_json_exists_and_content():
    """Verify that output.json exists and contains the exact expected JSON string."""
    output_file = "/home/user/output.json"
    assert os.path.isfile(output_file), f"Output file {output_file} is missing. Did the Python script run?"

    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read().strip()

    expected_content = '[{"type":1,"value":"Rust"},{"type":2,"value":2024}]'
    assert content == expected_content, f"Content of {output_file} is incorrect.\nExpected: {expected_content}\nGot: {content}"

    # Also verify it's valid JSON
    try:
        parsed = json.loads(content)
        assert isinstance(parsed, list), "Parsed JSON is not a list."
        assert len(parsed) == 2, "Parsed JSON does not have exactly 2 elements."
    except json.JSONDecodeError:
        pytest.fail(f"Content of {output_file} is not valid JSON.")