# test_final_state.py
import os
import re
import subprocess
import time
import urllib.request
import urllib.error
import socket
import pytest

def test_start_api_expect_script():
    exp_path = "/home/user/start_api.exp"
    assert os.path.isfile(exp_path), f"File {exp_path} is missing."

    with open(exp_path, "r") as f:
        content = f.read()
    assert "SRE-8891" in content, "Expect script does not contain the correct passcode."

    # Run the expect script in the background to see if it brings up port 9000
    proc = subprocess.Popen(["expect", exp_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    server_up = False
    for _ in range(10):
        try:
            with urllib.request.urlopen("http://127.0.0.1:9000/", timeout=1) as response:
                if response.status == 200:
                    server_up = True
                    break
        except Exception:
            pass
        time.sleep(0.5)

    proc.terminate()
    proc.wait(timeout=2)

    assert server_up, "The expect script failed to start the server on port 9000 successfully."

def test_haproxy_config():
    cfg_path = "/home/user/haproxy.cfg"
    assert os.path.isfile(cfg_path), f"File {cfg_path} is missing."

    with open(cfg_path, "r") as f:
        content = f.read()

    assert "8080" in content, "HAProxy config missing port 8080."
    assert "9000" in content, "HAProxy config missing port 9000."

    # Check syntax using haproxy
    result = subprocess.run(["haproxy", "-c", "-f", cfg_path], capture_output=True, text=True)
    assert result.returncode == 0, f"HAProxy config syntax check failed:\n{result.stderr}"

def test_monitor_script():
    script_path = "/home/user/monitor.sh"
    log_path = "/home/user/uptime.log"
    assert os.path.isfile(script_path), f"File {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"File {script_path} is not executable."

    # Ensure port 8080 is down
    subprocess.run([script_path], capture_output=True)
    assert os.path.isfile(log_path), f"Log file {log_path} was not created."
    with open(log_path, "r") as f:
        lines = f.read().strip().split('\n')
    assert lines[-1] == "DOWN", "Monitor script did not log 'DOWN' when the server is unreachable."

    # Start a dummy server on 8080
    dummy_server = subprocess.Popen(["python3", "-m", "http.server", "8080"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1) # wait for server to start

    try:
        subprocess.run([script_path], capture_output=True)
        with open(log_path, "r") as f:
            lines = f.read().strip().split('\n')
        assert lines[-1] == "UP", "Monitor script did not log 'UP' when the server is reachable."
    finally:
        dummy_server.terminate()
        dummy_server.wait(timeout=2)

def test_crontab_txt():
    cron_path = "/home/user/crontab.txt"
    assert os.path.isfile(cron_path), f"File {cron_path} is missing."

    with open(cron_path, "r") as f:
        content = f.read().strip()

    # Check for */5 * * * * /home/user/monitor.sh
    # allow some flexibility with spaces
    match = re.search(r"^\s*\*/5\s+\*\s+\*\s+\*\s+\*\s+/home/user/monitor\.sh\s*$", content, re.MULTILINE)
    assert match is not None, f"Crontab file does not contain the correct schedule. Found:\n{content}"