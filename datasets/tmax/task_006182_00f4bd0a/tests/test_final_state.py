# test_final_state.py

import os
import urllib.request
import urllib.error
import pytest

def test_test_results_log():
    log_path = "/home/user/test_results.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist"

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f.read().strip().splitlines() if line.strip()]

    assert len(lines) >= 2, f"{log_path} does not contain enough lines"
    assert lines[0] == "200", f"Expected first line of {log_path} to be '200', got '{lines[0]}'"
    assert lines[1] == "403", f"Expected second line of {log_path} to be '403', got '{lines[1]}'"

def test_build_directories():
    debug_exe = "/home/user/waf-proxy/build_debug/waf_server"
    release_exe = "/home/user/waf-proxy/build_release/waf_server"

    assert os.path.isfile(debug_exe), f"Debug executable not found at {debug_exe}"
    assert os.access(debug_exe, os.X_OK), f"File at {debug_exe} is not executable"

    assert os.path.isfile(release_exe), f"Release executable not found at {release_exe}"
    assert os.access(release_exe, os.X_OK), f"File at {release_exe} is not executable"

def test_memory_leak_fixed():
    waf_cpp_path = "/home/user/waf-proxy/waf.cpp"
    assert os.path.isfile(waf_cpp_path), f"File {waf_cpp_path} does not exist"

    with open(waf_cpp_path, 'r') as f:
        content = f.read()

    # Check if 'delete' is present or if the leak was fixed by removing 'new'
    leak_fixed = "delete" in content or "new int[100]" not in content or "unique_ptr" in content
    assert leak_fixed, "Memory leak in waf.cpp does not appear to be fixed (no 'delete' found and 'new' still present)"

def test_nginx_and_waf_endpoints():
    safe_url = "http://127.0.0.1:8080/api/safe"
    try:
        req = urllib.request.Request(safe_url)
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.getcode() == 200, f"Expected 200 OK for {safe_url}, got {response.getcode()}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Expected 200 OK for {safe_url}, but got HTTPError {e.code}")
    except Exception as e:
        pytest.fail(f"Failed to connect to Nginx reverse proxy at {safe_url}: {e}")

    hack_url = "http://127.0.0.1:8080/api/hack?q=UNION%20SELECT"
    try:
        req = urllib.request.Request(hack_url)
        with urllib.request.urlopen(req, timeout=2) as response:
            pytest.fail(f"Expected 403 Forbidden for {hack_url}, but got 200 OK")
    except urllib.error.HTTPError as e:
        assert e.code == 403, f"Expected 403 Forbidden for {hack_url}, got {e.code}"
    except Exception as e:
        pytest.fail(f"Failed to connect to Nginx reverse proxy at {hack_url}: {e}")