# test_final_state.py

import os
import subprocess
import random
import struct
import urllib.request
import time
import pytest

def test_services_running_and_health():
    # Check if the registry API is running and healthy
    max_retries = 5
    for i in range(max_retries):
        try:
            req = urllib.request.Request("http://127.0.0.1:5000/health")
            with urllib.request.urlopen(req, timeout=2) as response:
                assert response.status == 200, "Registry API /health returned non-200 status"
                break
        except Exception as e:
            if i == max_retries - 1:
                pytest.fail(f"Could not connect to Registry API on port 5000: {e}")
            time.sleep(1)

def test_nginx_config_and_directories():
    assert os.path.isdir("/home/user/repo/data"), "/home/user/repo/data directory is missing"
    assert os.path.isdir("/home/user/repo/run"), "/home/user/repo/run directory is missing"

    nginx_conf_path = "/app/services/nginx/nginx.conf"
    with open(nginx_conf_path, "r") as f:
        conf = f.read()

    assert "listen 8080;" in conf or "listen 8080 " in conf, "Nginx not configured to listen on port 8080"
    assert "/home/user/repo/data" in conf, "Nginx not configured to serve from /home/user/repo/data"
    assert "/home/user/repo/run" in conf, "Nginx not configured to use /home/user/repo/run for pid/temp"

def generate_fuzz_input(seed):
    random.seed(seed)
    num_chunks = random.randint(1, 10)
    data = bytearray()

    is_malformed = random.random() < 0.1

    for i in range(num_chunks):
        magic = b"ARTF"
        if is_malformed and i == num_chunks - 1 and random.random() < 0.5:
            magic = b"BADF"

        chunk_type = random.randint(0, 3)
        payload_size = random.randint(0, 1024)
        payload = bytes([random.randint(0, 255) for _ in range(payload_size)])

        chunk_data = magic + struct.pack("<B", chunk_type) + struct.pack("<I", payload_size) + payload

        if is_malformed and i == num_chunks - 1 and random.random() < 0.5:
            # Truncate chunk
            trunc_len = random.randint(1, len(chunk_data) - 1)
            chunk_data = chunk_data[:trunc_len]

        data.extend(chunk_data)

    return bytes(data)

def test_fuzz_equivalence():
    oracle_path = "/app/bin/filter_oracle"
    agent_path = "/home/user/filter_archive"

    assert os.path.isfile(agent_path), f"Agent binary missing at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary at {agent_path} is not executable"

    in_file = "/tmp/fuzz_in.arf"
    oracle_out = "/tmp/oracle_out.arf"
    agent_out = "/tmp/agent_out.arf"

    for i in range(500):
        input_data = generate_fuzz_input(seed=i)

        with open(in_file, "wb") as f:
            f.write(input_data)

        if os.path.exists(oracle_out):
            os.remove(oracle_out)
        if os.path.exists(agent_out):
            os.remove(agent_out)

        oracle_proc = subprocess.run([oracle_path, in_file, oracle_out], capture_output=True)
        agent_proc = subprocess.run([agent_path, in_file, agent_out], capture_output=True)

        assert oracle_proc.returncode == agent_proc.returncode, f"Exit code mismatch on seed {i}. Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}"

        oracle_out_exists = os.path.exists(oracle_out)
        agent_out_exists = os.path.exists(agent_out)

        assert oracle_out_exists == agent_out_exists, f"Output file existence mismatch on seed {i}. Oracle created: {oracle_out_exists}, Agent created: {agent_out_exists}"

        if oracle_out_exists:
            with open(oracle_out, "rb") as f:
                oracle_data = f.read()
            with open(agent_out, "rb") as f:
                agent_data = f.read()

            assert oracle_data == agent_data, f"Output data mismatch on seed {i}"

def test_atomic_rename():
    agent_path = "/home/user/filter_archive"
    in_file = "/tmp/fuzz_in_atomic.arf"
    agent_out = "/tmp/agent_out_atomic.arf"

    with open(in_file, "wb") as f:
        f.write(b"ARTF\x00\x00\x00\x00\x00")

    if os.path.exists(agent_out):
        os.remove(agent_out)

    proc = subprocess.run(
        ["strace", "-e", "trace=rename,renameat,renameat2", agent_path, in_file, agent_out],
        capture_output=True,
        text=True
    )

    assert proc.returncode == 0, "Agent failed to process valid file during strace"
    assert "rename" in proc.stderr, "Agent did not use rename syscalls for atomic write"