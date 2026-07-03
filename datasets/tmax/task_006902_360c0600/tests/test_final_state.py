# test_final_state.py

import os
import stat
import urllib.request
import time
import pytest

def test_deploy_script_exists():
    assert os.path.isfile("/home/user/deploy.sh"), "deploy.sh does not exist"

def test_startup_file_contents():
    startup_file = "/home/user/startup.txt"
    assert os.path.isfile(startup_file), "startup.txt does not exist"
    with open(startup_file, "r") as f:
        content = f.read()
    assert "v1_ready" in content, "startup.txt missing 'v1_ready'"
    assert "v2_ready" in content, "startup.txt missing 'v2_ready'"

def test_proxy_log_permissions():
    log_file = "/home/user/proxy.log"
    assert os.path.isfile(log_file), "proxy.log does not exist"
    st = os.stat(log_file)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o640, f"proxy.log permissions are {oct(perms)}, expected 0o640"

def test_proxy_routing_and_logging():
    # Wait for the proxy to be available
    max_retries = 10
    proxy_url = "http://127.0.0.1:8080"

    for _ in range(max_retries):
        try:
            urllib.request.urlopen(proxy_url + "/ping", timeout=1)
            break
        except Exception:
            time.sleep(0.5)
    else:
        pytest.fail("Proxy server is not listening on port 8080")

    # Test v1 routing
    req_v1 = urllib.request.Request(proxy_url + "/data1")
    with urllib.request.urlopen(req_v1) as response:
        body_v1 = response.read().decode('utf-8')
    assert "Legacy v1 Response: /data1" in body_v1, "v1 routing failed or returned incorrect response"

    # Test v2 routing
    req_v2 = urllib.request.Request(proxy_url + "/data2")
    req_v2.add_header("X-API-Version", "v2")
    with urllib.request.urlopen(req_v2) as response:
        body_v2 = response.read().decode('utf-8')
    assert "New v2 Response: /data2" in body_v2, "v2 routing failed or returned incorrect response"

    # Check proxy log
    log_file = "/home/user/proxy.log"
    with open(log_file, "r") as f:
        log_content = f.read()

    assert "v1 /data1" in log_content, "proxy.log missing v1 entry"
    assert "v2 /data2" in log_content, "proxy.log missing v2 entry"