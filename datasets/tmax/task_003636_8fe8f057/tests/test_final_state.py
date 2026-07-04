# test_final_state.py

import os
import random
import subprocess
import pytest

def test_fuzz_equivalence():
    oracle_path = "/app/legacy_calc"
    agent_script = "/home/user/calc_metrics.py"

    assert os.path.isfile(oracle_path), f"Oracle missing: {oracle_path}"
    assert os.path.isfile(agent_script), f"Agent script missing: {agent_script}"

    # Use a fixed seed for reproducible fuzzing
    random.seed(42)

    iterations = 1000
    for i in range(iterations):
        L = random.randint(10, 1000)
        # Generate floats in [1000000.0, 1000010.0] to trigger catastrophic cancellation in naive algorithms
        inputs = [random.uniform(1000000.0, 1000010.0) for _ in range(L)]
        input_str = "\n".join(str(x) for x in inputs) + "\n"

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [oracle_path],
                input=input_str,
                text=True,
                capture_output=True,
                check=True
            )
            oracle_out = oracle_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on iteration {i}:\n{e.stderr}")

        # Run agent
        agent_proc = subprocess.run(
            ["python3", agent_script],
            input=input_str,
            text=True,
            capture_output=True
        )

        assert agent_proc.returncode == 0, (
            f"Agent script failed on iteration {i}.\n"
            f"Stderr:\n{agent_proc.stderr}"
        )
        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on iteration {i} (Length of input={L}).\n"
                f"Input preview: {inputs[:5]}...\n\n"
                f"Expected Oracle Output:\n{oracle_out}\n"
                f"Actual Agent Output:\n{agent_out}\n"
            )