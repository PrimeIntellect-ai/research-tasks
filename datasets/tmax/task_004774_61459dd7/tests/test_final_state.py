# test_final_state.py

import os
import re
import pytest

def test_test_results_log_exists():
    log_path = "/home/user/test_results.log"
    assert os.path.isfile(log_path), f"Test results log {log_path} does not exist."

def test_test_results_indicate_success():
    log_path = "/home/user/test_results.log"
    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if tests passed
    assert re.search(r'test result: ok\.', content) or re.search(r'\d+ passed', content), \
        "The test_results.log does not indicate successful test execution ('test result: ok.' or 'passed')."

def test_cargo_toml_conflict_resolved():
    cargo_path = "/home/user/api-gateway/Cargo.toml"
    assert os.path.isfile(cargo_path), f"{cargo_path} does not exist."

    with open(cargo_path, "r", encoding="utf-8") as f:
        content = f.read()

    # It shouldn't have both tonic 0.9 and prost 0.12, as that caused the conflict.
    # We check that at least one of them was changed.
    has_tonic_09 = 'tonic = "0.9"' in content or "tonic = '0.9'" in content
    has_prost_12 = 'prost = "0.12"' in content or "prost = '0.12'" in content

    assert not (has_tonic_09 and has_prost_12), \
        "Cargo.toml still has the conflicting tonic 0.9 and prost 0.12 dependencies."

def test_rest_handler_implemented():
    rest_path = "/home/user/api-gateway/src/rest.rs"
    assert os.path.isfile(rest_path), f"{rest_path} does not exist."

    with open(rest_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "Hasher" in content or "crc32fast" in content, \
        "src/rest.rs does not seem to use crc32fast for checksum calculation."
    assert "Path" in content, "src/rest.rs does not seem to extract the Path parameter."

def test_security_tests_implemented():
    tests_path = "/home/user/api-gateway/src/security_tests.rs"
    assert os.path.isfile(tests_path), f"{tests_path} does not exist."

    with open(tests_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "proptest!" in content or "proptest {" in content, \
        "src/security_tests.rs does not seem to contain a proptest block."