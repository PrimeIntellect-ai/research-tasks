# test_final_state.py
import os
import re
import pytest

BASE_DIR = "/home/user/ws_encoder_api"
TEST_RESULTS_LOG = "/home/user/test_results.log"

def test_test_results_log_exists_and_passed():
    assert os.path.isfile(TEST_RESULTS_LOG), f"Expected test results log at {TEST_RESULTS_LOG} is missing."

    with open(TEST_RESULTS_LOG, "r", encoding="utf-8") as f:
        content = f.read()

    assert "test result: ok" in content, "The test_results.log does not indicate that all tests passed ('test result: ok' not found)."
    assert "0 failed" in content, "The test_results.log indicates that some tests failed."

def test_build_rs_implemented():
    build_rs_path = os.path.join(BASE_DIR, "build.rs")
    assert os.path.isfile(build_rs_path), "build.rs is missing."

    with open(build_rs_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert len(content.strip()) > 0, "build.rs is still empty."
    assert "cc::" in content or "Build::new" in content, "build.rs does not appear to use the 'cc' crate to build the C code."
    assert "hex_encoder.c" in content, "build.rs does not reference 'hex_encoder.c'."

def test_c_memory_bug_fixed():
    c_file_path = os.path.join(BASE_DIR, "c_src", "hex_encoder.c")
    assert os.path.isfile(c_file_path), "hex_encoder.c is missing."

    with open(c_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check that it allocates enough space for the null terminator
    # It could be malloc(len * 2 + 1) or calloc(len * 2 + 1, 1) or len*2 + 1 etc.
    assert re.search(r'(malloc|calloc)\s*\([^;]*\+\s*1[^;]*\)', content) or re.search(r'len\s*\*\s*2\s*\+\s*1', content), \
        "hex_encoder.c does not appear to allocate space for the null terminator (expected +1 in allocation)."

def test_rate_limiter_implemented():
    rate_limit_path = os.path.join(BASE_DIR, "src", "rate_limit.rs")
    assert os.path.isfile(rate_limit_path), "rate_limit.rs is missing."

    with open(rate_limit_path, "r", encoding="utf-8") as f:
        content = f.read()

    # The original file just had a `true` return.
    # A proper implementation will mutate `self.counts`
    assert "self.counts.entry" in content or "self.counts.get_mut" in content or "self.counts.insert" in content, \
        "rate_limit.rs does not appear to update the 'counts' HashMap."