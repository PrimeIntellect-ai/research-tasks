# test_final_state.py

import os
import re
import pytest

def test_test_results_log_exists_and_passed():
    log_path = "/home/user/project/test_results.log"
    assert os.path.isfile(log_path), f"Test results log missing at {log_path}"

    with open(log_path, "r") as f:
        content = f.read()

    # Check that tests were collected and passed
    assert re.search(r"collected \d+ items", content, re.IGNORECASE) or "test session starts" in content, \
        "The test_results.log does not appear to contain pytest output."

    assert "failed" not in content.lower() or "0 failed" in content.lower(), \
        "The test_results.log indicates that some tests failed."
    assert "passed" in content.lower(), \
        "The test_results.log does not indicate that tests passed."

def test_c_ext_fixed():
    c_file_path = "/home/user/project/c_ext/fast_sec.c"
    assert os.path.isfile(c_file_path), f"C extension file missing at {c_file_path}"

    with open(c_file_path, "r") as f:
        content = f.read()

    # The original bug was a 64-byte buffer and an unsafe strcpy.
    # The fix should either increase the buffer size (>= 256) or use safe string functions like strncpy.
    has_unsafe_strcpy = "strcpy(buffer, input_str);" in content
    has_small_buffer = "char buffer[64];" in content

    assert not (has_unsafe_strcpy and has_small_buffer), \
        "The C extension still contains the original buffer overflow bug."

def test_rust_ext_fixed():
    rust_file_path = "/home/user/project/rust_ext/src/lib.rs"
    assert os.path.isfile(rust_file_path), f"Rust extension file missing at {rust_file_path}"

    with open(rust_file_path, "r") as f:
        content = f.read()

    # The original bug returned PyResult<&'static str>
    assert "PyResult<&'static str>" not in content, \
        "The Rust extension still returns a static string reference, which causes a borrow checker error."

    # The fix should return an owned String
    assert "PyResult<String>" in content or "PyResult<std::string::String>" in content, \
        "The Rust extension should return an owned String (PyResult<String>)."

    # Check that the unsafe transmute was removed
    assert "std::mem::transmute" not in content, \
        "The Rust extension still contains the unsafe lifetime transmute."

def test_test_parser_implemented():
    test_file_path = "/home/user/project/tests/test_parser.py"
    assert os.path.isfile(test_file_path), f"Test parser file missing at {test_file_path}"

    with open(test_file_path, "r") as f:
        content = f.read()

    # Ensure the test file actually imports the modules and reads the json
    assert "json" in content or "data.json" in content, "The test file does not appear to read data.json."
    assert "fast_sec" in content, "The test file does not appear to test the C extension."
    assert "rust_sec" in content, "The test file does not appear to test the Rust extension."