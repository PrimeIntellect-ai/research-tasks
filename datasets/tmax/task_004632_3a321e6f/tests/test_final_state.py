# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_craft_payload_exists_and_executable():
    script_path = "/home/user/craft_payload.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_fuzz_equivalence():
    oracle_path = "/app/waf_evasion_encoder"
    agent_script = "/home/user/craft_payload.sh"

    assert os.path.isfile(oracle_path), f"Oracle binary {oracle_path} is missing."

    # Set a fixed seed for reproducible fuzzing
    random.seed(42)

    # Use printable ASCII characters (excluding newlines/tabs to avoid shell argument passing edge cases not related to the core logic)
    charset = string.ascii_letters + string.digits + string.punctuation + " "

    for i in range(100):
        length = random.randint(1, 200)
        payload = "".join(random.choice(charset) for _ in range(length))

        # Run oracle
        oracle_res = subprocess.run([oracle_path, payload], capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle failed unexpectedly on input: {payload!r}"

        # Run agent script
        agent_res = subprocess.run(["bash", agent_script, payload], capture_output=True, text=True)

        assert agent_res.returncode == 0, f"Agent script failed on input: {payload!r}\nStderr: {agent_res.stderr}"

        oracle_out = oracle_res.stdout.strip()
        agent_out = agent_res.stdout.strip()

        assert oracle_out == agent_out, (
            f"Mismatch on iteration {i+1} with input: {payload!r}\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent):       {agent_out}"
        )