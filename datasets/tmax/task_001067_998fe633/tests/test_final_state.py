# test_final_state.py

import os
import subprocess
import random
import string
import urllib.request
import urllib.parse
import json
import time

def test_fuzz_equivalence():
    oracle_path = "/home/user/oracle_hash"
    agent_path = "/home/user/workspace/build/compute_hash"

    assert os.path.isfile(oracle_path), f"Oracle binary not found at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent binary not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary at {agent_path} is not executable"

    random.seed(42)
    alphanumeric = string.ascii_letters + string.digits

    for i in range(1000):
        length = random.randint(1, 1024)
        test_input = ''.join(random.choices(alphanumeric, k=length))

        oracle_proc = subprocess.run(
            [oracle_path, test_input],
            capture_output=True,
            text=True,
            check=False
        )
        agent_proc = subprocess.run(
            [agent_path, test_input],
            capture_output=True,
            text=True,
            check=False
        )

        assert oracle_proc.returncode == 0, f"Oracle failed on input: {test_input}"
        assert agent_proc.returncode == 0, f"Agent failed on input: {test_input}"

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, (
            f"Mismatch on input '{test_input}'. "
            f"Oracle output: '{oracle_out}', Agent output: '{agent_out}'"
        )

def test_api_integration_and_caching():
    # Wait briefly to ensure Flask is up if it was just started
    time.sleep(1)

    random.seed(1337)
    alphanumeric = string.ascii_letters + string.digits
    test_input = ''.join(random.choices(alphanumeric, k=50))

    oracle_proc = subprocess.run(
        ["/home/user/oracle_hash", test_input],
        capture_output=True,
        text=True,
        check=True
    )
    expected_hash = int(oracle_proc.stdout.strip())

    url = "http://127.0.0.1:5000/hash"
    data = urllib.parse.urlencode({'data': test_input}).encode('utf-8')

    # First request: should not be cached (or might be if previous tests ran, but let's check hash)
    req1 = urllib.request.Request(url, data=data)
    try:
        with urllib.request.urlopen(req1, timeout=5) as response:
            res1 = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        raise AssertionError(f"Failed to connect to Flask API or parse response: {e}")

    assert 'hash' in res1, "API response missing 'hash' key"
    assert res1['hash'] == expected_hash, f"API returned wrong hash. Expected {expected_hash}, got {res1['hash']}"

    # Second request: must be cached
    req2 = urllib.request.Request(url, data=data)
    try:
        with urllib.request.urlopen(req2, timeout=5) as response:
            res2 = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        raise AssertionError(f"Failed to connect to Flask API on second request: {e}")

    assert res2.get('cached') is True, "Second API request did not return 'cached': true"
    assert res2['hash'] == expected_hash, f"API returned wrong hash on cached request. Expected {expected_hash}, got {res2['hash']}"