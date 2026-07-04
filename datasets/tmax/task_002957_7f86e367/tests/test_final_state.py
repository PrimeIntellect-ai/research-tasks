# test_final_state.py
import os
import subprocess
import random
import pytest
import math

def test_mc_worker_fuzz_equivalence():
    oracle_path = "/app/oracle_worker"
    agent_path = "/home/user/workspace/mc_worker"

    assert os.path.isfile(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent binary missing at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary at {agent_path} is not executable"

    random.seed(42)
    N = 100

    for i in range(N):
        k = random.uniform(0.1, 5.0)
        c = random.uniform(0.0, 2.0)
        x0 = random.uniform(-10.0, 10.0)
        y0 = random.uniform(-10.0, 10.0)
        N_mc = random.randint(10, 100)

        args = [str(k), str(c), str(x0), str(y0), str(N_mc)]

        oracle_cmd = [oracle_path] + args
        agent_cmd = [agent_path] + args

        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

        assert oracle_res.returncode == 0, f"Oracle failed on input {args}"
        assert agent_res.returncode == 0, f"Agent failed on input {args}. Error: {agent_res.stderr}"

        oracle_out = oracle_res.stdout.strip().split()
        agent_out = agent_res.stdout.strip().split()

        assert len(oracle_out) == 2, f"Oracle output invalid: {oracle_res.stdout}"
        assert len(agent_out) == 2, f"Agent output invalid: {agent_res.stdout}"

        try:
            o_x, o_y = float(oracle_out[0]), float(oracle_out[1])
            a_x, a_y = float(agent_out[0]), float(agent_out[1])
        except ValueError:
            pytest.fail(f"Could not parse outputs as floats. Oracle: {oracle_out}, Agent: {agent_out}")

        assert math.isclose(o_x, a_x, rel_tol=1e-3, abs_tol=1e-3), \
            f"Mismatch on x for input {args}. Oracle: {o_x}, Agent: {a_x}"
        assert math.isclose(o_y, a_y, rel_tol=1e-3, abs_tol=1e-3), \
            f"Mismatch on y for input {args}. Oracle: {o_y}, Agent: {a_y}"