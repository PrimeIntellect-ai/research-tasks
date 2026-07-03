# test_final_state.py

import os
import subprocess
import struct
import zlib
import random
import string
import pytest

ORACLE_PATH = "/app/doc-archiver-1.0/darc-extract"
AGENT_PATH = "/home/user/my-darc-extract"
NUM_TESTS = 100

def generate_random_markdown(length):
    lines = []
    current_len = 0
    while current_len < length:
        # Randomly choose line start
        start = random.choices(
            ["H1: ", "H2: ", "Normal text ", "  H1: ", "\n"],
            weights=[10, 10, 70, 5, 5]
        )[0]

        # Random line content
        line_len = random.randint(10, 100)
        content = ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=line_len))

        line = start + content + "\n"
        lines.append(line)
        current_len += len(line)

    return "".join(lines)[:length]

def create_darc_archive(text_content):
    compressed = zlib.compress(text_content.encode('utf-8'))
    header = b"DARC" + struct.pack("<I", len(compressed))
    return header + compressed

@pytest.fixture(scope="session")
def setup_fuzz_inputs():
    random.seed(42)
    inputs = []
    for i in range(NUM_TESTS):
        # Mix of small and a few larger inputs to keep tests reasonably fast
        if i < 5:
            size = random.randint(1_000_000, 5_000_000) # 1MB to 5MB
        else:
            size = random.randint(100, 10_000)

        md_text = generate_random_markdown(size)
        darc_data = create_darc_archive(md_text)
        inputs.append(darc_data)
    return inputs

def test_oracle_exists():
    assert os.path.exists(ORACLE_PATH), f"Oracle program not found at {ORACLE_PATH}. Did you fix the Makefile and run make?"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle program {ORACLE_PATH} is not executable."

def test_agent_program_exists():
    assert os.path.exists(AGENT_PATH), f"Agent program not found at {AGENT_PATH}."
    assert os.access(AGENT_PATH, os.X_OK), f"Agent program {AGENT_PATH} is not executable."

def test_fuzz_equivalence(setup_fuzz_inputs):
    for idx, darc_data in enumerate(setup_fuzz_inputs):
        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [ORACLE_PATH],
                input=darc_data,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=5
            )
            oracle_out = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle program timed out on input {idx}")

        # Run agent
        try:
            agent_proc = subprocess.run(
                [AGENT_PATH],
                input=darc_data,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=5
            )
            agent_out = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent program timed out on input {idx}")

        if oracle_proc.returncode != agent_proc.returncode:
            pytest.fail(f"Return code mismatch on input {idx}: Oracle={oracle_proc.returncode}, Agent={agent_proc.returncode}")

        if oracle_out != agent_out:
            # Truncate output for display if too large
            disp_oracle = oracle_out[:500] + (b"..." if len(oracle_out) > 500 else b"")
            disp_agent = agent_out[:500] + (b"..." if len(agent_out) > 500 else b"")
            pytest.fail(
                f"Output mismatch on input {idx} (size {len(darc_data)} bytes).\n"
                f"Oracle output starts with: {disp_oracle!r}\n"
                f"Agent output starts with: {disp_agent!r}"
            )