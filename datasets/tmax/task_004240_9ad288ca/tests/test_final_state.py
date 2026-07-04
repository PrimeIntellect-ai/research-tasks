# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def generate_random_string(min_len, max_len, chars):
    length = random.randint(min_len, max_len)
    return ''.join(random.choice(chars) for _ in range(length))

def test_fuzz_equivalence_migrator():
    oracle_path = "/app/legacy_router_configurator"
    agent_script = "/home/user/migrator.py"

    assert os.path.exists(oracle_path), f"Oracle binary missing at {oracle_path}"
    assert os.path.exists(agent_script), f"Agent script missing at {agent_script}"

    random.seed(42)

    chars_tz = string.ascii_letters + string.digits + '/'
    chars_loc = string.ascii_letters + string.digits + '.' + '-'
    chars_int = string.digits
    chars_reg = string.ascii_letters + string.digits + '-'

    for i in range(100):
        arg1 = generate_random_string(3, 20, chars_tz)
        arg2 = generate_random_string(5, 15, chars_loc)
        arg3 = generate_random_string(5, 12, chars_int)
        arg4 = generate_random_string(5, 15, chars_reg)

        args = [arg1, arg2, arg3, arg4]

        oracle_cmd = [oracle_path] + args
        agent_cmd = ["python3", agent_script] + args

        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

        assert oracle_res.returncode == 0, f"Oracle failed on input {args}"
        assert agent_res.returncode == 0, f"Agent script failed on input {args}. Error: {agent_res.stderr}"

        oracle_out = oracle_res.stdout.strip()
        agent_out = agent_res.stdout.strip()

        assert oracle_out == agent_out, (
            f"Output mismatch on input {args}.\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output: {agent_out}"
        )

def test_generate_tag_script():
    script_path = "/home/user/generate_tag.sh"
    assert os.path.exists(script_path), f"Script missing at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

    with open(script_path, 'r') as f:
        content = f.read()

    assert 'df' in content, "Script does not contain 'df'"
    assert '/etc/timezone' in content, "Script does not contain '/etc/timezone'"
    assert '/etc/default/locale' in content, "Script does not contain '/etc/default/locale'"
    assert '/home/user/migrator.py' in content, "Script does not contain '/home/user/migrator.py'"

def test_routing_tag_service():
    service_path = "/home/user/routing-tag.service"
    assert os.path.exists(service_path), f"Service file missing at {service_path}"

    with open(service_path, 'r') as f:
        content = f.read()

    assert '[Unit]' in content, "Service file missing [Unit] section"
    assert '[Service]' in content, "Service file missing [Service] section"
    assert 'Type=oneshot' in content, "Service file missing Type=oneshot"
    assert 'ExecStart=/home/user/generate_tag.sh' in content, "Service file missing ExecStart=/home/user/generate_tag.sh"