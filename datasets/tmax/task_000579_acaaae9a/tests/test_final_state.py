# test_final_state.py
import os
import subprocess
import struct
import random
import string
import tempfile
import pytest

AGENT_BINARY = "/home/user/log_converter"
ORACLE_BINARY = "/app/oracle/log_converter_oracle"
NUM_FUZZ_ITERATIONS = 1000

def generate_random_log_entry():
    timestamp = random.randint(0, 0xFFFFFFFF)
    level = random.randint(0, 3)
    msg_len = random.randint(0, 63)
    msg = ''.join(random.choices(string.ascii_letters + string.digits, k=msg_len)).encode('utf-8')
    msg = msg.ljust(64, b'\0')
    return struct.pack("<IB64s", timestamp, level, msg)

def test_agent_binary_exists():
    assert os.path.isfile(AGENT_BINARY), f"Agent binary {AGENT_BINARY} does not exist."
    assert os.access(AGENT_BINARY, os.X_OK), f"Agent binary {AGENT_BINARY} is not executable."

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_BINARY), f"Oracle binary {ORACLE_BINARY} does not exist."

    random.seed(42)

    # Set LD_LIBRARY_PATH so the agent binary can find libcjson.so if it's dynamically linked
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = "/app/vendor/cJSON:" + env.get("LD_LIBRARY_PATH", "")

    for i in range(NUM_FUZZ_ITERATIONS):
        num_entries = random.randint(1, 100)
        file_content = b"".join(generate_random_log_entry() for _ in range(num_entries))

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file_content)
            tmp_path = tmp.name

        try:
            oracle_proc = subprocess.run(
                [ORACLE_BINARY, tmp_path],
                capture_output=True,
                env=env,
                text=True
            )

            agent_proc = subprocess.run(
                [AGENT_BINARY, tmp_path],
                capture_output=True,
                env=env,
                text=True
            )

            assert agent_proc.returncode == oracle_proc.returncode, (
                f"Return code mismatch on iteration {i}. "
                f"Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}\n"
                f"Oracle stderr: {oracle_proc.stderr}\n"
                f"Agent stderr: {agent_proc.stderr}"
            )

            assert agent_proc.stdout == oracle_proc.stdout, (
                f"Output mismatch on iteration {i}.\n"
                f"Oracle stdout: {oracle_proc.stdout}\n"
                f"Agent stdout: {agent_proc.stdout}"
            )

        finally:
            os.remove(tmp_path)