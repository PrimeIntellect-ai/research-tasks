# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error
import random
import binascii
import pytest

def test_nginx_routing():
    """Test if Nginx correctly routes requests to the Go API."""
    url = "http://localhost:8080/api/v1/ping"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            status_code = response.getcode()
            body = response.read().decode('utf-8').strip()

            assert status_code == 200, f"Expected HTTP 200, got {status_code}"
            assert body == "pong", f"Expected response body 'pong', got '{body}'"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect or retrieve data from {url}: {e}")

def test_decoder_exists_and_executable():
    """Ensure the user's decoder script exists and is executable."""
    decoder_path = '/home/user/decoder'
    assert os.path.isfile(decoder_path), f"Decoder script {decoder_path} is missing."
    assert os.access(decoder_path, os.X_OK), f"Decoder script {decoder_path} is not executable."

def test_decoder_fuzz_equivalence():
    """Fuzz the user's decoder against the oracle."""
    oracle_path = '/app/oracle_decoder'
    agent_path = '/home/user/decoder'

    assert os.path.isfile(oracle_path), f"Oracle {oracle_path} is missing."

    random.seed(42)

    for i in range(100):
        # Generate random byte array of length 0 to 256
        length = random.randint(0, 256)
        random_bytes = bytearray(random.getrandbits(8) for _ in range(length))
        hex_input = binascii.hexlify(random_bytes).decode('ascii')

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path, hex_input],
            capture_output=True
        )
        # We don't check oracle_proc.returncode because it might be non-zero for some inputs, 
        # but we expect the agent to match it exactly.

        # Run agent
        agent_proc = subprocess.run(
            [agent_path, hex_input],
            capture_output=True
        )

        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Output mismatch on input '{hex_input}' (length {length}).\n"
            f"Oracle stdout: {oracle_proc.stdout!r}\n"
            f"Agent stdout: {agent_proc.stdout!r}"
        )