# test_final_state.py
import os
import random
import subprocess
import pytest

def generate_inputs(n=1000, seed=42):
    random.seed(seed)
    inputs = []
    ops = ['+', '-', '*', '@']
    while len(inputs) < n:
        num_terms = random.randint(2, 10)
        expr = str(random.randint(1, 100))
        for _ in range(num_terms - 1):
            op = random.choice(ops)
            num = str(random.randint(1, 100))
            sp1 = " " * random.randint(0, 1)
            sp2 = " " * random.randint(0, 1)
            expr += f"{sp1}{op}{sp2}{num}"
        if 3 <= len(expr) <= 50:
            inputs.append(expr)
    return inputs

def test_fuzz_equivalence():
    agent_bin = "/app/math_engine/build/eval_tool"
    oracle_bin = "/app/oracle_eval"

    assert os.path.isfile(agent_bin), f"Agent binary not found at {agent_bin}. Did the build succeed?"
    assert os.access(agent_bin, os.X_OK), f"Agent binary is not executable at {agent_bin}."
    assert os.path.isfile(oracle_bin), f"Oracle binary not found at {oracle_bin}."
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary is not executable at {oracle_bin}."

    inputs = generate_inputs(1000)

    for expr in inputs:
        # Run oracle
        oracle_res = subprocess.run([oracle_bin, expr], capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle failed on input: {expr}. Stderr: {oracle_res.stderr}"

        # Run agent
        agent_res = subprocess.run([agent_bin, expr], capture_output=True, text=True)
        assert agent_res.returncode == 0, f"Agent program failed (exit code {agent_res.returncode}) on input: '{expr}'\nStderr: {agent_res.stderr}"

        oracle_out = oracle_res.stdout.strip()
        agent_out = agent_res.stdout.strip()

        assert agent_out == oracle_out, (
            f"Mismatch on input: '{expr}'\n"
            f"Expected (Oracle) output: '{oracle_out}'\n"
            f"Actual (Agent) output: '{agent_out}'\n"
        )