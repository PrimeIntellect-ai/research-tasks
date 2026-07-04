# test_final_state.py

import os
import subprocess
import sys
import importlib.util

REPO_DIR = "/home/user/checksum_service"
LOG_FILE = "/home/user/test_results.log"

def test_results_log_exists_and_ok():
    assert os.path.isfile(LOG_FILE), f"Expected log file {LOG_FILE} is missing. Did you redirect the test output?"
    with open(LOG_FILE, "r") as f:
        content = f.read()
    assert "OK" in content, "The test_results.log does not contain 'OK'. The tests might not have passed or were not redirected correctly."

def test_test_suite_passes():
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "test_service.py"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"The test suite failed when run directly. Output:\n{result.stderr}\n{result.stdout}"

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def test_router_unquotes_payload():
    router_path = os.path.join(REPO_DIR, "router.py")
    assert os.path.isfile(router_path), "router.py is missing."

    router = load_module("router", router_path)

    # "hello world" encoded is "hello%20world". 
    # sum of ordinals of "hello world" is 1116. 
    # 1116 * 10000 = 11160000. 11160000 % 256 = 128
    result = router.route_request("/checksum/custom_sum/hello%20world")
    assert result == 128, "router.py does not correctly decode URL-encoded payloads."

def test_checksums_memory_efficient():
    checksums_path = os.path.join(REPO_DIR, "checksums.py")
    assert os.path.isfile(checksums_path), "checksums.py is missing."

    with open(checksums_path, "r") as f:
        content = f.read()

    # Ensure they didn't just hardcode the test case or keep the memory hog
    assert "payload * 10000" not in content, "The memory bug (payload * 10000) is still present in checksums.py."

    checksums = load_module("checksums", checksums_path)

    # Test with a known value
    payload = "abcdefghijklmnopqrstuvwxyz"
    # sum of "a..z" = 2847
    # 2847 * 10000 = 28470000. % 256 = 64
    result = checksums.custom_sum(payload)
    assert result == 64, f"custom_sum returned {result}, expected 64."