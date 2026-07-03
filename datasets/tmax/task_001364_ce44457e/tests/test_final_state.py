# test_final_state.py
import os
import subprocess
import random
import string
import pytest

def generate_arg1():
    v = random.choice(['1', '2', '3'])
    path_len = random.randint(5, 10)
    path_str = ''.join(random.choices(string.ascii_lowercase, k=path_len))
    res = f"/api/v{v}/{path_str}"

    if random.random() < 0.5:
        return res

    res += "?"
    num_extra = random.randint(0, 3)
    params = []
    for _ in range(1 + num_extra):
        key = ''.join(random.choices(string.ascii_lowercase, k=3))
        val_len = random.randint(1, 4)
        val = ''.join(random.choices(string.digits, k=val_len))
        params.append(f"{key}={val}")
    res += "&".join(params)
    return res

def generate_arg2():
    v1 = random.choice(['1', '2', '3'])
    v2 = random.choice(string.digits)
    v3 = random.choice(string.digits)
    return f"{v1}.{v2}.{v3}"

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_router"
    agent_cmd = ["python3", "/home/user/router_cli.py"]

    assert os.path.isfile(oracle_path), f"Oracle not found at {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle at {oracle_path} is not executable"
    assert os.path.isfile("/home/user/router_cli.py"), "Agent script /home/user/router_cli.py not found"

    random.seed(42)
    N = 200

    for i in range(N):
        arg1 = generate_arg1()
        arg2 = generate_arg2()

        oracle_res = subprocess.run([oracle_path, arg1, arg2], capture_output=True, text=True)
        agent_res = subprocess.run(agent_cmd + [arg1, arg2], capture_output=True, text=True)

        assert oracle_res.returncode == 0, f"Oracle failed on input: {arg1} {arg2}\nStderr: {oracle_res.stderr}"
        assert agent_res.returncode == 0, f"Agent script failed on input: {arg1} {arg2}\nStderr: {agent_res.stderr}"

        oracle_out = oracle_res.stdout.strip()
        agent_out = agent_res.stdout.strip()

        assert oracle_out == agent_out, (
            f"Mismatch on iteration {i}!\n"
            f"Input arg1 (path): {arg1}\n"
            f"Input arg2 (version): {arg2}\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output: {agent_out}"
        )