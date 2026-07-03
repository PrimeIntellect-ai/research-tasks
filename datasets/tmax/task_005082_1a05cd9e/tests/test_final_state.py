# test_final_state.py

import os
import random
import subprocess
import pytest

def test_rules_patched_exists():
    assert os.path.isfile("/home/user/rules_patched.bc"), "The patched bytecode file /home/user/rules_patched.bc is missing."

def test_telemetry_eval_exists():
    assert os.path.isfile("/home/user/telemetry_eval"), "The Go compiled binary /home/user/telemetry_eval is missing."
    assert os.access("/home/user/telemetry_eval", os.X_OK), "The Go compiled binary /home/user/telemetry_eval is not executable."

def test_fuzz_equivalence():
    oracle_bin = "/app/oracle_bin"
    agent_bin = "/home/user/telemetry_eval"
    patched_bc = "/home/user/rules_patched.bc"

    assert os.path.isfile(oracle_bin), f"Oracle binary missing at {oracle_bin}"

    random.seed(42)
    N = 100

    for i in range(N):
        # Generate random sequence of 10 to 50 integers (0 to 1000)
        num_ints = random.randint(10, 50)
        input_ints = [str(random.randint(0, 1000)) for _ in range(num_ints)]
        input_str = "\n".join(input_ints) + "\n"
        input_bytes = input_str.encode('utf-8')

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_bin, patched_bc],
            input=input_bytes,
            capture_output=True,
            timeout=5
        )
        oracle_out = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            [agent_bin, patched_bc],
            input=input_bytes,
            capture_output=True,
            timeout=5
        )
        agent_out = agent_proc.stdout

        assert oracle_proc.returncode == agent_proc.returncode, (
            f"Return code mismatch on input {i}.\n"
            f"Input:\n{input_str}\n"
            f"Oracle return code: {oracle_proc.returncode}\n"
            f"Agent return code: {agent_proc.returncode}\n"
            f"Oracle stderr: {oracle_proc.stderr.decode('utf-8', errors='replace')}\n"
            f"Agent stderr: {agent_proc.stderr.decode('utf-8', errors='replace')}"
        )

        assert oracle_out == agent_out, (
            f"Output mismatch on input {i}.\n"
            f"Input:\n{input_str}\n"
            f"Oracle output:\n{oracle_out.decode('utf-8', errors='replace')}\n"
            f"Agent output:\n{agent_out.decode('utf-8', errors='replace')}"
        )