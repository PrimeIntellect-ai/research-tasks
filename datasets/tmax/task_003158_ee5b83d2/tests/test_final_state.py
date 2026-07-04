# test_final_state.py

import os
import subprocess
import random
import pytest

def test_pipeline_binary_exists():
    agent_path = "/home/user/pipeline"
    assert os.path.isfile(agent_path), f"Compiled binary {agent_path} does not exist. Did you compile your C++ program?"
    assert os.access(agent_path, os.X_OK), f"Binary {agent_path} is not executable."

def test_fuzz_equivalence():
    oracle_path = "/opt/oracle/pipeline_ref"
    agent_path = "/home/user/pipeline"

    assert os.path.isfile(oracle_path), f"Oracle missing at {oracle_path}"

    random.seed(42)

    for i in range(100):
        # Generate random input based on the distribution described
        lines = []
        num_lines = random.randint(10, 1000)
        for _ in range(num_lines):
            id_val = random.randint(1, 100000)
            ts_val = random.randint(1600000000, 1700000000)
            size_val = str(random.randint(100, 10000)) if random.random() > 0.1 else ""
            metric_val = f"{random.uniform(0.0, 100.0):.4f}" if random.random() > 0.1 else ""
            # The prompt format is "ID (int), Timestamp (int), Size (int/empty), Metric (float/empty)"
            lines.append(f"{id_val},{ts_val},{size_val},{metric_val}")

        input_data = "\n".join(lines) + "\n"

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [oracle_path],
                input=input_data,
                text=True,
                capture_output=True,
                timeout=5
            )
            oracle_out = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input iteration {i}")

        # Run agent
        try:
            agent_proc = subprocess.run(
                [agent_path],
                input=input_data,
                text=True,
                capture_output=True,
                timeout=5
            )
            agent_out = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent program timed out on input iteration {i}")

        assert agent_proc.returncode == oracle_proc.returncode, (
            f"Return code mismatch on iteration {i}.\n"
            f"Oracle return code: {oracle_proc.returncode}\n"
            f"Agent return code: {agent_proc.returncode}\n"
            f"Input snippet:\n{input_data[:200]}..."
        )

        if agent_out != oracle_out:
            pytest.fail(
                f"Output mismatch on iteration {i}.\n"
                f"Input snippet:\n{input_data[:200]}...\n\n"
                f"Oracle output snippet:\n{oracle_out[:500]}\n\n"
                f"Agent output snippet:\n{agent_out[:500]}"
            )