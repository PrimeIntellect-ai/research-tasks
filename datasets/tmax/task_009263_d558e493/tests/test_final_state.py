# test_final_state.py

import os
import subprocess
import time
import urllib.request
import urllib.error
import pytest

def test_scripts_exist():
    assert os.path.isfile("/home/user/infra/proxy.py"), "/home/user/infra/proxy.py is missing"
    assert os.path.isfile("/home/user/infra/monitor.py"), "/home/user/infra/monitor.py is missing"
    assert os.path.isfile("/home/user/provision.sh"), "/home/user/provision.sh is missing"

def test_provisioning_and_health_check():
    # Execute the provisioning script
    result = subprocess.run(["bash", "/home/user/provision.sh"], capture_output=True, text=True)
    assert result.returncode == 0, f"provision.sh failed with exit code {result.returncode}\n{result.stderr}"

    # Wait a bit to ensure the monitor has written to the log
    time.sleep(3)

    # Check that the log file was created in the correct absolute path
    log_path = "/home/user/infra/logs/health.log"
    assert os.path.isfile(log_path), f"Log file {log_path} was not created. monitor.py likely failed to resolve its path."

    # Check the contents of the log file
    with open(log_path, "r") as f:
        log_content = f.read()

    assert "STATUS: OK" in log_content, f"Log file does not contain 'STATUS: OK'. Content: {log_content}"

def test_proxy_forwarding():
    # The proxy should be running on port 9090 and forwarding to port 8080
    url = "http://127.0.0.1:9090/health"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.getcode()
            body = response.read().decode('utf-8')

            assert status == 200, f"Expected HTTP 200, got {status}"
            assert body == "OK", f"Expected body 'OK', got '{body}'"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to proxy at {url}: {e}")