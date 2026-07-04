# test_final_state.py
import os
import random
import subprocess
import pytest

def test_finder_executable_exists():
    target = "/home/user/finder"
    assert os.path.isfile(target), f"Agent target {target} does not exist."
    assert os.access(target, os.X_OK), f"Agent target {target} is not executable."

def test_fuzz_equivalence():
    oracle = "/app/oracle_finder"
    target = "/home/user/finder"

    assert os.path.isfile(oracle), f"Oracle {oracle} does not exist."
    assert os.access(oracle, os.X_OK), f"Oracle {oracle} is not executable."

    random.seed(42)

    for i in range(100):
        frame_index = random.randint(0, 299)
        q1 = random.randint(0, 10000000)
        q2 = random.randint(0, 10000000)
        q3 = random.randint(0, 10000000)
        query_vector = f"{q1},{q2},{q3}"

        args = [str(frame_index), query_vector]

        # Run oracle
        oracle_cmd = [oracle] + args
        oracle_proc = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_proc.returncode == 0, f"Oracle failed on input {args} with error: {oracle_proc.stderr}"
        oracle_out = oracle_proc.stdout.strip()

        # Run target
        target_cmd = [target] + args
        target_proc = subprocess.run(target_cmd, capture_output=True, text=True)
        assert target_proc.returncode == 0, f"Target failed on input {args} with error: {target_proc.stderr}"
        target_out = target_proc.stdout.strip()

        assert oracle_out == target_out, (
            f"Mismatch on iteration {i+1}:\n"
            f"Input arguments: frame_index={frame_index}, query_vector='{query_vector}'\n"
            f"Oracle output: '{oracle_out}'\n"
            f"Target output: '{target_out}'"
        )