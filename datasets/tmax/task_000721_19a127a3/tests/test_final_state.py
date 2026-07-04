# test_final_state.py

import os
import subprocess
import random
import pytest

def test_agent_binary_exists():
    agent_path = "/home/user/replicate_gen"
    assert os.path.exists(agent_path), f"Agent binary is missing at {agent_path}"
    assert os.path.isfile(agent_path), f"Agent path {agent_path} is not a file"
    assert os.access(agent_path, os.X_OK), f"Agent binary at {agent_path} is not executable"

def test_agent_source_exists():
    source_path = "/home/user/replicate_gen.c"
    assert os.path.exists(source_path), f"Source file is missing at {source_path}"
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "omp" in content, "Source code does not seem to use OpenMP (missing 'omp')"

def test_fuzz_equivalence():
    oracle_path = "/app/gen_oracle"
    agent_path = "/home/user/replicate_gen"

    random.seed(42)

    # Run a few fuzz testing iterations
    for _ in range(5):
        N = random.randint(50, 500)
        lines = [str(N)]
        for _ in range(N):
            alpha = random.uniform(0.1, 3.0)
            beta = random.uniform(0.1, 3.0)
            gamma = random.uniform(0.1, 3.0)
            delta = random.uniform(0.1, 3.0)
            lines.append(f"{alpha:.6f} {beta:.6f} {gamma:.6f} {delta:.6f}")

        input_data = "\n".join(lines) + "\n"

        oracle_proc = subprocess.run([oracle_path], input=input_data, text=True, capture_output=True)
        assert oracle_proc.returncode == 0, f"Oracle failed with error:\n{oracle_proc.stderr}"

        agent_proc = subprocess.run([agent_path], input=input_data, text=True, capture_output=True)
        assert agent_proc.returncode == 0, f"Agent program failed with error:\n{agent_proc.stderr}"

        oracle_out = oracle_proc.stdout.strip().split('\n')
        agent_out = agent_proc.stdout.strip().split('\n')

        assert len(oracle_out) == len(agent_out), (
            f"Output length mismatch: Oracle produced {len(oracle_out)} lines, "
            f"Agent produced {len(agent_out)} lines."
        )

        for i, (o_line, a_line) in enumerate(zip(oracle_out, agent_out)):
            assert o_line == a_line, (
                f"Mismatch at parameter set {i+1}.\n"
                f"Input parameters: {lines[i+1]}\n"
                f"Expected (Oracle): {o_line}\n"
                f"Actual (Agent): {a_line}"
            )