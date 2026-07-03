# test_final_state.py

import os
import pytest

def test_haproxy_cfg_content():
    cfg_path = "/home/user/microservices/lb/haproxy.cfg"
    assert os.path.exists(cfg_path), f"The file {cfg_path} does not exist. Did you run the base generator with the correct environment variable?"

    with open(cfg_path, "r") as f:
        content = f.read()

    # The expected configuration based on the task description
    expected_content = """global
    maxconn 4096
    log 127.0.0.1 local0
defaults
    mode http
    timeout connect 5s
    timeout client 50s
    timeout server 50s
backend web_cluster
    server auth_svc 127.0.0.1:8081
    server user_svc 127.0.0.1:8083
    server inventory_svc 127.0.0.1:8085
    server legacy 127.0.0.1:9050"""

    # We compare line by line, stripping trailing whitespace to be robust against minor formatting differences
    content_lines = [line.rstrip() for line in content.splitlines() if line.strip()]
    expected_lines = [line.rstrip() for line in expected_content.splitlines() if line.strip()]

    assert content_lines == expected_lines, (
        f"The contents of {cfg_path} are incorrect.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n\n"
        f"Got:\n{chr(10).join(content_lines)}"
    )