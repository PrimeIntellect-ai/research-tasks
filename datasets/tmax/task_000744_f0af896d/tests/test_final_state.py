# test_final_state.py

import os
import subprocess
import random
import pytest

def test_sanitizer_fuzz_equivalence():
    agent_bin = "/home/user/workspace/sanitizer"
    oracle_bin = "/app/bin/sanitizer_oracle"

    assert os.path.exists(agent_bin), f"Agent binary not found at {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary at {agent_bin} is not executable"

    random.seed(42)

    # Run 1000 iterations to balance thoroughness and test execution time
    for i in range(1000):
        length = random.randint(0, 4096)
        input_data = bytes(random.choices(range(256), k=length))

        try:
            oracle_proc = subprocess.run([oracle_bin], input=input_data, capture_output=True, timeout=2)
            agent_proc = subprocess.run([agent_bin], input=input_data, capture_output=True, timeout=2)
        except subprocess.TimeoutExpired:
            pytest.fail(f"Timeout on input iteration {i} (length {length})")

        assert agent_proc.returncode == oracle_proc.returncode, (
            f"Return code mismatch on iteration {i}. "
            f"Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}"
        )
        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Output mismatch on iteration {i} (length {length}).\n"
            f"Oracle output: {oracle_proc.stdout!r}\n"
            f"Agent output: {agent_proc.stdout!r}"
        )

def test_nginx_configuration():
    config_path = "/home/user/workspace/nginx.conf"
    assert os.path.exists(config_path), f"Nginx config not found at {config_path}"

    with open(config_path, "r") as f:
        content = f.read()

    # Basic checks for the required directives
    assert "5000" in content, "Missing proxy_pass to port 5000 for the REST API."
    assert "5001" in content, "Missing proxy_pass to port 5001 for the WebSocket service."

    content_lower = content.lower()
    assert "upgrade $http_upgrade" in content_lower, "Missing 'proxy_set_header Upgrade $http_upgrade;' directive."
    assert "connection" in content_lower and "upgrade" in content_lower, "Missing 'proxy_set_header Connection \"upgrade\";' directive."

    assert "host" in content_lower and "$host" in content_lower, "Missing 'proxy_set_header Host $host;' (or similar) directive to preserve the Host header."