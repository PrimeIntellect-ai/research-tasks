# test_final_state.py

import os
import subprocess
import random
import string
import urllib.request
import urllib.error
import pytest
import time
import json

ORACLE_PATH = "/opt/oracle/normalizer_oracle"
AGENT_PATH = "/home/user/normalizer"
N_ITERATIONS = 100

def generate_random_input():
    length = random.randint(0, 500)
    # Generate random bytes, including valid/invalid utf-8, +, -, =, spaces, newlines
    choices = [b'+', b'-', b'=', b' ', b'\n', b'\r', b'\t', b'a', b'A', b'1', b'_', b'\xff', b'\xc3\x28']
    res = bytearray()
    for _ in range(length):
        res.extend(random.choice(choices))
    return bytes(res)

def test_fuzz_equivalence():
    """Fuzz test the agent's normalizer against the oracle."""
    assert os.path.isfile(AGENT_PATH), f"Agent normalizer not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent normalizer at {AGENT_PATH} is not executable"

    if not os.path.isfile(ORACLE_PATH):
        pytest.skip(f"Oracle not found at {ORACLE_PATH}, skipping fuzz test.")

    random.seed(42)

    for i in range(N_ITERATIONS):
        inp = generate_random_input()

        oracle_proc = subprocess.run([ORACLE_PATH], input=inp, capture_output=True)
        agent_proc = subprocess.run([AGENT_PATH], input=inp, capture_output=True)

        assert oracle_proc.returncode == agent_proc.returncode, f"Return code mismatch on iteration {i}. Input: {inp!r}. Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}"
        assert oracle_proc.stdout == agent_proc.stdout, f"Stdout mismatch on iteration {i}. Input: {inp!r}.\nOracle:\n{oracle_proc.stdout!r}\nAgent:\n{agent_proc.stdout!r}"
        assert oracle_proc.stderr == agent_proc.stderr, f"Stderr mismatch on iteration {i}. Input: {inp!r}.\nOracle:\n{oracle_proc.stderr!r}\nAgent:\n{agent_proc.stderr!r}"

def test_redis_running_and_configured():
    """Test that Redis is running on port 6379 and has maxmemory set to 10mb."""
    try:
        import redis
        r = redis.Redis(host='127.0.0.1', port=6379, db=0)
        r.ping()
        info = r.info('memory')
        # 10mb is 10485760 bytes
        assert info.get('maxmemory') == 10485760, f"Redis maxmemory is not 10mb. Found: {info.get('maxmemory')}"
    except ImportError:
        # Fallback if redis-py is not installed, use redis-cli
        res = subprocess.run(['redis-cli', 'ping'], capture_output=True, text=True)
        assert 'PONG' in res.stdout, "Redis is not running on port 6379"

        res_conf = subprocess.run(['redis-cli', 'CONFIG', 'GET', 'maxmemory'], capture_output=True, text=True)
        assert '10485760' in res_conf.stdout, f"Redis maxmemory is not 10mb. Found: {res_conf.stdout}"

def test_end_to_end_flow():
    """Test the end-to-end flow from Nginx to Flask to Normalizer to Redis."""
    # Clear redis configs list
    subprocess.run(['redis-cli', 'DEL', 'configs'], capture_output=True)

    payload = b"+ KEY=val\n- OLD\n+ Greeting=Hello \xf0\x9f\x8c\x8d"

    req = urllib.request.Request("http://127.0.0.1:8080/patch", data=payload, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx on port 8080: {e}")

    # Check redis
    res = subprocess.run(['redis-cli', 'LRANGE', 'configs', '0', '-1'], capture_output=True, text=True)
    assert 'key=val' in res.stdout.lower() or 'greeting=hello' in res.stdout.lower() or 'old' in res.stdout.lower(), f"Redis configs list does not contain expected output. Found: {res.stdout}"