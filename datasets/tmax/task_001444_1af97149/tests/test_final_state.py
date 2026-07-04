# test_final_state.py

import os
import random
import subprocess
import pytest

def test_evaluator_fuzz_equivalence():
    """
    Fuzz test to ensure the agent's Go binary perfectly matches the oracle's output.
    """
    agent_bin = "/home/user/evaluator"
    oracle_bin = "/app/oracle_evaluator"

    assert os.path.exists(agent_bin), f"Agent binary not found exactly at {agent_bin}"
    assert os.path.isfile(agent_bin), f"Path {agent_bin} is not a file"
    assert os.access(agent_bin, os.X_OK), f"Agent binary at {agent_bin} is not executable"

    assert os.path.exists(oracle_bin), f"Oracle binary not found at {oracle_bin}"
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary at {oracle_bin} is not executable"

    random.seed(42)

    for i in range(100):
        n = random.randint(5, 100)

        preds_list = [f"{random.uniform(-10.0, 10.0):.6f}" for _ in range(n)]
        truths_list = [f"{random.uniform(-10.0, 10.0):.6f}" for _ in range(n)]
        ages_list = [str(random.randint(5, 90)) for _ in range(n)]

        preds = ",".join(preds_list)
        truths = ",".join(truths_list)
        ages = ",".join(ages_list)

        args = [preds, truths, ages]

        agent_proc = subprocess.run([agent_bin] + args, capture_output=True, text=True)
        oracle_proc = subprocess.run([oracle_bin] + args, capture_output=True, text=True)

        assert agent_proc.returncode == 0, f"Agent binary failed on iteration {i} with stderr: {agent_proc.stderr}"
        assert oracle_proc.returncode == 0, f"Oracle binary failed on iteration {i} with stderr: {oracle_proc.stderr}"

        agent_out = agent_proc.stdout.strip()
        oracle_out = oracle_proc.stdout.strip()

        assert agent_out == oracle_out, (
            f"Mismatch on iteration {i}.\n"
            f"Inputs (N={n}):\n"
            f"  preds: {preds[:100]}...\n"
            f"  truths: {truths[:100]}...\n"
            f"  ages: {ages[:100]}...\n"
            f"Expected (Oracle): '{oracle_out}'\n"
            f"Got (Agent): '{agent_out}'"
        )