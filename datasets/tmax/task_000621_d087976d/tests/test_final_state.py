# test_final_state.py

import os
import random
import subprocess

def test_default_params():
    """Verify the extracted audio parameters are saved correctly."""
    path = "/home/user/default_params.txt"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().lower()
    assert "2.5" in content, "f0 value 2.5 not found in default_params.txt"
    assert "0.15" in content, "damping value 0.15 not found in default_params.txt"

def test_fuzz_equivalence():
    """Fuzz equivalence test against the oracle binary."""
    oracle_path = "/app/oracle_bin"
    agent_path = "/home/user/data_gen/target/release/data_gen"

    assert os.path.exists(oracle_path), f"Oracle binary {oracle_path} not found."
    assert os.path.exists(agent_path), f"Agent binary {agent_path} not found. Did you compile with --release?"
    assert os.access(agent_path, os.X_OK), f"Agent binary {agent_path} is not executable."

    random.seed(42)

    for _ in range(100):
        N = random.randint(10, 100)
        f0 = random.uniform(1.0, 10.0)
        damping = random.uniform(0.01, 0.5)
        steps = random.randint(10, 100)

        args = [str(N), f"{f0:.6f}", f"{damping:.6f}", str(steps)]

        oracle_cmd = [oracle_path] + args
        agent_cmd = [agent_path] + args

        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

        assert oracle_res.returncode == 0, f"Oracle failed on input {args}"
        assert agent_res.returncode == 0, f"Agent program failed on input {args}.\nStderr: {agent_res.stderr}"

        oracle_out = oracle_res.stdout.strip()
        agent_out = agent_res.stdout.strip()

        assert oracle_out == agent_out, (
            f"Mismatch on input: N={N}, f0={f0:.6f}, damping={damping:.6f}, steps={steps}\n"
            f"Oracle output:\n{oracle_out}\n"
            f"Agent output:\n{agent_out}"
        )