# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_token_gen_sh_exists_and_executable():
    agent_script = "/home/user/token_gen.sh"
    assert os.path.exists(agent_script), f"Agent script {agent_script} does not exist."
    assert os.path.isfile(agent_script), f"Agent script {agent_script} is not a file."
    assert os.access(agent_script, os.X_OK), f"Agent script {agent_script} is not executable."

def test_fuzz_equivalence():
    oracle_bin = "/app/auth_module"
    agent_script = "/home/user/token_gen.sh"

    assert os.path.exists(oracle_bin), f"Oracle binary {oracle_bin} missing."
    assert os.path.exists(agent_script), f"Agent script {agent_script} missing."

    random.seed(42)
    charset = string.ascii_letters + string.digits

    for _ in range(100):
        length = random.randint(5, 20)
        fuzz_input = ''.join(random.choice(charset) for _ in range(length))

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_bin, fuzz_input],
            capture_output=True,
            text=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input: {fuzz_input}"
        oracle_output = oracle_proc.stdout.strip()

        # Run agent
        agent_proc = subprocess.run(
            [agent_script, fuzz_input],
            capture_output=True,
            text=True
        )
        assert agent_proc.returncode == 0, f"Agent script failed on input: {fuzz_input}"
        agent_output = agent_proc.stdout.strip()

        assert oracle_output == agent_output, (
            f"Mismatch on input '{fuzz_input}'.\n"
            f"Oracle output: {oracle_output}\n"
            f"Agent output:  {agent_output}"
        )