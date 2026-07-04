# test_final_state.py

import os
import subprocess
import random
import urllib.request
import urllib.error
import time

def test_nginx_api_proxy():
    """Test that Nginx correctly proxies /api/ requests to the Flask API."""
    url = "http://localhost:8080/api/validate?primer=ACGT"
    max_retries = 5
    for i in range(max_retries):
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=2) as response:
                status = response.getcode()
                body = response.read().decode('utf-8')
                assert status == 200, f"Expected status 200, got {status}"
                assert "valid" in body.lower() or "true" in body.lower() or body, "API response seems incorrect"
                return
        except urllib.error.URLError as e:
            if i == max_retries - 1:
                raise AssertionError(f"Failed to connect to Nginx API proxy at {url}: {e}")
            time.sleep(1)

def test_nginx_cache_proxy():
    """Test that Nginx correctly proxies /cache/ requests to Webdis."""
    url = "http://localhost:8080/cache/SET/testkey/testval"
    max_retries = 5
    for i in range(max_retries):
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=2) as response:
                status = response.getcode()
                body = response.read().decode('utf-8')
                assert status == 200, f"Expected status 200, got {status}"
                return
        except urllib.error.URLError as e:
            if i == max_retries - 1:
                raise AssertionError(f"Failed to connect to Nginx cache proxy at {url}: {e}")
            time.sleep(1)

def test_spectral_dist_fuzz_equivalence():
    """Test the agent's Go binary against the reference oracle using fuzz testing."""
    oracle_path = "/app/oracle/spectral_dist_oracle"
    agent_path = "/home/user/spectral_dist"

    assert os.path.isfile(oracle_path), f"Oracle binary not found at {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle binary is not executable at {oracle_path}"

    assert os.path.isfile(agent_path), f"Agent binary not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary is not executable at {agent_path}"

    random.seed(42)
    charset = "ACGT"
    N = 100

    for _ in range(N):
        length = random.randint(10, 100)
        dna_seq = "".join(random.choices(charset, k=length))

        # Run oracle
        try:
            oracle_result = subprocess.run(
                [oracle_path, dna_seq],
                capture_output=True,
                text=True,
                check=True,
                timeout=2
            )
            oracle_output = oracle_result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise AssertionError(f"Oracle failed on input {dna_seq}:\n{e.stderr}")
        except subprocess.TimeoutExpired:
            raise AssertionError(f"Oracle timed out on input {dna_seq}")

        # Run agent
        try:
            agent_result = subprocess.run(
                [agent_path, dna_seq],
                capture_output=True,
                text=True,
                check=True,
                timeout=2
            )
            agent_output = agent_result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise AssertionError(f"Agent binary failed on input {dna_seq}:\n{e.stderr}")
        except subprocess.TimeoutExpired:
            raise AssertionError(f"Agent binary timed out on input {dna_seq}")

        assert agent_output == oracle_output, (
            f"Mismatch on input: {dna_seq}\n"
            f"Expected (Oracle): {oracle_output}\n"
            f"Got (Agent): {agent_output}"
        )