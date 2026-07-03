# test_final_state.py

import os
import random
import subprocess
import pytest

def test_open_scorer_exists_and_executable():
    binary_path = "/home/user/open_scorer"
    assert os.path.exists(binary_path), f"The agent binary {binary_path} does not exist."
    assert os.path.isfile(binary_path), f"The path {binary_path} is not a file."
    assert os.access(binary_path, os.X_OK), f"The file {binary_path} is not executable."

def test_fuzz_equivalence():
    oracle_path = "/app/nanopore_scorer"
    agent_path = "/home/user/open_scorer"

    assert os.path.exists(oracle_path), f"Oracle binary {oracle_path} missing."
    assert os.path.exists(agent_path), f"Agent binary {agent_path} missing."

    random.seed(42)
    num_iterations = 1000

    bases = ['A', 'C', 'G', 'T']

    for i in range(num_iterations):
        n = random.randint(5, 50)
        seq = "".join(random.choice(bases) for _ in range(n))
        signals = [str(round(random.uniform(-2.0, 2.0), 6)) for _ in range(n)]

        args = [seq] + signals

        oracle_cmd = [oracle_path] + args
        agent_cmd = [agent_path] + args

        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

        assert oracle_res.returncode == 0, f"Oracle failed on input: {' '.join(args)}"
        assert agent_res.returncode == 0, f"Agent failed on input: {' '.join(args)}"

        oracle_out = oracle_res.stdout.strip()
        agent_out = agent_res.stdout.strip()

        assert oracle_out == agent_out, (
            f"Mismatch on iteration {i+1}:\n"
            f"Input args: {' '.join(args)}\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output:  {agent_out}"
        )