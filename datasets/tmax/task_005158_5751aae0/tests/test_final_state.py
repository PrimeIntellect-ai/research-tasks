# test_final_state.py
import os
import subprocess
import random

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_simulator"
    agent_path = "/home/user/simulator"

    assert os.path.isfile(oracle_path), f"Oracle program not found at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent program not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent program at {agent_path} is not executable"

    random.seed(42)
    num_iterations = 1000

    for i in range(num_iterations):
        seed_arg = str(random.randint(0, 10000))
        num_obs = random.randint(10, 100)
        observations = [f"{random.uniform(-100.0, 100.0):.6f}" for _ in range(num_obs)]

        args = [seed_arg] + observations

        try:
            oracle_result = subprocess.run(
                [oracle_path] + args,
                capture_output=True,
                text=True,
                check=True,
                timeout=2
            )
            oracle_out = oracle_result.stdout.strip()
        except subprocess.CalledProcessError as e:
            assert False, f"Oracle failed on iteration {i} with args {args[:5]}... Error: {e.stderr}"
        except subprocess.TimeoutExpired:
            assert False, f"Oracle timed out on iteration {i}"

        try:
            agent_result = subprocess.run(
                [agent_path] + args,
                capture_output=True,
                text=True,
                check=True,
                timeout=2
            )
            agent_out = agent_result.stdout.strip()
        except subprocess.CalledProcessError as e:
            assert False, f"Agent program failed on iteration {i} with args {args[:5]}...\nStderr: {e.stderr}"
        except subprocess.TimeoutExpired:
            assert False, f"Agent program timed out on iteration {i}"

        assert agent_out == oracle_out, (
            f"Mismatch on iteration {i}.\n"
            f"Input args (first 5): {args[:5]}...\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent):       {agent_out}"
        )