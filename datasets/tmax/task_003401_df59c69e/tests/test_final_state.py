# test_final_state.py

import os
import re
import socket
import pytest

def test_logrotate_conf():
    conf_file = "/home/user/logrotate.conf"
    assert os.path.exists(conf_file), f"Configuration file {conf_file} does not exist."
    with open(conf_file, "r") as f:
        content = f.read()

    assert "/home/user/logs/api.log" in content, "logrotate.conf does not target /home/user/logs/api.log"
    assert re.search(r"size\s+1k", content) or re.search(r"size\s*=\s*1k", content) or "1k" in content, "logrotate.conf must specify size 1k"
    assert re.search(r"rotate\s+2", content) or re.search(r"rotate\s*=\s*2", content), "logrotate.conf must keep 2 rotated logs"
    assert "compress" in content, "logrotate.conf must use compress"
    assert "delaycompress" in content, "logrotate.conf must use delaycompress"

def test_logrotate_state_and_rotation():
    state_file = "/home/user/logrotate.state"
    assert os.path.exists(state_file), f"State file {state_file} does not exist. Did you run logrotate with a custom state file?"

    rotated_log = "/home/user/logs/api.log.1"
    assert os.path.exists(rotated_log), f"Rotated log {rotated_log} does not exist. Ensure logrotate was executed successfully."

def test_parse_script_and_output():
    script_file = "/home/user/parse.sh"
    assert os.path.exists(script_file), f"Script file {script_file} does not exist."

    output_file = "/home/user/avg_error.txt"
    assert os.path.exists(output_file), f"Output file {output_file} does not exist."

    with open(output_file, "r") as f:
        content = f.read().strip()

    assert content in ["475", "475.0"], f"Expected average error response time to be 475, but got {content}"

def test_proxy_script_and_output():
    script_file = "/home/user/proxy.sh"
    assert os.path.exists(script_file), f"Proxy script {script_file} does not exist."

    with open(script_file, "r") as f:
        content = f.read()

    assert "socat" in content, "Proxy script does not contain a socat command."
    assert "9090" in content, "Proxy script does not reference port 9090."
    assert "8000" in content, "Proxy script does not reference port 8000."

    output_file = "/home/user/health_check.txt"
    assert os.path.exists(output_file), f"Health check output file {output_file} does not exist."

    with open(output_file, "r") as f:
        content = f.read().strip()

    assert content == "OK", f"Expected health check output to be 'OK', but got '{content}'"

def test_port_9090_listening():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = s.connect_ex(('127.0.0.1', 9090))
        assert result == 0, "Port 9090 is not listening. Ensure the proxy script is running in the background."
    finally:
        s.close()