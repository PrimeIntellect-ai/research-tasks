# test_final_state.py

import os
import subprocess
import random
import pytest

def test_student_executable_exists():
    exe_file = "/home/user/spatial_transformer_recreated"
    assert os.path.exists(exe_file), f"The expected executable {exe_file} does not exist."
    assert os.path.isfile(exe_file), f"{exe_file} is not a file."
    assert os.access(exe_file, os.X_OK), f"{exe_file} is not executable."

def test_fuzz_equivalence():
    oracle_exe = "/app/spatial_transformer"
    agent_exe = "/home/user/spatial_transformer_recreated"

    assert os.path.exists(oracle_exe), f"Oracle executable {oracle_exe} missing."
    assert os.path.exists(agent_exe), f"Agent executable {agent_exe} missing."

    random.seed(42)
    num_tests = 100

    for i in range(num_tests):
        # Generate random inputs
        id_val = random.randint(1, 1000)
        x = random.uniform(-10.0, 10.0)
        y = random.uniform(-10.0, 10.0)
        z = random.uniform(-10.0, 10.0)

        input_str = f"{id_val},{x:.6f},{y:.6f},{z:.6f}\n"

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_exe],
            input=input_str,
            text=True,
            capture_output=True,
            check=False
        )
        oracle_out = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            [agent_exe],
            input=input_str,
            text=True,
            capture_output=True,
            check=False
        )
        agent_out = agent_proc.stdout

        assert agent_proc.returncode == oracle_proc.returncode, \
            f"Return codes differ for input '{input_str.strip()}'. Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}"

        assert agent_out == oracle_out, \
            f"Output mismatch for input '{input_str.strip()}'.\nExpected (Oracle): {oracle_out}\nGot (Agent): {agent_out}"