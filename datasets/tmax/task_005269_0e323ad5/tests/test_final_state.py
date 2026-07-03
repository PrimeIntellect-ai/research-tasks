# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error
import random
import string
import time
import pytest

def test_build_and_run_log_exists():
    path = "/home/user/proxy_project/build_and_run.log"
    assert os.path.isfile(path), f"Log file {path} was not created."

def test_proxy_binary_exists():
    path = "/home/user/proxy_project/proxy"
    assert os.path.isfile(path), f"Proxy binary {path} was not built."
    assert os.access(path, os.X_OK), f"Proxy binary {path} is not executable."

def test_config_env_values():
    path = "/home/user/proxy_project/config.env"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "PROXY_PORT=8080" in content, "PROXY_PORT not set correctly in config.env"
    assert "BACKEND_URL=http://127.0.0.1:9090" in content, "BACKEND_URL not set correctly in config.env"
    assert "REDIS_HOST=127.0.0.1" in content, "REDIS_HOST not set correctly in config.env"

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_proxy"
    assert os.path.isfile(oracle_path), f"Oracle binary {oracle_path} not found."

    # Start the oracle proxy on port 8081
    oracle_proc = subprocess.Popen(
        [oracle_path, "--port", "8081", "--backend", "127.0.0.1:9090", "--redis", "127.0.0.1:6379"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    try:
        # Give it a moment to start
        time.sleep(2)

        random.seed(42)
        chars = string.ascii_letters + string.digits + "-_.~!*'();:@&=+$,/?%#[]"

        # Test 1000 random requests
        for i in range(1000):
            length = random.randint(1, 2048)
            query = ''.join(random.choice(chars) for _ in range(length))

            agent_url = f"http://127.0.0.1:8080/{query}"
            oracle_url = f"http://127.0.0.1:8081/{query}"

            agent_res = None
            oracle_res = None

            try:
                with urllib.request.urlopen(agent_url, timeout=2) as response:
                    agent_res = response.read()
            except urllib.error.HTTPError as e:
                agent_res = e.read()
            except Exception as e:
                agent_res = str(e).encode()

            try:
                with urllib.request.urlopen(oracle_url, timeout=2) as response:
                    oracle_res = response.read()
            except urllib.error.HTTPError as e:
                oracle_res = e.read()
            except Exception as e:
                oracle_res = str(e).encode()

            assert agent_res == oracle_res, f"Mismatch on input {query[:50]}... (length {length}). Agent: {agent_res[:100]}, Oracle: {oracle_res[:100]}"

    finally:
        oracle_proc.terminate()
        oracle_proc.wait()