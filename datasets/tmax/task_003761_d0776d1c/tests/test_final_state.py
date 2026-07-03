# test_final_state.py

import os
import random
import string
import subprocess
import urllib.request
import pytest

def test_nginx_conf_updated():
    path = "/home/user/app-config/nginx.conf"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "/tmp/app_backend_real.sock" in content, "nginx.conf does not point to the correct socket path."

def test_git_hook_setup():
    hook_path = "/home/user/deploy.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Git hook {hook_path} does not exist."
    assert os.access(hook_path, os.X_OK), f"Git hook {hook_path} is not executable."

def test_nginx_serving_backend():
    # Nginx should now successfully proxy to the backend
    try:
        req = urllib.request.Request("http://127.0.0.1:8080")
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Nginx returned HTTP error: {e.code}")
    except Exception as e:
        pytest.fail(f"Failed to connect to Nginx: {e}")

def test_token_generator_fuzz_equivalence():
    oracle = "/app/token_generator"
    agent = "/home/user/token_generator.py"

    assert os.path.isfile(agent), f"Agent script {agent} does not exist."

    random.seed(42)
    chars = string.ascii_letters + string.digits

    for _ in range(200):
        length = random.randint(5, 32)
        test_input = "".join(random.choice(chars) for _ in range(length))

        try:
            oracle_proc = subprocess.run(
                [oracle, test_input], 
                capture_output=True, 
                text=True, 
                check=True
            )
            oracle_out = oracle_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {test_input!r}: {e.stderr}")

        try:
            agent_proc = subprocess.run(
                ["/usr/bin/python3", agent, test_input], 
                capture_output=True, 
                text=True, 
                check=True
            )
            agent_out = agent_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent script failed on input {test_input!r}: {e.stderr}")

        assert oracle_out == agent_out, (
            f"Output mismatch on input {test_input!r}.\n"
            f"Oracle output: {oracle_out!r}\n"
            f"Agent output:  {agent_out!r}"
        )