# test_final_state.py

import os
import random
import subprocess
import pytest

def test_vm_router_exists():
    path = '/home/user/vm_router.py'
    assert os.path.exists(path), f"Student script {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."

def test_fuzz_equivalence():
    agent_script = '/home/user/vm_router.py'
    oracle_bin = '/app/oracle_router'

    assert os.path.exists(agent_script), f"Agent script missing: {agent_script}"
    assert os.path.exists(oracle_bin), f"Oracle binary missing: {oracle_bin}"

    random.seed(42)
    hex_chars = "0123456789ABCDEF"

    iterations = 1000

    for _ in range(iterations):
        # Generate random length between 2 and 100, must be even for valid hex bytes
        length = random.choice(range(2, 102, 2))
        hex_payload = "".join(random.choice(hex_chars) for _ in range(length))

        # Run oracle
        oracle_cmd = [oracle_bin, hex_payload]
        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)

        # Run agent
        agent_cmd = ["python3", agent_script, hex_payload]
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

        # Check success and equivalence
        assert agent_res.returncode == 0, f"Agent script failed on input {hex_payload}. Stderr: {agent_res.stderr}"
        assert oracle_res.returncode == 0, f"Oracle failed on input {hex_payload}. Stderr: {oracle_res.stderr}"

        oracle_out = oracle_res.stdout.strip()
        agent_out = agent_res.stdout.strip()

        assert agent_out == oracle_out, (
            f"Mismatch on payload {hex_payload}.\n"
            f"Expected (Oracle): {repr(oracle_out)}\n"
            f"Got (Agent)      : {repr(agent_out)}"
        )