# test_final_state.py
import os
import subprocess
import random
import pytest

ORACLE_PATH = "/app/obfuscator_oracle"
AGENT_PATH = "/home/user/replica"
AGENT_SRC = "/home/user/replica.cpp"

def test_agent_files_exist():
    assert os.path.exists(AGENT_SRC), f"Agent source not found at {AGENT_SRC}"
    assert os.path.exists(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"{AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"

    random.seed(42)
    # 1000 iterations is sufficient to find edge cases without timing out the test runner
    num_iterations = 1000 

    for i in range(num_iterations):
        length = random.randint(0, 4096)

        # Generate random bytes
        if length > 0:
            input_data = bytearray(random.getrandbits(8) for _ in range(length))
        else:
            input_data = bytearray()

        # Inject known patterns to trigger specific logic
        if i % 5 == 0:
            pattern = b"TOKEN=secret123"
            insert_pos = random.randint(0, max(0, len(input_data) - len(pattern)))
            input_data[insert_pos:insert_pos] = pattern
        if i % 7 == 0:
            pattern = b"<html><script>alert('XSS')</script></html>"
            insert_pos = random.randint(0, max(0, len(input_data) - len(pattern)))
            input_data[insert_pos:insert_pos] = pattern

        input_bytes = bytes(input_data)

        oracle_proc = subprocess.run([ORACLE_PATH], input=input_bytes, capture_output=True)
        agent_proc = subprocess.run([AGENT_PATH], input=input_bytes, capture_output=True)

        assert agent_proc.returncode == oracle_proc.returncode, (
            f"Return code mismatch on iteration {i} (input length {len(input_bytes)}).\n"
            f"Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}"
        )
        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Stdout mismatch on iteration {i} (input length {len(input_bytes)}).\n"
            f"Input snippet: {input_bytes[:100]!r}\n"
            f"Oracle stdout snippet: {oracle_proc.stdout[:200]!r}\n"
            f"Agent stdout snippet: {agent_proc.stdout[:200]!r}"
        )