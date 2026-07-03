# test_final_state.py
import os
import time
import subprocess
import urllib.request
import urllib.error
import pytest
import re

def test_bashrc_env_var():
    """Check that FINOPS_PROXY_PORT=8080 is in /home/user/.bashrc."""
    bashrc_path = "/home/user/.bashrc"
    assert os.path.exists(bashrc_path), f"{bashrc_path} does not exist."
    with open(bashrc_path, "r") as f:
        content = f.read()
    assert re.search(r"FINOPS_PROXY_PORT\s*=\s*8080", content) or "FINOPS_PROXY_PORT=8080" in content, \
        "FINOPS_PROXY_PORT=8080 not found in /home/user/.bashrc."

def test_proxy_script_exists():
    """Check that the proxy script exists."""
    proxy_path = "/home/user/scale_to_zero_proxy.py"
    assert os.path.exists(proxy_path), f"{proxy_path} does not exist."

def test_supervisor_conf_exists_and_valid():
    """Check that supervisor.conf exists and has required sections."""
    conf_path = "/home/user/supervisor.conf"
    assert os.path.exists(conf_path), f"{conf_path} does not exist."
    with open(conf_path, "r") as f:
        content = f.read()
    assert "[program:finops_proxy]" in content, "Missing [program:finops_proxy] in supervisor.conf"
    assert "scale_to_zero_proxy.py" in content, "Proxy script not referenced in supervisor.conf"
    assert "autorestart=true" in content.lower(), "autorestart=true not found in supervisor.conf"

@pytest.fixture(scope="module")
def run_supervisor():
    """Fixture to start supervisord and ensure cleanup."""
    conf_path = "/home/user/supervisor.conf"
    # Ensure no old instances are running
    subprocess.run(["pkill", "-f", "supervisord"], capture_output=True)
    subprocess.run(["pkill", "-f", "scale_to_zero_proxy.py"], capture_output=True)
    subprocess.run(["pkill", "-f", "analytics_service.py"], capture_output=True)

    # Start supervisord
    proc = subprocess.Popen(["supervisord", "-c", conf_path])
    time.sleep(3) # Wait for supervisord to start the proxy

    yield

    # Teardown
    subprocess.run(["pkill", "-f", "supervisord"], capture_output=True)
    subprocess.run(["pkill", "-f", "scale_to_zero_proxy.py"], capture_output=True)
    subprocess.run(["pkill", "-f", "analytics_service.py"], capture_output=True)

def test_proxy_behavior(run_supervisor):
    """Test the end-to-end behavior of the proxy."""
    # Verify proxy is running
    check_proxy = subprocess.run(["pgrep", "-f", "scale_to_zero_proxy.py"], capture_output=True, text=True)
    assert check_proxy.returncode == 0, "scale_to_zero_proxy.py is not running via supervisord."

    # Ensure analytics_service is NOT running initially
    check_backend_initial = subprocess.run(["pgrep", "-f", "analytics_service.py"], capture_output=True, text=True)
    assert check_backend_initial.returncode != 0, "analytics_service.py should not be running before the first request."

    # Make a request to the proxy
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/")
        with urllib.request.urlopen(req, timeout=10) as response:
            status = response.getcode()
            body = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to proxy or proxy returned error: {e}")

    assert status == 200, f"Expected status 200, got {status}"
    assert "ANALYTICS_COST_SAVINGS_ACTIVE" in body, "Response body did not match expected output."

    # Verify analytics_service is NOW running
    check_backend_final = subprocess.run(["pgrep", "-f", "analytics_service.py"], capture_output=True, text=True)
    assert check_backend_final.returncode == 0, "analytics_service.py was not spawned by the proxy."