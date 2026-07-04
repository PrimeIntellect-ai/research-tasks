# test_final_state.py
import os
import subprocess
import random
import string
import urllib.request
import urllib.error
import pytest

ORACLE_PATH = "/app/oracle_processor"
AGENT_PATH = "/home/user/processor.py"

def test_fuzz_equivalence():
    """Test that the agent's processor script perfectly matches the oracle binary."""
    assert os.path.isfile(AGENT_PATH), f"Agent script missing: {AGENT_PATH}"
    assert os.path.isfile(ORACLE_PATH), f"Oracle missing: {ORACLE_PATH}"

    random.seed(42)
    charset = string.printable

    for i in range(100):
        length = random.randint(0, 5000)
        input_data = "".join(random.choice(charset) for _ in range(length)).encode('utf-8')

        oracle_proc = subprocess.run([ORACLE_PATH], input=input_data, capture_output=True)
        assert oracle_proc.returncode == 0, f"Oracle failed on input {i}"
        oracle_out = oracle_proc.stdout

        agent_proc = subprocess.run(["python3", AGENT_PATH], input=input_data, capture_output=True)
        assert agent_proc.returncode == 0, f"Agent script failed on input {i}. Stderr: {agent_proc.stderr.decode(errors='replace')}"
        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on input {i} (length {length}).\n"
                f"Input data (repr): {input_data!r}\n"
                f"Expected (Oracle): {oracle_out!r}\n"
                f"Got (Agent): {agent_out!r}"
            )

def test_end_to_end_service():
    """Test that the Nginx -> Gunicorn -> Flask -> processor.py pipeline works end-to-end."""
    url = "http://127.0.0.1:8080/process"
    data = b"Hello World"

    try:
        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            body = response.read()
            # "Hello World" -> ROT13 -> "Uryyb Jbeyq" -> Reversed -> "qlyeJ byyrU"
            expected = b"qlyeJ byyrU"
            assert body == expected, f"End-to-end transformation failed. Expected {expected!r}, got {body!r}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"HTTP Error received from Nginx: {e.code} {e.reason}")
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx at {url}: {e.reason}")
    except Exception as e:
        pytest.fail(f"Unexpected error during end-to-end request: {e}")