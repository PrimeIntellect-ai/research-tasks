# test_final_state.py

import os
import random
import subprocess
import string
import pytest

ORACLE_PATH = "/app/oracle_tracker"
AGENT_PATH = "/home/user/tracker"

KEYS = [
    "CACHE_TTL", "MAX_RETRIES", "DB_HOST", "FEATURE_X", 
    "TIMEOUT_MS", "LOG_LEVEL", "MAX_CONNS", "API_KEY", 
    "WORKER_CNT", "MODE"
]

def generate_fuzz_input(num_lines):
    lines = []
    ts = 1600000000
    for _ in range(num_lines):
        ts += random.randint(1, 15)
        key = random.choice(KEYS)
        val_len = random.randint(2, 20)
        val_chars = "".join(random.choices(string.ascii_letters + string.digits, k=val_len))
        hex_val = val_chars.encode('ascii').hex()
        lines.append(f"{ts}\t{key}\t{hex_val}")
    return "\n".join(lines) + "\n"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Agent binary missing at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary not executable at {AGENT_PATH}"

    random.seed(42)

    for i in range(100):
        num_lines = random.randint(50, 5000)
        input_data = generate_fuzz_input(num_lines)

        oracle_proc = subprocess.run(
            [ORACLE_PATH], 
            input=input_data, 
            text=True, 
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i}"

        agent_proc = subprocess.run(
            [AGENT_PATH], 
            input=input_data, 
            text=True, 
            capture_output=True
        )

        if agent_proc.returncode != 0:
            pytest.fail(f"Agent failed with exit code {agent_proc.returncode} on iteration {i}\nStderr: {agent_proc.stderr}")

        if oracle_proc.stdout != agent_proc.stdout:
            oracle_lines = oracle_proc.stdout.splitlines()
            agent_lines = agent_proc.stdout.splitlines()

            diff_msg = []
            for j, (o_line, a_line) in enumerate(zip(oracle_lines, agent_lines)):
                if o_line != a_line:
                    diff_msg.append(f"Line {j+1} mismatch:")
                    diff_msg.append(f"  Expected (Oracle): {o_line}")
                    diff_msg.append(f"  Got (Agent):       {a_line}")
                    break

            if not diff_msg and len(oracle_lines) != len(agent_lines):
                diff_msg.append(f"Line count mismatch: Oracle={len(oracle_lines)}, Agent={len(agent_lines)}")

            pytest.fail(f"Output mismatch on iteration {i}\n" + "\n".join(diff_msg))