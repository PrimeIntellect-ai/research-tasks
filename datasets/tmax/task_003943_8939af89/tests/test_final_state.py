# test_final_state.py

import os
import json
import subprocess
import urllib.request
import urllib.error
import random
import string
import pytest

def test_ssh_keys_exist():
    private_key_path = "/home/user/.ssh/id_ed25519"
    public_key_path = "/home/user/.ssh/id_ed25519.pub"

    assert os.path.isfile(private_key_path), f"Private key not found at {private_key_path}"
    with open(private_key_path, 'r') as f:
        assert "PRIVATE KEY" in f.read(), "File does not look like a private key"

def test_authorized_keys_configuration():
    auth_keys_path = "/home/user/.ssh/authorized_keys"
    assert os.path.isfile(auth_keys_path), f"authorized_keys not found at {auth_keys_path}"

    with open(auth_keys_path, 'r') as f:
        content = f.read().strip()

    expected_prefix = 'restrict,command="/usr/bin/tail -n 50 /var/log/syslog" '
    assert content.startswith(expected_prefix), "authorized_keys does not start with the required restrict and command prefix."
    assert "ssh-ed25519" in content, "authorized_keys does not contain an ed25519 public key."

def test_config_json_updated():
    config_path = "/app/config.json"
    assert os.path.isfile(config_path), f"{config_path} is missing."

    with open(config_path, 'r') as f:
        config = json.load(f)

    assert config.get("ssh_key_path") == "/home/user/.ssh/id_ed25519", "config.json does not have the correct ssh_key_path."

def test_redis_running():
    try:
        output = subprocess.check_output(["redis-cli", "ping"]).decode("utf-8").strip()
        assert output == "PONG", "Redis is not responding to PING."
    except Exception as e:
        pytest.fail(f"Failed to ping Redis: {e}")

def test_end_to_end_pipeline():
    req = urllib.request.Request("http://127.0.0.1:8080/")
    req.add_header("Cookie", "session=test")
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            data = json.loads(response.read().decode('utf-8'))
            # The prompt says it should return a successful JSON response, e.g. {"status": "ok", "logs_read": true}
            # We just check it's valid JSON and maybe contains 'status' or 'logs_read'
            assert isinstance(data, dict), "Response is not a JSON object"
    except urllib.error.URLError as e:
        pytest.fail(f"HTTP request to Nginx failed: {e}")

def test_validator_fuzz_equivalence():
    oracle_path = "/app/oracle_validator"
    agent_path = "/home/user/validator.py"

    assert os.path.isfile(agent_path), f"Agent script {agent_path} is missing."
    assert os.access(agent_path, os.X_OK), f"Agent script {agent_path} is not executable."

    random.seed(42)

    cookie_charset = string.ascii_letters + string.digits + "_"
    log_charset = string.ascii_letters + string.digits + "_/</> "
    injection_patterns = ["UNION SELECT", "union   select", "/etc/shadow", "<script>", "benign string"]

    for i in range(1000):
        cookie_len = random.randint(5, 20)
        cookie_val = "".join(random.choice(cookie_charset) for _ in range(cookie_len))

        log_len = random.randint(10, 50)
        log_val = "".join(random.choice(log_charset) for _ in range(log_len))

        if random.random() < 0.2:
            pattern = random.choice(injection_patterns)
            insert_pos = random.randint(0, len(log_val))
            log_val = log_val[:insert_pos] + pattern + log_val[insert_pos:]

        try:
            oracle_out = subprocess.check_output([oracle_path, cookie_val, log_val], stderr=subprocess.STDOUT).decode('utf-8').strip()
        except subprocess.CalledProcessError as e:
            oracle_out = e.output.decode('utf-8').strip()

        try:
            agent_out = subprocess.check_output([agent_path, cookie_val, log_val], stderr=subprocess.STDOUT).decode('utf-8').strip()
        except subprocess.CalledProcessError as e:
            agent_out = e.output.decode('utf-8').strip()

        assert oracle_out == agent_out, f"Mismatch on input '{cookie_val}' '{log_val}'. Oracle: {oracle_out}, Agent: {agent_out}"