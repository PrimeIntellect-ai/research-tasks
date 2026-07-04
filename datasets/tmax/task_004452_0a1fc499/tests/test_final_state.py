# test_final_state.py
import os
import pytest

def test_libeval_so_exists():
    lib_path = "/home/user/bashwaf/libeval.so"
    assert os.path.isfile(lib_path), f"Expected shared library {lib_path} to exist, but it is missing."

def test_scan_results_content():
    results_path = "/home/user/bashwaf/scan_results.log"
    assert os.path.isfile(results_path), f"Expected {results_path} to exist."

    with open(results_path, "r") as f:
        content = f.read().strip()

    expected_content = "req_001: CLEAN\nreq_002: MALICIOUS\nreq_003: ERROR"

    assert content == expected_content, (
        f"Contents of {results_path} do not match the expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Got:\n{content}"
    )

def test_waf_sh_initialization_checks_retained():
    waf_path = "/home/user/bashwaf/waf.sh"
    assert os.path.isfile(waf_path), f"Expected {waf_path} to exist."

    with open(waf_path, "r") as f:
        content = f.read()

    assert "Starting BashWAF..." in content, "Original initialization check 'Starting BashWAF...' is missing from waf.sh"
    assert "Initializing engine..." in content, "Original initialization check 'Initializing engine...' is missing from waf.sh"