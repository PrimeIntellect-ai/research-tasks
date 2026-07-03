# test_final_state.py

import os
import subprocess
import random
import pytest

def test_reconstructed_timeline_exists():
    path = "/home/user/reconstructed_timeline.txt"
    assert os.path.isfile(path), f"Reconstructed timeline is missing at {path}"
    with open(path, 'r') as f:
        content = f.read().strip()
    assert len(content) > 0, "Reconstructed timeline is empty"

def test_fixed_script_exists():
    path = "/home/user/fixed_voice_processor.py"
    assert os.path.isfile(path), f"Fixed script is missing at {path}"

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_voice_processor"
    agent_script = "/home/user/fixed_voice_processor.py"

    assert os.path.isfile(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.path.isfile(agent_script), f"Agent script missing at {agent_script}"

    random.seed(42)

    N = 100
    for i in range(N):
        num_ints = random.randint(1, 1000)
        input_data = " ".join(str(random.randint(0, 10000)) for _ in range(num_ints))

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [oracle_path],
                input=input_data,
                text=True,
                capture_output=True,
                timeout=5,
                check=True
            )
            oracle_out = oracle_proc.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail("Oracle timed out")
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed with error: {e.stderr}")

        # Run agent
        try:
            agent_proc = subprocess.run(
                ["python3", agent_script],
                input=input_data,
                text=True,
                capture_output=True,
                timeout=5,
                env={**os.environ, "PROCESSOR_TMP_DIR": "/tmp/voice_processing"}
            )
            agent_out = agent_proc.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on input: {input_data[:50]}...")

        if agent_proc.returncode != 0:
            pytest.fail(f"Agent script failed with return code {agent_proc.returncode}. Stderr: {agent_proc.stderr}")

        assert agent_out == oracle_out, (
            f"Output mismatch on run {i+1}.\n"
            f"Input (first 50 chars): {input_data[:50]}...\n"
            f"Expected (Oracle): {oracle_out[:100]}...\n"
            f"Got (Agent): {agent_out[:100]}..."
        )