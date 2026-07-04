# test_final_state.py

import os
import subprocess
import urllib.request
import pytest

def test_results_log():
    path = "/home/user/test_results.log"
    assert os.path.exists(path), f"Missing {path}. Did the verify.py script run and create it?"

    with open(path, "r") as f:
        content = f.read().strip()

    if not content:
        pytest.fail(f"{path} is empty.")

    lines = content.splitlines()
    assert len(lines) == 4, f"Expected exactly 4 lines in {path}, found {len(lines)}"

    for i, line in enumerate(lines):
        assert line == "API_OK", f"Line {i+1} in {path} expected to be 'API_OK', got '{line}'"

def test_lb_service_dependencies():
    # We use su to run as user because systemctl --user requires the user's D-Bus/environment
    cmd = ['su', '-', 'user', '-c', 'systemctl --user show lb.service -p After -p Requires']
    result = subprocess.run(cmd, capture_output=True, text=True)

    assert result.returncode == 0, f"Failed to run systemctl: {result.stderr}"
    output = result.stdout

    after_line = ""
    requires_line = ""
    for line in output.splitlines():
        if line.startswith("After="):
            after_line = line
        elif line.startswith("Requires="):
            requires_line = line

    assert "api.service" in after_line, "lb.service 'After=' directive does not contain 'api.service'"
    assert "tunnel.service" in after_line, "lb.service 'After=' directive does not contain 'tunnel.service'"

    assert "api.service" in requires_line, "lb.service 'Requires=' directive does not contain 'api.service'"
    assert "tunnel.service" in requires_line, "lb.service 'Requires=' directive does not contain 'tunnel.service'"

def test_lb_and_tunnel_running():
    # Make 4 requests to ensure we hit both the direct backend and the tunnel via round-robin
    for i in range(4):
        try:
            req = urllib.request.Request("http://127.0.0.1:9000/")
            with urllib.request.urlopen(req, timeout=2) as response:
                body = response.read().decode('utf-8').strip()
                assert body == "API_OK", f"Request {i+1}: Expected 'API_OK', got '{body}'"
        except Exception as e:
            pytest.fail(f"Request {i+1}: Failed to connect to Load Balancer on port 9000 or receive correct response: {e}. Are all services running?")