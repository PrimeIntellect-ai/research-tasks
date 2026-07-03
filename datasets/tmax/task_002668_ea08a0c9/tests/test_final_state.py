# test_final_state.py
import os
import subprocess
import random

def test_ode_sim_fuzz_equivalence():
    agent_bin = "/home/user/ode_sim"
    oracle_bin = "/opt/verifier/oracle_sim"

    assert os.path.exists(agent_bin), f"Agent binary not found at {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary {agent_bin} is not executable"

    assert os.path.exists(oracle_bin), f"Oracle binary not found at {oracle_bin}"
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary {oracle_bin} is not executable"

    random.seed(42)
    N = 1000

    for i in range(N):
        x0 = random.uniform(-10.0, 10.0)
        y0 = random.uniform(-10.0, 10.0)
        input_str = f"{x0:.6f} {y0:.6f}\n"

        # Run oracle
        try:
            oracle_res = subprocess.run(
                [oracle_bin],
                input=input_str,
                text=True,
                capture_output=True,
                check=True,
                timeout=1
            )
            oracle_out = oracle_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            assert False, f"Oracle crashed on input '{input_str.strip()}': {e.stderr}"

        # Run agent
        try:
            agent_res = subprocess.run(
                [agent_bin],
                input=input_str,
                text=True,
                capture_output=True,
                check=True,
                timeout=1
            )
            agent_out = agent_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            assert False, f"Agent program crashed on input '{input_str.strip()}': {e.stderr}"
        except subprocess.TimeoutExpired:
            assert False, f"Agent program timed out on input '{input_str.strip()}'"

        assert agent_out == oracle_out, (
            f"Mismatch on input '{input_str.strip()}'.\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent): {agent_out}"
        )