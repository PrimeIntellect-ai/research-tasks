# test_final_state.py

import os
import subprocess
import random
import pytest

ORACLE_PATH = "/app/manifest_hash_oracle"
AGENT_PATH = "/home/user/manifest_tool"
WATCHER_PATH = "/home/user/watch_project.sh"

def test_manifest_tool_exists_and_executable():
    assert os.path.exists(AGENT_PATH), f"Agent tool missing at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent tool at {AGENT_PATH} is not executable"

def test_watcher_script_exists():
    assert os.path.exists(WATCHER_PATH), f"Watcher script missing at {WATCHER_PATH}"
    assert os.access(WATCHER_PATH, os.X_OK), f"Watcher script at {WATCHER_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"
    assert os.path.exists(AGENT_PATH), f"Agent tool missing at {AGENT_PATH}"

    random.seed(42)

    for i in range(1000):
        length = random.randint(0, 4096)
        # Generate random bytes (0x00 to 0xFF)
        test_data = bytearray(random.getrandbits(8) for _ in range(length))

        oracle_proc = subprocess.run([ORACLE_PATH], input=test_data, capture_output=True)
        agent_proc = subprocess.run([AGENT_PATH], input=test_data, capture_output=True)

        oracle_out = oracle_proc.stdout.decode('utf-8', errors='replace').strip()
        agent_out = agent_proc.stdout.decode('utf-8', errors='replace').strip()

        assert oracle_proc.returncode == 0, f"Oracle failed on input length {length}"
        assert agent_proc.returncode == 0, f"Agent tool failed on input length {length}"

        assert oracle_out == agent_out, (
            f"Mismatch on iteration {i} with input length {length}.\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output: {agent_out}"
        )