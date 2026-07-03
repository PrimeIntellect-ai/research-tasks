# test_final_state.py
import os
import json
import random
import string
import subprocess
import tempfile
import pytest

def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

def generate_random_string(min_len=1, max_len=20):
    length = random.randint(min_len, max_len)
    chars = string.ascii_letters + string.digits + "-_."
    return "".join(random.choices(chars, k=length))

def generate_random_package():
    # To ensure we hit the edge cases, occasionally inject "eval", "exec", "npm", "0."
    name = generate_random_string()
    if random.random() < 0.1:
        name += "eval"
    elif random.random() < 0.1:
        name += "exec"

    version = generate_random_string()
    if random.random() < 0.2:
        version = "0." + version

    ecosystem = generate_random_string()
    if random.random() < 0.3:
        ecosystem = "npm"

    return {
        "name": name,
        "version": version,
        "ecosystem": ecosystem
    }

def generate_random_input():
    num_packages = random.randint(0, 10)
    packages = [generate_random_package() for _ in range(num_packages)]
    return {
        "client_ip": generate_random_ip(),
        "packages": packages
    }

def test_fuzz_equivalence():
    oracle_path = "/app/build_sec_proxy"
    agent_file = "/home/user/build_sec_proxy.go"

    assert os.path.isfile(oracle_path), f"Oracle binary missing at {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle binary not executable at {oracle_path}"
    assert os.path.isfile(agent_file), f"Agent Go file missing at {agent_file}"

    random.seed(42)
    num_tests = 500

    with tempfile.TemporaryDirectory() as temp_dir:
        for i in range(num_tests):
            input_data = generate_random_input()
            input_file = os.path.join(temp_dir, f"input_{i}.json")
            with open(input_file, "w") as f:
                json.dump(input_data, f)

            # Run oracle
            oracle_res = subprocess.run(
                [oracle_path, input_file],
                capture_output=True,
                text=True
            )
            oracle_output = oracle_res.stdout.strip()

            # Run agent
            agent_res = subprocess.run(
                ["go", "run", agent_file, input_file],
                capture_output=True,
                text=True
            )
            agent_output = agent_res.stdout.strip()

            if oracle_output != agent_output:
                error_msg = (
                    f"Mismatch on test case {i}!\n"
                    f"Input: {json.dumps(input_data)}\n"
                    f"Oracle output: {oracle_output}\n"
                    f"Agent output:  {agent_output}\n"
                    f"Agent stderr:  {agent_res.stderr.strip()}"
                )
                pytest.fail(error_msg)