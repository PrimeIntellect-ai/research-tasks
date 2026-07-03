# test_final_state.py
import json
import os
import pytest

def test_json_output_exists_and_correct():
    json_path = "/home/user/docs_final.json"
    assert os.path.exists(json_path), f"JSON output file missing at {json_path}"
    assert os.path.isfile(json_path), f"{json_path} is not a file"

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {json_path} as JSON: {e}")

    assert isinstance(data, list), "JSON root must be an array (list)"
    assert len(data) == 2, f"Expected 2 entries in JSON, found {len(data)}"

    # Check first entry
    assert data[0].get("title") == "Introduction to System", "Title mismatch for entry 1"
    assert data[0].get("author") == "Alice Writer", "Author mismatch for entry 1"
    assert data[0].get("body", "").strip() == "This is the introduction.\nIt spans multiple lines.", "Body mismatch for entry 1"

    # Check second entry
    assert data[1].get("title") == "Installation Guide", "Title mismatch for entry 2"
    assert data[1].get("author") == "Bob Coder", "Author mismatch for entry 2"
    assert data[1].get("body", "").strip() == "Step 1: Download\nStep 2: Install\nStep 3: Profit!", "Body mismatch for entry 2"

def test_rust_source_code_atomic_write():
    rs_path = "/home/user/doc_converter/src/main.rs"
    assert os.path.exists(rs_path), f"Rust source file missing at {rs_path}"
    assert os.path.isfile(rs_path), f"{rs_path} is not a file"

    with open(rs_path, 'r') as f:
        code = f.read()

    assert "rename" in code, "Code does not appear to use std::fs::rename for atomic writes. The word 'rename' was not found in main.rs."