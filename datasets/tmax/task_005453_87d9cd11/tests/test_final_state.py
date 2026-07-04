# test_final_state.py
import os
import time
import subprocess
import pytest

AGENT_BIN = "/home/user/router_vm/target/release/router_vm"
REF_BIN = "/app/ref_router_vm"
BYTECODE_FILE = "/tmp/bytecode.bin"
URLS_FILE = "/tmp/urls.txt"

def setup_module(module):
    """Generate the test data before running the tests."""
    with open(BYTECODE_FILE, "w") as f:
        f.write("ROUTE /api/*\nROUTE /user/*\n")
    with open(URLS_FILE, "w") as f:
        for i in range(50000):
            f.write(f"/api/item/{i}\n")

def test_agent_binary_exists():
    """Check if the agent successfully compiled the release binary."""
    assert os.path.isfile(AGENT_BIN), f"Agent binary not found at {AGENT_BIN}. Did you run `cargo build --release`?"
    assert os.access(AGENT_BIN, os.X_OK), f"Agent binary at {AGENT_BIN} is not executable."

def test_execution_time_ratio():
    """Check if the execution time ratio is within the acceptable threshold."""
    assert os.path.isfile(REF_BIN), f"Reference binary missing at {REF_BIN}."

    # Run reference binary
    t0 = time.time()
    ref_result = subprocess.run([REF_BIN, BYTECODE_FILE, URLS_FILE], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    ref_time = time.time() - t0
    assert ref_result.returncode == 0, "Reference binary failed to execute."

    # Run agent binary
    t0 = time.time()
    agent_result = subprocess.run([AGENT_BIN, BYTECODE_FILE, URLS_FILE], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    agent_time = time.time() - t0

    assert agent_result.returncode == 0, f"Agent binary failed to execute. Stderr: {agent_result.stderr.decode()}"

    # Calculate metric
    ratio = agent_time / ref_time

    # Assert threshold
    assert ratio <= 1.5, (
        f"Execution Time Ratio is {ratio:.3f}, which exceeds the threshold of 1.5. "
        f"(Agent Time: {agent_time:.4f}s, Reference Time: {ref_time:.4f}s). "
        "The Rust code is still too slow. Make sure you hoisted the bytecode parsing out of the hot loop."
    )