# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_asset_counts():
    """
    Validates Phase 1: The asset_counts.txt file should exist and contain 
    the correct comma-separated counts for TCP packets and video frames.
    """
    path = "/home/user/asset_counts.txt"
    assert os.path.exists(path), f"Missing required file: {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    # The setup guarantees exactly 154 TCP packets and 240 frames.
    # Since parsing PCAP and MP4 purely with the Python standard library is 
    # highly complex, we validate against the expected output format.
    expected = "154,240"
    assert content == expected, f"Expected '{expected}' in {path}, but got '{content}'"

def test_fuzz_equivalence():
    """
    Validates Phase 2: Fuzzes the agent's bash script against the reference 
    C binary to ensure bit-for-bit equivalence in output and exit codes.
    """
    oracle_path = "/app/reference_decoder"
    agent_script = "/home/user/decode.sh"

    assert os.path.exists(oracle_path), f"Oracle binary missing at {oracle_path}"
    assert os.path.exists(agent_script), f"Agent script missing at {agent_script}"

    # Fixed seed for reproducible fuzzing
    random.seed(42)

    iterations = 500
    for i in range(iterations):
        # Generate random even-length hex string between 8 and 128 characters
        length = random.choice(range(8, 129, 2))
        hex_str = "".join(random.choices(string.hexdigits.upper(), k=length))

        # Run oracle
        oracle_res = subprocess.run(
            [oracle_path, hex_str], 
            capture_output=True, 
            text=True
        )

        # Run agent script
        agent_res = subprocess.run(
            ["/bin/bash", agent_script, hex_str], 
            capture_output=True, 
            text=True
        )

        # Assert equivalence
        assert oracle_res.returncode == agent_res.returncode, (
            f"Return code mismatch on input '{hex_str}' (Iteration {i+1}/{iterations}).\n"
            f"Oracle exit code: {oracle_res.returncode}\n"
            f"Agent exit code: {agent_res.returncode}"
        )

        assert oracle_res.stdout == agent_res.stdout, (
            f"Standard output mismatch on input '{hex_str}' (Iteration {i+1}/{iterations}).\n"
            f"Oracle stdout:\n{oracle_res.stdout}\n"
            f"Agent stdout:\n{agent_res.stdout}"
        )

        assert oracle_res.stderr == agent_res.stderr, (
            f"Standard error mismatch on input '{hex_str}' (Iteration {i+1}/{iterations}).\n"
            f"Oracle stderr:\n{oracle_res.stderr}\n"
            f"Agent stderr:\n{agent_res.stderr}"
        )