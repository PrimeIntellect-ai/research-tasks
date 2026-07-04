# test_final_state.py

import os
import subprocess
import random
import string
import json
import pytest

def test_auto_restore_script_exists():
    agent_path = "/home/user/auto_restore.py"
    assert os.path.isfile(agent_path), f"Agent script missing at {agent_path}. Did you create it?"

def test_fuzz_equivalence():
    oracle_path = "/opt/oracle/auto_restore_oracle.py"
    agent_path = "/home/user/auto_restore.py"

    assert os.path.isfile(oracle_path), f"Oracle script missing at {oracle_path}"

    # Set up fixed seed for reproducibility
    random.seed(42)
    chars = string.ascii_letters + string.digits

    for i in range(100):
        length = random.randint(8, 16)
        fuzz_input = ''.join(random.choice(chars) for _ in range(length))

        oracle_cmd = ["/usr/bin/python3", oracle_path, fuzz_input]
        agent_cmd = ["/usr/bin/python3", agent_path, fuzz_input]

        oracle_proc = subprocess.run(oracle_cmd, capture_output=True, text=True)
        agent_proc = subprocess.run(agent_cmd, capture_output=True, text=True)

        assert agent_proc.returncode == oracle_proc.returncode, (
            f"Return code mismatch on input '{fuzz_input}': "
            f"expected {oracle_proc.returncode}, got {agent_proc.returncode}.\n"
            f"Agent stderr: {agent_proc.stderr}"
        )

        # Try to parse as JSON for a cleaner comparison, fallback to raw string
        try:
            oracle_out = json.loads(oracle_proc.stdout)
        except json.JSONDecodeError:
            oracle_out = oracle_proc.stdout.strip()

        try:
            agent_out = json.loads(agent_proc.stdout)
        except json.JSONDecodeError:
            agent_out = agent_proc.stdout.strip()

        assert agent_out == oracle_out, (
            f"Output mismatch on input '{fuzz_input}'.\n"
            f"Expected:\n{oracle_out}\n"
            f"Got:\n{agent_out}\n"
            f"Agent stderr:\n{agent_proc.stderr}"
        )