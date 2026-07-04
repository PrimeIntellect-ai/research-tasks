# test_final_state.py

import os
import subprocess
import time
import pytest

def test_bashrc_exports():
    """Check that .bashrc contains the correct environment variable exports."""
    bashrc_path = "/home/user/.bashrc"
    assert os.path.exists(bashrc_path), f"File {bashrc_path} does not exist."

    with open(bashrc_path, 'r') as f:
        content = f.read()

    assert "export APP_LB_PORT=8080" in content, "APP_LB_PORT=8080 is not exported in .bashrc"
    assert "export APP_B1_PORT=9001" in content, "APP_B1_PORT=9001 is not exported in .bashrc"
    assert "export APP_B2_PORT=9002" in content, "APP_B2_PORT=9002 is not exported in .bashrc"

def test_haproxy_cfg_syntax_and_contents():
    """Validate HAProxy configuration syntax and required directives."""
    cfg_path = "/home/user/haproxy.cfg"
    assert os.path.exists(cfg_path), f"HAProxy config {cfg_path} does not exist."

    result = subprocess.run(["haproxy", "-c", "-f", cfg_path], capture_output=True, text=True)
    assert result.returncode == 0, f"HAProxy config syntax error:\n{result.stderr}"

    with open(cfg_path, 'r') as f:
        content = f.read()

    assert "app_front" in content, "Frontend 'app_front' not found in haproxy.cfg"
    assert "app_back" in content, "Backend 'app_back' not found in haproxy.cfg"
    assert "8080" in content, "Port 8080 not found in haproxy.cfg"
    assert "9001" in content, "Backend port 9001 not found in haproxy.cfg"
    assert "9002" in content, "Backend port 9002 not found in haproxy.cfg"
    assert "roundrobin" in content, "Roundrobin algorithm not specified in haproxy.cfg"
    assert "mode http" in content, "mode http not specified in haproxy.cfg"

def test_verify_script_exists_and_executable():
    """Check that verify.sh exists and is executable."""
    script_path = "/home/user/verify.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_deployment_functionality():
    """
    Simulate the automated testing framework:
    1. Start mock backends.
    2. Start HAProxy.
    3. Run verify.sh.
    4. Validate health_check.log output.
    """
    b1_cmd = "while true; do echo -e 'HTTP/1.1 200 OK\\r\\n\\r\\nB1' | nc -l -p 9001 -q 1; done"
    b2_cmd = "while true; do echo -e 'HTTP/1.1 200 OK\\r\\n\\r\\nB2' | nc -l -p 9002 -q 1; done"

    p_b1 = subprocess.Popen(b1_cmd, shell=True, executable="/bin/bash", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    p_b2 = subprocess.Popen(b2_cmd, shell=True, executable="/bin/bash", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    p_ha = subprocess.Popen(["haproxy", "-f", "/home/user/haproxy.cfg"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Allow services to start
    time.sleep(2)

    log_file = "/home/user/health_check.log"
    if os.path.exists(log_file):
        os.remove(log_file)

    # Run the user's verify script
    subprocess.run(["/home/user/verify.sh"], shell=True, executable="/bin/bash")

    # Cleanup processes
    p_b1.kill()
    p_b2.kill()
    p_ha.kill()

    assert os.path.exists(log_file), f"Log file {log_file} was not created by verify.sh."

    with open(log_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    b1_count = lines.count("B1")
    b2_count = lines.count("B2")

    assert len(lines) == 4, f"Expected exactly 4 lines in {log_file}, found {len(lines)}."
    assert b1_count == 2, f"Expected 2 requests routed to B1, found {b1_count}."
    assert b2_count == 2, f"Expected 2 requests routed to B2, found {b2_count}."