# test_final_state.py

import os
import subprocess
import random
import re

def test_nginx_config_updated():
    nginx_conf = "/home/user/edge_proxy/nginx.conf"
    assert os.path.isfile(nginx_conf), f"Nginx config missing at {nginx_conf}"
    with open(nginx_conf, 'r') as f:
        content = f.read()

    assert "unix:/home/user/run/app.sock" in content, "Nginx config does not point to the correct socket path 'unix:/home/user/run/app.sock'."

def test_logrotate_config():
    logrotate_conf = "/home/user/logrotate.conf"
    assert os.path.isfile(logrotate_conf), f"Logrotate config missing at {logrotate_conf}"
    with open(logrotate_conf, 'r') as f:
        content = f.read()

    assert "daily" in content, "Logrotate config missing 'daily' directive"
    assert "rotate 7" in content, "Logrotate config missing 'rotate 7' directive"
    assert "compress" in content, "Logrotate config missing 'compress' directive"
    assert "missingok" in content, "Logrotate config missing 'missingok' directive"

    has_wildcard = "/home/user/edge_proxy/logs/*.log" in content
    has_both = "/home/user/edge_proxy/logs/access.log" in content and "/home/user/edge_proxy/logs/error.log" in content
    assert has_wildcard or has_both, "Logrotate config does not apply to the correct log files (/home/user/edge_proxy/logs/access.log and error.log, or *.log)"

def test_crontab_updated():
    try:
        output = subprocess.check_output(['crontab', '-l'], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError:
        output = ""

    assert re.search(r'\*/5\s+\*\s+\*\s+\*\s+\*\s+/home/user/monitor\.sh', output), "Crontab does not contain the correct entry for monitor.sh running every 5 minutes"

def test_fuzz_equivalence_encoder():
    oracle_path = "/app/legacy_encoder"
    agent_path = "/home/user/encoder"

    assert os.path.isfile(agent_path), f"Agent binary missing at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary is not executable at {agent_path}"

    random.seed(42)

    for _ in range(1000):
        t = random.randint(0, 10000)
        h = random.randint(0, 10000)
        p = random.randint(0, 10000)
        l = random.randint(0, 10000)

        input_data = f"{t} {h} {p} {l}\n".encode('utf-8')

        oracle_proc = subprocess.run([oracle_path], input=input_data, capture_output=True)
        agent_proc = subprocess.run([agent_path], input=input_data, capture_output=True)

        assert oracle_proc.stdout == agent_proc.stdout, (
            f"Output mismatch on input '{input_data.decode().strip()}'.\n"
            f"Oracle stdout: {oracle_proc.stdout.hex()}\n"
            f"Agent stdout:  {agent_proc.stdout.hex()}"
        )