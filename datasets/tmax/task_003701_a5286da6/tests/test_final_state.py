# test_final_state.py

import os
import subprocess
import random
import time
import urllib.request
import urllib.parse
import pytest

def generate_rpn(length):
    if length % 2 == 0:
        length += 1

    num_operands = (length + 1) // 2
    num_operators = (length - 1) // 2

    stack = 0
    expr = []

    operands_left = num_operands
    operators_left = num_operators

    while operands_left > 0 or operators_left > 0:
        choices = []
        if operands_left > 0:
            choices.append('num')
        if operators_left > 0 and stack >= 2:
            choices.append('op')

        choice = random.choice(choices)
        if choice == 'num':
            expr.append(str(random.randint(-1000, 1000)))
            stack += 1
            operands_left -= 1
        else:
            expr.append(random.choice(['+', '-', '*']))
            stack -= 1
            operators_left -= 1

    return " ".join(expr)


def test_fasteval_binary_exists():
    assert os.path.isfile('/home/user/fasteval'), "The compiled binary /home/user/fasteval does not exist."
    assert os.access('/home/user/fasteval', os.X_OK), "/home/user/fasteval is not executable."

def test_fuzz_equivalence():
    oracle_path = '/app/oracle.py'
    agent_path = '/home/user/fasteval'

    assert os.path.isfile(oracle_path), f"Oracle {oracle_path} missing."
    assert os.path.isfile(agent_path), f"Agent binary {agent_path} missing."

    random.seed(42)

    for _ in range(1000):
        length = random.choice(range(3, 26, 2))
        expr = generate_rpn(length)

        # Run oracle
        try:
            oracle_res = subprocess.run(
                ['python3', oracle_path, expr],
                capture_output=True, text=True, check=True
            )
            oracle_output = oracle_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            continue # Skip if oracle fails for some reason

        # Run agent
        try:
            agent_res = subprocess.run(
                [agent_path, expr],
                capture_output=True, text=True, check=True
            )
            agent_output = agent_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent binary failed on input: '{expr}'.\nError: {e.stderr}")

        assert agent_output == oracle_output, (
            f"Output mismatch on input: '{expr}'\n"
            f"Expected (Oracle): {oracle_output}\n"
            f"Got (Agent): {agent_output}"
        )

def test_app_py_configured():
    with open('/home/user/app.py', 'r') as f:
        content = f.read()
    assert '/home/user/fasteval' in content, "app.py does not call /home/user/fasteval"
    assert '6379' in content, "app.py does not use Redis port 6379"

def test_nginx_configured():
    with open('/home/user/nginx.conf', 'r') as f:
        content = f.read()
    assert 'proxy_pass' in content, "nginx.conf does not contain a proxy_pass directive"
    assert '5000' in content, "nginx.conf does not proxy to port 5000"

def test_end_to_end_flow():
    # Attempt to start services if not already running
    subprocess.run(['bash', '/app/start_services.sh'], capture_output=True)
    time.sleep(2) # Give services a moment to start

    expr = "3 4 + 2 *"
    encoded_expr = urllib.parse.quote(expr)
    url = f"http://127.0.0.1:8080/api/eval?q={encoded_expr}"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.getcode()
            body = response.read().decode('utf-8').strip()

            assert status == 200, f"Expected HTTP 200, got {status}"
            assert body == "14", f"Expected result '14' for expression '{expr}', got '{body}'"
    except Exception as e:
        pytest.fail(f"End-to-end test failed: {e}")