# test_final_state.py

import os
import subprocess
import random
import string
import socket
import tempfile
import time
import pytest

ORACLE_PATH = "/app/oracle_processor"
AGENT_PATH = "/app/backend-repo/backend_processor"

def test_fuzz_equivalence():
    """
    Fuzz-equivalence verifier:
    Generate N=1000 random binary and text streams, length 1 to 10000 bytes.
    Compare stdout of oracle and agent program.
    """
    assert os.path.isfile(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle not executable"
    assert os.path.isfile(AGENT_PATH), f"Agent program missing at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent program not executable"

    random.seed(42)

    for i in range(1000):
        length = random.randint(1, 10000)
        if random.choice([True, False]):
            # Text stream
            chars = string.ascii_letters + string.digits + string.punctuation + " \n\t"
            input_data = "".join(random.choice(chars) for _ in range(length)).encode('utf-8')
        else:
            # Binary stream
            input_data = bytes(random.getrandbits(8) for _ in range(length))

        try:
            oracle_proc = subprocess.run(
                [ORACLE_PATH],
                input=input_data,
                capture_output=True,
                timeout=2
            )
            oracle_out = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input {i}")

        try:
            agent_proc = subprocess.run(
                [AGENT_PATH],
                input=input_data,
                capture_output=True,
                timeout=2
            )
            agent_out = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent program timed out on input {i}")

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on input {i} (length {length}).\n"
                f"Oracle output: {oracle_out!r}\n"
                f"Agent output: {agent_out!r}\n"
                f"Input data snippet: {input_data[:100]!r}"
            )

def test_services_running_and_integration():
    """
    Test end-to-end flow:
    Frontend listening on TCP 8000, backend on TCP 8001.
    Send a filename with spaces to localhost:8000, get hash back.
    """
    # Create a test file with spaces
    with tempfile.NamedTemporaryFile(prefix="test file ", suffix=" with spaces.txt", delete=False) as f:
        test_filepath = f.name
        test_content = b"Hello World! This is a test file to hash.\n"
        f.write(test_content)

    try:
        # Get expected hash from oracle
        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=test_content,
            capture_output=True,
            timeout=2
        )
        expected_hash = oracle_proc.stdout

        # Connect to frontend
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5.0)
        try:
            s.connect(("127.0.0.1", 8000))
        except ConnectionRefusedError:
            pytest.fail("Frontend service is not listening on 127.0.0.1:8000")

        # Send filename
        s.sendall(f"{test_filepath}\n".encode('utf-8'))

        # Read response
        response = b""
        while True:
            try:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response += chunk
            except socket.timeout:
                break

        s.close()

        assert response == expected_hash, (
            f"End-to-end integration failed. Expected hash {expected_hash!r}, "
            f"but got {response!r}"
        )
    finally:
        if os.path.exists(test_filepath):
            os.remove(test_filepath)