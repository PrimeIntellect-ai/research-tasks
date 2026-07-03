# test_final_state.py
import os
import json
import random
import subprocess
import pytest

ORACLE_PATH = "/app/oracle_optimizer"
AGENT_PATH = "/home/user/build/optimizer.py"
N_FUZZ = 1000

def generate_random_array(length):
    arr = []
    for _ in range(length):
        if random.random() < 0.05:
            arr.append(0.0)
        else:
            arr.append(random.uniform(-100.0, 100.0))
    return arr

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Agent script missing at {AGENT_PATH}"

    random.seed(42)

    for i in range(N_FUZZ):
        length = random.randint(5, 50)
        weights = generate_random_array(length)
        gradients = generate_random_array(length)

        weights_str = json.dumps(weights)
        gradients_str = json.dumps(gradients)

        # Determine how to invoke the oracle
        if ORACLE_PATH.endswith('.pyc') or ORACLE_PATH.endswith('.py'):
            oracle_cmd = ["python3", ORACLE_PATH]
        else:
            oracle_cmd = [ORACLE_PATH]

        oracle_cmd.extend(["--weights", weights_str, "--gradients", gradients_str])

        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle failed on input {i}: {oracle_res.stderr}"

        agent_cmd = ["python3", AGENT_PATH, "--weights", weights_str, "--gradients", gradients_str]
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

        if agent_res.returncode != 0:
            pytest.fail(f"Agent script failed on input {i}. Stderr: {agent_res.stderr}\nWeights: {weights_str}\nGradients: {gradients_str}")

        oracle_out = oracle_res.stdout.strip()
        agent_out = agent_res.stdout.strip()

        if oracle_out != agent_out:
            try:
                oracle_json = json.loads(oracle_out)
                agent_json = json.loads(agent_out)

                assert len(oracle_json) == len(agent_json), "Output array length mismatch"
                for j, (o_val, a_val) in enumerate(zip(oracle_json, agent_json)):
                    assert abs(o_val - a_val) < 1e-9, f"Value mismatch at index {j}. Oracle: {o_val}, Agent: {a_val}"
            except Exception as e:
                pytest.fail(f"Output mismatch on input {i}.\nWeights: {weights_str}\nGradients: {gradients_str}\nOracle output: {oracle_out}\nAgent output: {agent_out}\nComparison error: {e}")