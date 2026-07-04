# test_final_state.py

import os
import subprocess
import random
import pytest

def test_frame_count():
    """Verify that the frame count file exists and contains the correct number of frames."""
    path = "/home/user/frame_count.txt"
    assert os.path.isfile(path), f"File {path} does not exist. Did you write the frame count?"

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "90", f"Expected frame count to be 90, but got '{content}'."

def test_solve_system_executable():
    """Verify that the compiled executable exists and is executable."""
    path = "/home/user/solve_system"
    assert os.path.isfile(path), f"Executable {path} does not exist. Did you compile your C program?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_fuzz_solve_system():
    """Fuzz the agent's C program against the oracle to ensure bit-exact equivalence."""
    oracle_path = "/app/oracle_solve"
    agent_path = "/home/user/solve_system"

    assert os.path.isfile(oracle_path), f"Oracle executable missing at {oracle_path}."
    assert os.path.isfile(agent_path), f"Agent executable missing at {agent_path}."

    random.seed(42)
    num_iterations = 1000

    for _ in range(num_iterations):
        # Generate 7 random floats between -10.0 and 10.0
        inputs = [random.uniform(-10.0, 10.0) for _ in range(7)]
        input_str = " ".join(f"{x:.6f}" for x in inputs) + "\n"

        oracle_proc = subprocess.run(
            [oracle_path], 
            input=input_str, 
            text=True, 
            capture_output=True
        )
        agent_proc = subprocess.run(
            [agent_path], 
            input=input_str, 
            text=True, 
            capture_output=True
        )

        assert oracle_proc.returncode == 0, f"Oracle failed on input: {input_str.strip()}"
        assert agent_proc.returncode == 0, f"Agent program failed (non-zero exit code) on input: {input_str.strip()}"

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, (
            f"Output mismatch on input: {input_str.strip()}\n"
            f"Expected (Oracle): '{oracle_out}'\n"
            f"Got (Agent): '{agent_out}'"
        )