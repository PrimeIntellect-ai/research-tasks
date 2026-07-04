# test_final_state.py

import os
import random
import subprocess
import pytest

def test_hasher_executable_exists():
    assert os.path.isfile("/home/user/hasher"), "/home/user/hasher does not exist."
    assert os.access("/home/user/hasher", os.X_OK), "/home/user/hasher is not executable."

def test_process_script_exists():
    assert os.path.isfile("/home/user/process.sh"), "/home/user/process.sh does not exist."
    assert os.access("/home/user/process.sh", os.X_OK), "/home/user/process.sh is not executable."

def test_fuzz_equivalence():
    random.seed(42)
    oracle_path = "/app/oracle.sh"
    agent_path = "/home/user/process.sh"

    assert os.path.isfile(oracle_path), f"Oracle {oracle_path} missing."

    for _ in range(20):
        frame_num = random.randint(0, 100)
        url = f"http://localhost/api/frame?number={frame_num}"

        oracle_res = subprocess.run([oracle_path, url], capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle failed on {url}:\n{oracle_res.stderr}"

        agent_res = subprocess.run([agent_path, url], capture_output=True, text=True)
        assert agent_res.returncode == 0, f"Agent script failed on {url}:\n{agent_res.stderr}"

        oracle_out = oracle_res.stdout.strip()
        agent_out = agent_res.stdout.strip()

        assert oracle_out == agent_out, (
            f"Mismatch on input: {url}\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent): {agent_out}"
        )