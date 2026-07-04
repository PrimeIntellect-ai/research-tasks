# test_final_state.py

import os
import subprocess
import random
import string
import urllib.request
import urllib.error
import pytest

def test_nginx_configured_and_running():
    conf_path = "/home/user/nginx.conf"
    assert os.path.exists(conf_path), f"Nginx config missing at {conf_path}"

    with open(conf_path, "r") as f:
        config_content = f.read()

    assert "8080" in config_content, "Nginx config must bind to port 8080"
    assert "8081" in config_content, "Nginx config must route to 8081"
    assert "9090" in config_content, "Nginx config must route to 9090"
    assert "daemon off;" in config_content, "Nginx must be configured to run in foreground"

    # Check if Nginx is actually listening on 8080
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/")
        urllib.request.urlopen(req, timeout=2)
    except urllib.error.HTTPError:
        pass # HTTP errors are fine, means server is responding
    except urllib.error.URLError as e:
        pytest.fail(f"Nginx does not appear to be listening on 127.0.0.1:8080. Error: {e}")

def test_fuzz_equivalence_analyzer():
    oracle_path = "/app/oracle_analyzer"
    agent_path = "/home/user/payload_analyzer/target/release/analyzer"

    assert os.path.exists(oracle_path), f"Oracle binary missing at {oracle_path}"
    assert os.path.exists(agent_path), f"Agent binary missing at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary is not executable at {agent_path}"

    random.seed(42)
    base_chars = string.ascii_letters + string.digits
    weighted_chars = base_chars + "%/\\." * 10 + "-_=+?&#:" * 2

    prefixes = [
        "http://", "https://", "//", "http:/\\/\\", "%2F%2F", 
        "%68%74%74%70%3A%2F%2F", "/dashboard", "corp.local", 
        "127.0.0.1", "localhost"
    ]

    for _ in range(1000):
        length = random.randint(1, 200)
        payload = "".join(random.choice(weighted_chars) for _ in range(length))

        if random.random() < 0.3:
            payload = random.choice(prefixes) + payload

        oracle_proc = subprocess.run([oracle_path, payload], capture_output=True, text=True)
        agent_proc = subprocess.run([agent_path, payload], capture_output=True, text=True)

        assert oracle_proc.stdout == agent_proc.stdout, (
            f"Mismatch on input: {payload!r}\n"
            f"Oracle output: {oracle_proc.stdout!r}\n"
            f"Agent output: {agent_proc.stdout!r}"
        )