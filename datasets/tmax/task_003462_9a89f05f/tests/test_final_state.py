# test_final_state.py
import os
import subprocess
import random
import pytest

def test_scorer_go_exists():
    assert os.path.exists("/home/user/scorer.go"), "/home/user/scorer.go does not exist"
    assert os.path.isfile("/home/user/scorer.go"), "/home/user/scorer.go is not a file"

def test_fuzz_equivalence():
    oracle_path = "/app/divergence_scorer"
    agent_cmd = ["go", "run", "/home/user/scorer.go"]

    assert os.path.exists(oracle_path), f"Oracle missing at {oracle_path}"

    random.seed(42)
    iterations = 1000
    min_length = 2
    max_length = 50
    min_val = 0.0
    max_val = 100.0

    for i in range(iterations):
        length = random.randint(min_length, max_length)
        floats = [random.uniform(min_val, max_val) for _ in range(length)]
        input_data = " ".join(f"{v:.6f}" for v in floats).encode("utf-8")

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path],
            input=input_data,
            capture_output=True,
            check=True
        )
        oracle_out = oracle_proc.stdout.decode("utf-8").strip()

        # Run agent
        agent_proc = subprocess.run(
            agent_cmd,
            input=input_data,
            capture_output=True
        )

        assert agent_proc.returncode == 0, f"Agent program failed on input: {input_data.decode('utf-8')}\nStderr: {agent_proc.stderr.decode('utf-8')}"
        agent_out = agent_proc.stdout.decode("utf-8").strip()

        assert agent_out == oracle_out, (
            f"Output mismatch on iteration {i}.\n"
            f"Input: {input_data.decode('utf-8')}\n"
            f"Oracle: {oracle_out}\n"
            f"Agent:  {agent_out}"
        )