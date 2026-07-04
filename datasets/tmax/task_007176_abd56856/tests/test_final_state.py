# test_final_state.py

import os
import json
import pytest

def test_rust_library_compiled():
    so_path = "/home/user/parser/target/release/libparser.so"
    assert os.path.exists(so_path), f"Compiled shared library not found at {so_path}. Did you compile in release mode?"

def test_rust_source_fixed():
    rs_path = "/home/user/parser/src/lib.rs"
    assert os.path.exists(rs_path), f"Rust source file missing at {rs_path}."
    with open(rs_path, "r") as f:
        content = f.read()
    assert "into_raw()" in content, "The Rust bug does not appear to be fixed. Expected to see `into_raw()` used to hand over ownership of the CString."
    assert "as_ptr()" not in content.split("BUG:")[1] if "BUG:" in content else True, "The buggy `as_ptr()` return might still be present."

def test_benchmark_result_json():
    json_path = "/home/user/benchmark_result.json"
    assert os.path.exists(json_path), f"Benchmark result file not found at {json_path}."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    assert "message_count" in data, "JSON missing 'message_count' key."
    assert data["message_count"] == 100, f"Expected message_count to be 100, got {data['message_count']}."

    assert "total_time_ms" in data, "JSON missing 'total_time_ms' key."
    assert isinstance(data["total_time_ms"], (int, float)), "total_time_ms must be a number."
    assert data["total_time_ms"] > 0, f"Expected total_time_ms to be > 0, got {data['total_time_ms']}."

    assert "last_message_decoded" in data, "JSON missing 'last_message_decoded' key."
    expected_last_message = "FINAL_TEST_MESSAGE_SUCCESS"
    assert data["last_message_decoded"] == expected_last_message, f"Expected last_message_decoded to be '{expected_last_message}', got '{data['last_message_decoded']}'."

def test_client_script_exists():
    client_path = "/home/user/client.py"
    assert os.path.exists(client_path), f"Client script not found at {client_path}."