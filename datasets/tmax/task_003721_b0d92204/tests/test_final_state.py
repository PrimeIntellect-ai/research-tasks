# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def generate_fuzz_inputs(n=100, seed=42):
    random.seed(seed)
    inputs = []
    for _ in range(n):
        username_len = random.randint(3, 10)
        username = ''.join(random.choices(string.ascii_lowercase, k=username_len))
        fingerprint_chars = string.ascii_letters + string.digits + "+/"
        fingerprint = ''.join(random.choices(fingerprint_chars, k=43))
        has_sudo = random.choice(['0', '1'])
        inputs.append(f"{username},SHA256:{fingerprint},{has_sudo}\n")
    return inputs

def test_libb64_compiled():
    lib_path = "/app/libb64-1.2.1/src/libb64.a"
    assert os.path.isfile(lib_path), f"Expected static library {lib_path} does not exist. Did you fix the Makefile and run make?"

def test_agent_executable_exists():
    agent_path = "/home/user/audit_token_gen"
    assert os.path.isfile(agent_path), f"Agent executable {agent_path} does not exist."
    assert os.access(agent_path, os.X_OK), f"Agent {agent_path} is not executable."

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_audit_token_gen"
    agent_path = "/home/user/audit_token_gen"

    assert os.path.isfile(oracle_path), f"Oracle {oracle_path} missing."
    assert os.path.isfile(agent_path), f"Agent {agent_path} missing."

    inputs = generate_fuzz_inputs(100, seed=12345)

    for i, inp in enumerate(inputs):
        # Run oracle
        proc_oracle = subprocess.run(
            [oracle_path],
            input=inp.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # Run agent
        proc_agent = subprocess.run(
            [agent_path],
            input=inp.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        assert proc_agent.returncode == proc_oracle.returncode, \
            f"Return code mismatch on input {i}: {inp!r}. Oracle: {proc_oracle.returncode}, Agent: {proc_agent.returncode}"

        assert proc_agent.stdout == proc_oracle.stdout, \
            f"Stdout mismatch on input {i}: {inp!r}.\nOracle stdout: {proc_oracle.stdout!r}\nAgent stdout: {proc_agent.stdout!r}"