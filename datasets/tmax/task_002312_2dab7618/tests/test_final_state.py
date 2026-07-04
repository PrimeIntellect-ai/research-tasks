# test_final_state.py

import os
import subprocess
import random
import string
import pytest

def test_admin_password_cracked():
    path = "/home/user/admin_password.txt"
    assert os.path.isfile(path), f"Missing password file at {path}"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "apple", "The cracked password is incorrect."

def test_nginx_config_updated():
    path = "/app/nginx/nginx.conf"
    assert os.path.isfile(path), f"Missing Nginx config at {path}"
    with open(path, "r") as f:
        content = f.read()
    assert "proxy_pass http://127.0.0.1:5000/;" in content or "proxy_pass http://localhost:5000/;" in content, "Nginx config does not contain the correct proxy_pass directive."

def test_flask_config_updated():
    path = "/app/flask/config.py"
    assert os.path.isfile(path), f"Missing Flask config at {path}"
    with open(path, "r") as f:
        content = f.read()
    assert "os.environ.get" in content and "AUTH_SECRET" in content, "Flask config does not read SECRET_KEY from the AUTH_SECRET environment variable."

def test_perm_check_equivalence():
    agent_script = "/home/user/perm_check.py"
    oracle_script = "/app/oracle/reference_perm_check.py"

    assert os.path.isfile(agent_script), f"Missing agent script at {agent_script}"
    assert os.access(agent_script, os.X_OK) or True, "Agent script should be executable, but we will run it with python3."

    random.seed(42)

    for i in range(5000):
        # Generate random 16-character hex string
        token = ''.join(random.choices(string.hexdigits.lower(), k=16))
        # Generate random alphanumeric string of length 4 to 12
        res_len = random.randint(4, 12)
        resource = ''.join(random.choices(string.ascii_letters + string.digits, k=res_len))

        # Run oracle
        oracle_res = subprocess.run(
            ["python3", oracle_script, token, resource],
            capture_output=True, text=True
        )
        oracle_out = oracle_res.stdout.strip()

        # Run agent
        agent_res = subprocess.run(
            ["python3", agent_script, token, resource],
            capture_output=True, text=True
        )
        agent_out = agent_res.stdout.strip()

        assert agent_out == oracle_out, f"Mismatch on input token='{token}', resource='{resource}'. Oracle: '{oracle_out}', Agent: '{agent_out}'"