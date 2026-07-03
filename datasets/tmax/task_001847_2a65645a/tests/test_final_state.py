# test_final_state.py

import os
import random
import string
import subprocess
import glob
import pytest

ORACLE_PATH = "/app/renamer_utility"

def get_agent_executable():
    # Find any executable starting with /home/user/new_renamer
    candidates = glob.glob("/home/user/new_renamer*")
    executables = [c for c in candidates if os.path.isfile(c) and os.access(c, os.X_OK)]
    assert executables, "Could not find any executable matching /home/user/new_renamer*"

    # Prefer exact match if exists
    if "/home/user/new_renamer" in executables:
        return "/home/user/new_renamer"
    return executables[0]

def generate_random_filename(length):
    chars = string.ascii_letters + string.digits + "_-."
    return ''.join(random.choice(chars) for _ in range(length))

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle at {ORACLE_PATH} is not executable"

    agent_path = get_agent_executable()

    random.seed(42)
    # Testing 1000 inputs to ensure it runs within a reasonable time limit
    # while still providing strong fuzzing guarantees.
    N = 1000 

    for _ in range(N):
        length = random.randint(5, 50)
        # Add spaces occasionally since the prompt mentions replacing spaces with underscores
        input_str = generate_random_filename(length)
        if random.random() < 0.2:
            input_str = input_str.replace('_', ' ')

        oracle_proc = subprocess.run(
            [ORACLE_PATH, input_str],
            capture_output=True,
            text=True
        )
        oracle_out = oracle_proc.stdout.strip()

        agent_proc = subprocess.run(
            [agent_path, input_str],
            capture_output=True,
            text=True
        )
        agent_out = agent_proc.stdout.strip()

        assert oracle_proc.returncode == 0, f"Oracle failed on input: {input_str!r}"
        assert agent_proc.returncode == 0, f"Agent failed on input: {input_str!r}. Error: {agent_proc.stderr}"

        assert agent_out == oracle_out, (
            f"Mismatch on input: {input_str!r}\n"
            f"Oracle output: {oracle_out!r}\n"
            f"Agent output:  {agent_out!r}"
        )