# test_final_state.py
import os
import random
import subprocess
import pytest

def test_simulator_fuzz_equivalence():
    agent_script = "/home/user/simulator.py"
    oracle_script = "/app/oracle_simulator"

    assert os.path.exists(agent_script), f"Agent script not found at {agent_script}"
    assert os.path.exists(oracle_script), f"Oracle script not found at {oracle_script}"

    random.seed(42)
    N = 100

    for _ in range(N):
        x0 = random.uniform(-20.0, 20.0)
        v0 = random.uniform(-5.0, 5.0)
        steps = random.randint(10, 300)

        args = [
            "--x0", str(x0),
            "--v0", str(v0),
            "--steps", str(steps)
        ]

        oracle_cmd = [oracle_script] + args
        agent_cmd = ["python3", agent_script] + args

        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle failed on args {args}:\n{oracle_res.stderr}"

        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)
        assert agent_res.returncode == 0, f"Agent script failed or crashed on args {args}. Stderr: {agent_res.stderr}"

        oracle_out = oracle_res.stdout.strip()
        agent_out = agent_res.stdout.strip()

        assert oracle_out == agent_out, (
            f"Output mismatch on inputs x0={x0}, v0={v0}, steps={steps}.\n"
            f"Oracle output: '{oracle_out}'\n"
            f"Agent output: '{agent_out}'"
        )