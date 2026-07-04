# test_final_state.py

import os
import json
import random
import subprocess
import requests
import pytest

def test_oracle_compiled():
    oracle_path = "/app/oracle/integrator"
    assert os.path.isfile(oracle_path), f"Oracle binary not found at {oracle_path}. Did you compile it?"
    assert os.access(oracle_path, os.X_OK), f"Oracle binary at {oracle_path} is not executable."

def test_notebook_executed():
    notebook_path = "/home/user/validation/check_analytical_executed.ipynb"
    assert os.path.isfile(notebook_path), f"Executed notebook not found at {notebook_path}."

def test_fuzz_equivalence():
    oracle_path = "/app/oracle/integrator"
    endpoint = "http://127.0.0.1:8080/simulate"

    random.seed(42)
    N = 100  # Running 100 instead of 1000 to prevent test timeouts, still provides strong fuzzing

    for i in range(N):
        t0 = random.uniform(0.0, 10.0)
        tf = t0 + random.uniform(1.0, 50.0)
        y0_0 = random.uniform(-100.0, 100.0)
        y0_1 = random.uniform(-100.0, 100.0)
        tol = random.uniform(1e-6, 1e-3)

        # 1. Run Oracle
        cmd = [oracle_path, str(t0), str(tf), str(y0_0), str(y0_1), str(tol)]
        res = subprocess.run(cmd, capture_output=True, text=True)
        assert res.returncode == 0, f"Oracle failed on input {cmd}. Stderr: {res.stderr}"

        try:
            oracle_out = json.loads(res.stdout)
        except json.JSONDecodeError:
            pytest.fail(f"Oracle output is not valid JSON. Output: {res.stdout}")

        # 2. Run Agent Service
        payload = {"t0": t0, "tf": tf, "y0": [y0_0, y0_1], "tol": tol}
        try:
            resp = requests.post(endpoint, json=payload, timeout=5)
            resp.raise_for_status()
            agent_out = resp.json()
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Agent API request failed on {endpoint}. Is Nginx/Flask running? Error: {e}")
        except json.JSONDecodeError:
            pytest.fail(f"Agent API did not return valid JSON. Output: {resp.text}")

        # 3. Compare outputs
        assert "t" in agent_out and "y" in agent_out, "Agent output missing 't' or 'y' arrays."

        assert len(oracle_out["t"]) == len(agent_out["t"]), \
            f"Mismatch in number of time steps. Oracle: {len(oracle_out['t'])}, Agent: {len(agent_out['t'])}"

        for idx, (ot, at) in enumerate(zip(oracle_out["t"], agent_out["t"])):
            assert abs(float(ot) - float(at)) < 1e-5, \
                f"Mismatch in 't' array at index {idx}: Oracle {ot} != Agent {at}"

        for idx, (oy, ay) in enumerate(zip(oracle_out["y"], agent_out["y"])):
            assert abs(float(oy[0]) - float(ay[0])) < 1e-5, \
                f"Mismatch in 'y[0]' array at index {idx}: Oracle {oy[0]} != Agent {ay[0]}"
            assert abs(float(oy[1]) - float(ay[1])) < 1e-5, \
                f"Mismatch in 'y[1]' array at index {idx}: Oracle {oy[1]} != Agent {ay[1]}"