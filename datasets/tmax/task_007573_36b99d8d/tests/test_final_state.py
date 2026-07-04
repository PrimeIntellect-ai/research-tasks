# test_final_state.py
import os
import stat
import time
import urllib.request
import urllib.error
import subprocess
import json

def test_metrics_service_compiled():
    """Verify that the metrics_service binary exists and is executable."""
    binary_path = "/home/user/metrics_service"
    assert os.path.isfile(binary_path), f"{binary_path} does not exist."
    st = os.stat(binary_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{binary_path} is not executable."

def test_deploy_script_exists_and_executable():
    """Verify that deploy.sh exists and is executable."""
    script_path = "/home/user/deploy.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable."

def test_nginx_config_exists():
    """Verify that nginx.conf exists."""
    config_path = "/home/user/nginx.conf"
    assert os.path.isfile(config_path), f"{config_path} does not exist."
    with open(config_path, "r") as f:
        content = f.read()
    assert "8080" in content, "Nginx config does not seem to contain port 8080."
    assert "9090" in content, "Nginx config does not seem to contain upstream port 9090."

def test_deploy_and_verify_endpoint():
    """Run the deploy script and verify the endpoint returns the correct JSON."""
    # Run the deploy script to ensure idempotency and that services are up
    try:
        subprocess.run(["/home/user/deploy.sh"], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        assert False, f"deploy.sh failed to execute: {e.stderr}"

    # Give services a moment to start
    time.sleep(2)

    # Test the endpoint
    url = "http://127.0.0.1:8080/api/metrics"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.getcode()
            body = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to {url}: {e}"

    assert status == 200, f"Expected HTTP 200, got {status}"

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        assert False, f"Response is not valid JSON: {body}"

    assert data.get("status") == "ok", f"Expected status 'ok', got {data.get('status')}"
    assert data.get("active_connections") == 42, f"Expected 42 active_connections, got {data.get('active_connections')}"