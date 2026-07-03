# test_final_state.py

import os
import json
import pytest

def test_rust_bug_fixed():
    lib_rs_path = "/home/user/rust_parser/src/lib.rs"
    assert os.path.isfile(lib_rs_path), f"File {lib_rs_path} does not exist."
    with open(lib_rs_path, "r") as f:
        content = f.read()

    assert "into_raw()" in content, "The ownership issue in lib.rs was not fixed using `into_raw()` or equivalent."
    assert "c_result.as_ptr() as *mut c_char" not in content, "The buggy `as_ptr()` call is still present in lib.rs."

def test_rust_library_built():
    so_path = "/home/user/rust_parser/target/release/librust_parser.so"
    assert os.path.isfile(so_path), f"The compiled Rust library was not found at {so_path}. Did you run `cargo build --release`?"

def test_python_script_exists():
    py_path = "/home/user/test_migration.py"
    assert os.path.isfile(py_path), f"The Python script was not found at {py_path}."

def test_migrated_output_json():
    json_path = "/home/user/migrated_output.json"
    assert os.path.isfile(json_path), f"The output JSON was not found at {json_path}. Did you run the Python script?"

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    expected = {
        "schema_version": "v2",
        "user_id": "bob123",
        "status": "active"
    }

    assert data == expected, f"The JSON content in {json_path} does not match the expected output."