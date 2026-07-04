# test_final_state.py

import os
import random
import string
import subprocess
import urllib.request

def test_executable_exists():
    agent_path = "/home/user/transform_backend"
    assert os.path.isfile(agent_path), f"The executable {agent_path} is missing."
    assert os.access(agent_path, os.X_OK), f"The file {agent_path} is not executable."

def test_nginx_proxy():
    # Test that Nginx is proxying correctly to the FastCGI backend
    data = b"aabbbcc"
    req = urllib.request.Request("http://127.0.0.1:8080/api", data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            body = response.read().decode('utf-8').strip()
            # The exact output depends on the oracle, but we expect it to succeed.
            assert len(body) > 0, "Received empty response from Nginx."
    except urllib.error.HTTPError as e:
        assert False, f"Nginx proxy returned HTTP error: {e.code}"
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to Nginx proxy: {e.reason}"
    except Exception as e:
        assert False, f"Nginx proxy test failed: {e}"

def test_fuzz_equivalence():
    oracle_path = "/opt/oracle_transform"
    agent_path = "/home/user/transform_backend"

    assert os.path.isfile(oracle_path), f"Oracle program {oracle_path} missing."
    assert os.path.isfile(agent_path), f"Agent program {agent_path} missing."

    random.seed(42)
    chars = string.ascii_letters + string.digits

    env = os.environ.copy()
    env["LANG"] = "en_US.UTF-8"
    env["TZ"] = "UTC"

    for i in range(1000):
        length = random.randint(1, 500)
        test_input = "".join(random.choices(chars, k=length))

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [oracle_path], 
                input=test_input, 
                text=True, 
                capture_output=True, 
                env=env, 
                timeout=2
            )
            oracle_out = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            assert False, f"Oracle program timed out on input: {test_input}"

        # Run agent
        try:
            agent_proc = subprocess.run(
                [agent_path], 
                input=test_input, 
                text=True, 
                capture_output=True, 
                env=env, 
                timeout=2
            )
            agent_out = agent_proc.stdout
        except subprocess.TimeoutExpired:
            assert False, f"Agent program timed out on input: {test_input}"

        assert agent_proc.returncode == 0, f"Agent program crashed (return code {agent_proc.returncode}) on input: '{test_input}'"
        assert agent_out == oracle_out, (
            f"Output mismatch on input '{test_input}'.\n"
            f"Expected (Oracle): '{oracle_out}'\n"
            f"Got (Agent): '{agent_out}'"
        )