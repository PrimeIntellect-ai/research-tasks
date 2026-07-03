# test_final_state.py

import os
import random
import string
import subprocess
import urllib.request
import urllib.error
import pytest

def test_nginx_routing():
    """
    Test that Nginx is correctly routing to the Flask backend and returning a successful response.
    """
    data = b"test input line"
    req = urllib.request.Request("http://127.0.0.1:8080/api/process", data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200 OK, got {response.status}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"HTTP request failed with status {e.code}. Nginx routing is likely still broken (e.g., 502 Bad Gateway) or the backend failed.")
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx at 127.0.0.1:8080: {e.reason}")

def test_processor_fuzz_equivalence():
    """
    Fuzz test the agent's processor.py against the oracle_processor binary.
    """
    oracle_path = "/app/oracle_processor"
    agent_path = "/home/user/deployment/processor.py"

    assert os.path.isfile(oracle_path), f"Oracle binary missing at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent script missing at {agent_path}"

    random.seed(42)

    # Generate a pool of characters, excluding newlines to ensure it's treated as a single line
    chars = [c for c in string.printable if c not in ('\n', '\r', '\x0b', '\x0c')]
    # Add some common unicode characters
    chars += [chr(i) for i in range(0x00A0, 0x02AF)]

    for _ in range(1000):
        length = random.randint(0, 500)
        input_str = "".join(random.choice(chars) for _ in range(length))
        # The task specifies reading a line of text, so we append a newline
        input_bytes = (input_str + "\n").encode('utf-8')

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [oracle_path],
                input=input_bytes,
                capture_output=True,
                timeout=2
            )
            oracle_out = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail("Oracle binary timed out.")
        except Exception as e:
            pytest.fail(f"Oracle failed to run: {e}")

        # Run agent
        try:
            agent_proc = subprocess.run(
                ["python3", agent_path],
                input=input_bytes,
                capture_output=True,
                timeout=2
            )
            agent_out = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on input: {repr(input_str[:50])}...")
        except Exception as e:
            pytest.fail(f"Agent script failed to run: {e}")

        assert agent_out == oracle_out, (
            f"Output mismatch on input (length {length}): {repr(input_str[:50])}...\n"
            f"Oracle output: {repr(oracle_out[:100])}\n"
            f"Agent output: {repr(agent_out[:100])}"
        )