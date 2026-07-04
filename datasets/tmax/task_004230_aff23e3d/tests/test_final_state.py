# test_final_state.py

import os
import subprocess
import random
import string
import tempfile
import pytest

ORACLE_PATH = "/opt/oracle/process_artifacts_oracle.py"
AGENT_PATH = "/home/user/process_artifacts.py"
NUM_TESTS = 1000

def generate_valid_manifest():
    """Generate a validly formatted manifest: 4-byte integer N, followed by N length-prefixed strings."""
    num_entries = random.randint(0, 20)
    # Assuming little-endian as it's typical for C extensions unless specified
    data = bytearray(num_entries.to_bytes(4, byteorder='little'))
    for _ in range(num_entries):
        length = random.randint(1, 50)
        s = ''.join(random.choices(string.ascii_letters + string.digits, k=length)).encode('utf-8')
        data += length.to_bytes(4, byteorder='little') + s
    return bytes(data)

def generate_random_bytes():
    """Generate random bytes to trigger edge cases and test memory safety."""
    length = random.randint(4, 2048)
    return os.urandom(length)

def test_fuzz_equivalence():
    assert os.path.isfile(AGENT_PATH), f"Agent script not found at {AGENT_PATH}"
    assert os.path.isfile(ORACLE_PATH), f"Oracle script not found at {ORACLE_PATH}"

    random.seed(42)

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(NUM_TESTS):
            if random.random() < 0.2:
                data = generate_valid_manifest()
            else:
                data = generate_random_bytes()

            filepath = os.path.join(tmpdir, f"input_{i}.bin")
            with open(filepath, "wb") as f:
                f.write(data)

            # Run oracle
            oracle_cmd = ["python3", ORACLE_PATH, filepath]
            oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)

            # Run agent
            agent_cmd = ["python3", AGENT_PATH, filepath]
            agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

            # If the C extension segfaults, the return code will be negative (e.g. -11 for SIGSEGV)
            # We expect the agent to handle malformed data gracefully (not crash) and match the oracle.
            assert agent_res.returncode == oracle_res.returncode, (
                f"Return code mismatch on input {i} (length {len(data)}).\n"
                f"Oracle exit code: {oracle_res.returncode}\n"
                f"Agent exit code: {agent_res.returncode}\n"
                f"Agent stderr: {agent_res.stderr}\n"
                f"This may indicate a crash (e.g. segmentation fault) due to missing bounds checks."
            )

            assert agent_res.stdout.strip() == oracle_res.stdout.strip(), (
                f"Output mismatch on input {i} (length {len(data)}).\n"
                f"Oracle output: {oracle_res.stdout.strip()}\n"
                f"Agent output: {agent_res.stdout.strip()}\n"
                f"Agent stderr: {agent_res.stderr}"
            )

def test_build_tool_fixtures():
    fixtures_dir = "/tmp/fixtures"
    assert os.path.isdir(fixtures_dir), f"{fixtures_dir} directory was not created. Did you run the Go build tool?"
    assert len(os.listdir(fixtures_dir)) > 0, f"{fixtures_dir} is empty. The Go build tool should generate test fixtures here."