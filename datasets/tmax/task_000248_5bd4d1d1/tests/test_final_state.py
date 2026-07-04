# test_final_state.py

import os
import subprocess
import random
import urllib.parse
import pytest

def test_files_exist():
    assert os.path.isfile('/home/user/auth_checker.cpp'), "Missing /home/user/auth_checker.cpp"
    assert os.path.isfile('/home/user/Makefile'), "Missing /home/user/Makefile"

def test_makefile_proxy_target():
    with open('/home/user/Makefile', 'r') as f:
        content = f.read()
    assert 'proxy:' in content, "Makefile is missing the 'proxy:' target"

def test_binary_exists_and_executable():
    # Attempt to build if not exists
    if not os.path.isfile('/home/user/auth_checker'):
        subprocess.run(['make'], cwd='/home/user', capture_output=True)

    assert os.path.isfile('/home/user/auth_checker'), "Binary /home/user/auth_checker was not built"
    assert os.access('/home/user/auth_checker', os.X_OK), "Binary /home/user/auth_checker is not executable"

def generate_fuzz_inputs(n=1000):
    random.seed(42)
    services = ['GATEWAY', 'AUTH', 'USER_DB', 'PAYMENT', 'LEDGER', 'FRAUD']
    inputs = []
    for _ in range(n):
        parts = []
        num_parts = random.randint(1, 15)
        for _ in range(num_parts):
            if random.random() < 0.7:
                parts.append(random.choice(services))
            else:
                noise = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-%', k=random.randint(2, 10)))
                parts.append(noise)
        raw_str = ','.join(parts)
        encoded = urllib.parse.quote(raw_str)
        # Ensure length constraint (roughly)
        if len(encoded) > 150:
            encoded = encoded[:150]
        inputs.append(encoded)
    return inputs

def test_fuzz_equivalence():
    oracle_path = '/app/oracle_auth_checker'
    agent_path = '/home/user/auth_checker'

    assert os.path.isfile(oracle_path), "Oracle binary missing"
    assert os.path.isfile(agent_path), "Agent binary missing"

    inputs = generate_fuzz_inputs(1000)

    for fuzzed_input in inputs:
        oracle_proc = subprocess.run([oracle_path, fuzzed_input], capture_output=True, text=True)
        agent_proc = subprocess.run([agent_path, fuzzed_input], capture_output=True, text=True)

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, (
            f"Mismatch on input: {fuzzed_input}\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output: {agent_out}"
        )