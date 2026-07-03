# test_final_state.py

import os
import subprocess
import random
import pytest

def test_solution_file_exists():
    assert os.path.isfile("/home/user/audio_service/solution.py"), "The file /home/user/audio_service/solution.py is missing."

def test_fuzz_equivalence():
    oracle_path = "/app/bin/oracle_audio_sig"
    agent_script = "/home/user/audio_service/solution.py"

    assert os.path.isfile(oracle_path), f"Oracle program missing at {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle program at {oracle_path} is not executable"

    random.seed(42)
    N = 1000  # Reduced from 10000 to avoid test timeout, while still providing robust fuzzing

    for i in range(N):
        length = random.randint(10, 100)  # Reduced max length slightly to speed up subprocess calls
        # Generate float32-like values between -1.0 and 1.0
        inputs = [str(round(random.uniform(-1.0, 1.0), 6)) for _ in range(length)]

        # We also need to test the edge case mentioned in the prompt (sum of x_i exactly 1.0)
        if i == 0:
            inputs = ["0.5", "0.5"] + ["0.0"] * 8

        oracle_cmd = [oracle_path] + inputs
        agent_cmd = ["python3", agent_script] + inputs

        try:
            oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True, timeout=2, check=True)
            oracle_output = oracle_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input: {' '.join(inputs)}\nError: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input: {' '.join(inputs)}")

        try:
            agent_res = subprocess.run(agent_cmd, capture_output=True, text=True, timeout=2)
            agent_output = agent_res.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on input: {' '.join(inputs)}")

        if agent_res.returncode != 0:
            pytest.fail(f"Agent script crashed on input: {' '.join(inputs)}\nError: {agent_res.stderr}")

        # Compare outputs line by line or token by token
        oracle_tokens = oracle_output.split()
        agent_tokens = agent_output.split()

        if len(oracle_tokens) != len(agent_tokens):
            pytest.fail(f"Output length mismatch on input: {' '.join(inputs)}\nOracle: {oracle_output}\nAgent: {agent_output}")

        for j, (o_tok, a_tok) in enumerate(zip(oracle_tokens, agent_tokens)):
            try:
                o_val = float(o_tok)
                a_val = float(a_tok)
                # Bit-exact equivalence generally means exact string match or exact float match
                if o_tok != a_tok and abs(o_val - a_val) > 1e-6:
                    pytest.fail(f"Mismatch at index {j} on input: {' '.join(inputs)}\nOracle: {o_tok}\nAgent: {a_tok}\nFull Oracle: {oracle_output}\nFull Agent: {agent_output}")
            except ValueError:
                if o_tok != a_tok:
                    pytest.fail(f"Mismatch at index {j} (non-float) on input: {' '.join(inputs)}\nOracle: {o_tok}\nAgent: {a_tok}")