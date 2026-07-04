# test_final_state.py

import os
import json
import random
import subprocess
import pytest

def test_notebook_exists():
    path = "/home/user/profile_workflow.ipynb"
    assert os.path.isfile(path), f"Jupyter notebook is missing: {path}"

def test_fast_metric_exists():
    path = "/home/user/fast_metric.py"
    assert os.path.isfile(path), f"Optimized script is missing: {path}"

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_dist"
    agent_script = "/home/user/fast_metric.py"

    assert os.path.isfile(oracle_path), f"Oracle binary missing: {oracle_path}"
    assert os.path.isfile(agent_script), f"Agent script missing: {agent_script}"

    random.seed(42)
    bases = ['A', 'C', 'G', 'T']

    for i in range(100):
        seq_len = random.randint(10, 200)
        sequence = "".join(random.choices(bases, k=seq_len))
        coords = [
            [random.uniform(-100.0, 100.0) for _ in range(3)]
            for _ in range(seq_len)
        ]

        input_data = {
            "sequence": sequence,
            "coords": coords
        }
        input_json = json.dumps(input_data)

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path],
            input=input_json,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i}:\n{oracle_proc.stderr}"
        oracle_out = oracle_proc.stdout.strip()

        # Run agent
        agent_proc = subprocess.run(
            ["python3", agent_script],
            input=input_json,
            text=True,
            capture_output=True
        )
        assert agent_proc.returncode == 0, f"Agent script failed on iteration {i}:\n{agent_proc.stderr}"
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, (
            f"Output mismatch on iteration {i}.\n"
            f"Input JSON length: {len(input_json)}\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output: {agent_out}"
        )