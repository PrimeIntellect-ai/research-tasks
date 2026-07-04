# test_final_state.py
import os
import subprocess
import re
import time
import urllib.request
import ssl
import pytest

def test_deploy_script_idempotent():
    script_path = "/home/user/deploy.sh"
    assert os.path.isfile(script_path), f"Deploy script not found at {script_path}"
    assert os.access(script_path, os.X_OK) or script_path.endswith(".sh"), f"Deploy script {script_path} should be executable or runnable via bash"

    # Run once
    res1 = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert res1.returncode == 0, f"Deploy script failed on first run:\nSTDOUT:\n{res1.stdout}\nSTDERR:\n{res1.stderr}"

    # Run twice to test idempotency
    res2 = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert res2.returncode == 0, f"Deploy script failed on second run (idempotency check):\nSTDOUT:\n{res2.stdout}\nSTDERR:\n{res2.stderr}"

def test_index_html():
    path = "/home/user/www/index.html"
    assert os.path.isfile(path), f"File {path} not found"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "OK", f"Expected index.html to contain 'OK', got '{content}'"

def test_services_running():
    # Give services a moment to start if they were just restarted
    time.sleep(2)

    # Check 8080 (backend)
    try:
        req = urllib.request.urlopen("http://127.0.0.1:8080/", timeout=3)
        content = req.read().decode('utf-8').strip()
        assert content == "OK", f"Backend server returned unexpected content: {content}"
    except Exception as e:
        pytest.fail(f"Backend server on 8080 is not responding correctly: {e}")

    # Check 8443 (proxy)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        req = urllib.request.urlopen("https://127.0.0.1:8443/", context=ctx, timeout=3)
        content = req.read().decode('utf-8').strip()
        assert content == "OK", f"Proxy server returned unexpected content: {content}"
    except Exception as e:
        pytest.fail(f"Proxy server on 8443 is not responding correctly: {e}")

def test_throughput():
    # Run Apache Bench against the proxy
    cmd = ["ab", "-n", "500", "-c", "50", "-k", "https://127.0.0.1:8443/"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Extract Requests per second
    match = re.search(r'Requests per second:\s+([\d.]+)', result.stdout)
    assert match is not None, f"Could not parse 'Requests per second' from ab output:\n{result.stdout}\n{result.stderr}"

    rps = float(match.group(1))
    assert rps >= 200.0, f"Throughput is too low: {rps} RPS (expected >= 200.0). The artificial delay in the proxy might not be fully removed."