# test_final_state.py

import os
import subprocess
import random
import csv

def test_features_csv_exists_and_format():
    path = "/home/user/features.csv"
    assert os.path.isfile(path), f"Missing {path}"

    with open(path, "r") as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        assert headers is not None, f"File {path} is empty"
        expected_headers = ["word", "start_time_ms", "end_time_ms", "duration_ms", "char_count"]
        # Allow case differences or slight whitespace, but check core structure
        headers_clean = [h.strip().lower() for h in headers]
        assert headers_clean == expected_headers, f"Headers mismatch in {path}. Expected {expected_headers}, got {headers_clean}"

        rows = list(reader)
        assert len(rows) >= 5, f"Expected at least 5 rows of features in {path}, got {len(rows)}"

def test_final_activations_txt():
    path = "/home/user/final_activations.txt"
    assert os.path.isfile(path), f"Missing {path}"
    with open(path, "r") as f:
        content = f.read().strip()

    parts = content.split()
    assert len(parts) == 3, f"Expected exactly 3 space-separated numbers in {path}, got {len(parts)}: {content}"
    for p in parts:
        try:
            float(p)
        except ValueError:
            assert False, f"Value '{p}' in {path} is not a valid float."

def test_fuzz_equivalence_project_features():
    oracle_path = "/app/oracle_projector"
    agent_path = "/home/user/project_features"

    assert os.path.isfile(agent_path), f"Missing compiled binary {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Binary {agent_path} is not executable"

    random.seed(42)
    N = 100

    for i in range(N):
        # Generate 5 random floats in [-100.0, 100.0]
        inputs = [random.uniform(-100.0, 100.0) for _ in range(5)]
        input_str = " ".join(f"{x:.6f}" for x in inputs) + "\n"

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [oracle_path],
                input=input_str,
                text=True,
                capture_output=True,
                timeout=2
            )
            oracle_out = oracle_proc.stdout.strip()
        except Exception as e:
            assert False, f"Failed to run oracle on input '{input_str.strip()}': {e}"

        # Run agent
        try:
            agent_proc = subprocess.run(
                [agent_path],
                input=input_str,
                text=True,
                capture_output=True,
                timeout=2
            )
            agent_out = agent_proc.stdout.strip()
        except Exception as e:
            assert False, f"Failed to run agent binary on input '{input_str.strip()}': {e}"

        assert oracle_out == agent_out, (
            f"Mismatch on fuzz iteration {i+1}/{N}.\n"
            f"Input: {input_str.strip()}\n"
            f"Oracle output: '{oracle_out}'\n"
            f"Agent output:  '{agent_out}'"
        )