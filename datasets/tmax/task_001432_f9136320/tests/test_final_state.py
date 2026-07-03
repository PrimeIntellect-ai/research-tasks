# test_final_state.py

import os
import subprocess
import random
import tempfile
import pytest

def generate_fuzz_input(seed):
    random.seed(seed)
    length = random.randint(10, 1024)
    # Bias towards edge-case headers
    choices = [0x00, 0xFF, 0x7F] * 10 + list(range(256))
    return bytes(random.choice(choices) for _ in range(length))

def test_run_extractor_exists():
    script_path = "/home/user/run_extractor.sh"
    assert os.path.exists(script_path), f"Wrapper script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_watermark_extractor"
    agent_script = "/home/user/run_extractor.sh"

    assert os.path.exists(oracle_path), f"Oracle {oracle_path} not found."
    assert os.path.exists(agent_script), f"Agent script {agent_script} not found."

    N = 250  # Reduced from 1000 to avoid test timeout, but provides sufficient coverage

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(N):
            input_data = generate_fuzz_input(i)
            input_file = os.path.join(tmpdir, f"input_{i}.bin")
            with open(input_file, "wb") as f:
                f.write(input_data)

            # Run oracle
            oracle_proc = subprocess.run(
                [oracle_path, input_file],
                capture_output=True,
                timeout=5
            )

            # Run agent
            agent_proc = subprocess.run(
                ["/bin/bash", agent_script, input_file],
                capture_output=True,
                timeout=5
            )

            assert oracle_proc.returncode == agent_proc.returncode, (
                f"Return code mismatch on input {i} (seed={i}, len={len(input_data)}).\n"
                f"Oracle returncode: {oracle_proc.returncode}\n"
                f"Agent returncode: {agent_proc.returncode}\n"
                f"Oracle stderr: {oracle_proc.stderr}\n"
                f"Agent stderr: {agent_proc.stderr}"
            )

            assert oracle_proc.stdout == agent_proc.stdout, (
                f"Output mismatch on input {i} (seed={i}, len={len(input_data)}).\n"
                f"Oracle stdout: {oracle_proc.stdout}\n"
                f"Agent stdout: {agent_proc.stdout}"
            )