# test_final_state.py
import os
import sys
import json
import random
import subprocess
import pytest

def test_fuzz_equivalence():
    target_script = "/home/user/etl_extractor.py"
    oracle_script = "/app/oracle.py"

    assert os.path.isfile(target_script), f"Target script not found at {target_script}"
    assert os.path.isfile(oracle_script), f"Oracle script not found at {oracle_script}"

    random.seed(42)
    inputs = [f"NODE_{str(i).zfill(3)}" for i in range(1, 101)]
    fuzz_inputs = random.choices(inputs, k=20)

    for node_id in fuzz_inputs:
        # Run oracle
        oracle_cmd = [sys.executable, oracle_script, node_id]
        oracle_proc = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_proc.returncode == 0, f"Oracle failed on input {node_id}:\n{oracle_proc.stderr}"
        oracle_out = oracle_proc.stdout.strip()

        # Run target
        target_cmd = [sys.executable, target_script, node_id]
        target_proc = subprocess.run(target_cmd, capture_output=True, text=True)
        assert target_proc.returncode == 0, f"Target failed on input {node_id}:\n{target_proc.stderr}"
        target_out = target_proc.stdout.strip()

        # Compare outputs
        # Parse as JSON to avoid whitespace differences if possible, or just exact string match.
        try:
            oracle_json = json.loads(oracle_out)
        except json.JSONDecodeError:
            oracle_json = oracle_out

        try:
            target_json = json.loads(target_out)
        except json.JSONDecodeError:
            target_json = target_out

        assert target_json == oracle_json, (
            f"Mismatch on input '{node_id}'.\n"
            f"Oracle output: {oracle_out}\n"
            f"Target output: {target_out}"
        )