# test_final_state.py

import os
import pytest

def test_patch_applied():
    c_src_path = "/home/user/release_prep/c_src/route_parser.c"
    assert os.path.isfile(c_src_path), f"File {c_src_path} is missing."
    with open(c_src_path, "r") as f:
        content = f.read()

    assert "strncpy(out_buf, id_start, out_len);" in content, "The patch was not applied correctly to route_parser.c (missing strncpy)."
    assert "strcpy(out_buf, id_start);" not in content, "The buggy strcpy is still present in route_parser.c."

def test_lib_rs_implemented():
    lib_rs_path = "/home/user/release_prep/rust_wrapper/src/lib.rs"
    assert os.path.isfile(lib_rs_path), f"File {lib_rs_path} is missing."
    with open(lib_rs_path, "r") as f:
        content = f.read()

    assert "proptest" in content, "The proptest crate is not used in lib.rs."
    assert "test_extract_valid_urls" in content, "The test 'test_extract_valid_urls' is not defined in lib.rs."
    assert "extract_item_id" in content, "The FFI function 'extract_item_id' is not declared/called in lib.rs."

def test_cargo_test_log():
    log_path = "/home/user/release_test.log"
    assert os.path.isfile(log_path), f"The log file {log_path} is missing. Did you run cargo test and redirect the output?"
    with open(log_path, "r") as f:
        content = f.read()

    assert "test_extract_valid_urls" in content, "The log does not show 'test_extract_valid_urls' being run."
    assert "test result: ok" in content or "test test_extract_valid_urls ... ok" in content, "The test suite did not pass successfully according to the log."