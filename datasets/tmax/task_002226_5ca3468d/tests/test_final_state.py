# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_agent_executable_exists():
    agent_bin = "/home/user/sign"
    assert os.path.exists(agent_bin), f"Agent executable not found at {agent_bin}"
    assert os.path.isfile(agent_bin), f"{agent_bin} is not a file"
    assert os.access(agent_bin, os.X_OK), f"Agent executable {agent_bin} is not executable"

def test_fuzz_equivalence():
    oracle_bin = "/app/oracle_signer"
    agent_bin = "/home/user/sign"

    assert os.path.exists(oracle_bin), f"Oracle binary not found at {oracle_bin}"
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary {oracle_bin} is not executable"

    random.seed(42)
    chars = string.ascii_letters + string.digits

    for i in range(100):
        length = random.randint(10, 100)
        payload = "".join(random.choices(chars, k=length))

        try:
            oracle_proc = subprocess.run(
                [oracle_bin, payload],
                capture_output=True,
                text=True,
                check=True,
                timeout=2
            )
            oracle_output = oracle_proc.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input '{payload}': {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input '{payload}'")

        try:
            agent_proc = subprocess.run(
                [agent_bin, payload],
                capture_output=True,
                text=True,
                check=True,
                timeout=2
            )
            agent_output = agent_proc.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent program failed on input '{payload}': {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent program timed out on input '{payload}'")

        assert agent_output == oracle_output, (
            f"Output mismatch on input '{payload}'.\n"
            f"Expected (Oracle): {oracle_output}\n"
            f"Got (Agent): {agent_output}"
        )