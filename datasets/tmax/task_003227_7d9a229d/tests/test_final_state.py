# test_final_state.py
import os
import subprocess
import random
import pytest

def test_files_exist():
    assert os.path.exists("/home/user/validate.py"), "/home/user/validate.py does not exist"
    assert os.path.exists("/home/user/convergence.png"), "/home/user/convergence.png does not exist"
    assert os.path.exists("/home/user/fast_vol.c"), "/home/user/fast_vol.c does not exist"
    assert os.path.exists("/home/user/fast_vol"), "/home/user/fast_vol does not exist"
    assert os.access("/home/user/fast_vol", os.X_OK), "/home/user/fast_vol is not executable"

def test_fuzz_equivalence():
    oracle = "/app/vol_estimator"
    agent = "/home/user/fast_vol"

    assert os.path.exists(oracle), f"Oracle {oracle} missing"
    assert os.path.exists(agent), f"Agent binary {agent} missing"

    random.seed(42)

    for _ in range(50):
        seed = random.randint(1, 65535)
        n = random.randint(10, 100000)
        r = round(random.uniform(0.1, 20.0), 2)

        args = [str(seed), str(n), f"{r:.2f}"]

        oracle_cmd = [oracle] + args
        agent_cmd = [agent] + args

        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

        assert oracle_res.returncode == 0, f"Oracle failed on args {args}"
        assert agent_res.returncode == 0, f"Agent failed on args {args}"

        assert oracle_res.stdout == agent_res.stdout, (
            f"Output mismatch on args {args}.\n"
            f"Oracle output: {oracle_res.stdout.strip()}\n"
            f"Agent output: {agent_res.stdout.strip()}"
        )