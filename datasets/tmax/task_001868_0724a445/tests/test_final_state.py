# test_final_state.py

import os
import subprocess
import random
import string
import time
import pytest

def test_file_locations():
    assert os.path.exists("/home/user/project/cmd/secapi/main.go"), "cmd/secapi/main.go is missing"
    assert os.path.exists("/home/user/project/pkg/secsum/secsum.go"), "pkg/secsum/secsum.go is missing"
    assert os.path.exists("/home/user/project/cmd/cli/main.go"), "cmd/cli/main.go is missing"
    assert os.path.exists("/home/user/project/bin/secsum_cli"), "bin/secsum_cli is missing"
    assert os.path.exists("/home/user/project/start.sh"), "start.sh is missing"
    assert os.path.exists("/home/user/project/.env"), ".env is missing"
    assert os.access("/home/user/project/start.sh", os.X_OK), "start.sh is not executable"

def test_env_config():
    with open("/home/user/project/.env", "r") as f:
        content = f.read()
    assert "REDIS_ADDR=127.0.0.1:6379" in content, ".env does not contain REDIS_ADDR=127.0.0.1:6379"

def test_nginx_config():
    with open("/home/user/project/nginx.conf", "r") as f:
        content = f.read()
    assert "proxy_pass http://127.0.0.1:8000/" in content or "proxy_pass http://127.0.0.1:8000" in content, "nginx.conf does not contain correct proxy_pass directive"

def test_fuzz_equivalence():
    oracle_path = "/opt/oracle/secsum"
    agent_path = "/home/user/project/bin/secsum_cli"

    random.seed(42)
    chars = string.ascii_letters + string.digits
    for _ in range(1000):
        length = random.randint(1, 256)
        test_str = "".join(random.choices(chars, k=length))

        oracle_out = subprocess.run([oracle_path, test_str], capture_output=True, text=True).stdout.strip()
        agent_out = subprocess.run([agent_path, test_str], capture_output=True, text=True).stdout.strip()

        assert oracle_out == agent_out, f"Mismatch on input '{test_str}'. Expected '{oracle_out}', got '{agent_out}'"

def test_end_to_end():
    subprocess.run(["pkill", "-f", "redis-server"])
    subprocess.run(["pkill", "-f", "secapi"])
    subprocess.run(["pkill", "-f", "nginx"])
    time.sleep(1)

    proc = subprocess.Popen(["bash", "/home/user/project/start.sh"], cwd="/home/user/project")
    time.sleep(2)

    try:
        test_str = "fuzztest"
        oracle_out = subprocess.run(["/opt/oracle/secsum", test_str], capture_output=True, text=True).stdout.strip()

        curl_out = subprocess.run(["curl", "-s", f"http://127.0.0.1:8080/api/sign?data={test_str}"], capture_output=True, text=True).stdout.strip()

        assert curl_out == oracle_out, f"API mismatch. Expected '{oracle_out}', got '{curl_out}'"

        redis_keys = subprocess.run(["redis-cli", "keys", "*"], capture_output=True, text=True).stdout.strip()
        assert len(redis_keys) > 0, "Redis cache is empty, meaning it wasn't used"
    finally:
        subprocess.run(["pkill", "-f", "redis-server"])
        subprocess.run(["pkill", "-f", "secapi"])
        subprocess.run(["pkill", "-f", "nginx"])