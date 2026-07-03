# test_final_state.py

import os
import random
import subprocess
import pytest

def test_transcript_file():
    transcript_path = "/home/user/transcript.txt"
    assert os.path.exists(transcript_path), f"Transcript file {transcript_path} is missing."
    assert os.path.isfile(transcript_path), f"Path {transcript_path} is not a file."

    with open(transcript_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "AUGGCUAACGGUACCUAA" in content.upper().replace(" ", ""), "The extracted RNA sequence was not found in the transcript file."
    assert "10" in content, "The observation time (10 or 10.0) was not found in the transcript file."

def test_agent_program_exists():
    agent_path = "/home/user/rna_model"
    assert os.path.exists(agent_path), f"Agent program {agent_path} is missing."
    assert os.path.isfile(agent_path), f"Path {agent_path} is not a file."
    assert os.access(agent_path, os.X_OK), f"Agent program {agent_path} is not executable."

def test_fuzz_equivalence():
    oracle_path = "/app/bin/oracle_rna_model"
    agent_path = "/home/user/rna_model"

    assert os.path.exists(oracle_path), f"Oracle program {oracle_path} is missing."
    assert os.access(oracle_path, os.X_OK), f"Oracle program {oracle_path} is not executable."

    random.seed(42)
    bases = ['A', 'C', 'G', 'U']

    for i in range(100):
        seq_length = random.randint(10, 50)
        sequence = "".join(random.choices(bases, k=seq_length))

        try:
            oracle_result = subprocess.run(
                [oracle_path, sequence],
                capture_output=True,
                text=True,
                timeout=5,
                check=True
            )
            oracle_output = oracle_result.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {sequence} with stderr: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input {sequence}")

        try:
            agent_result = subprocess.run(
                [agent_path, sequence],
                capture_output=True,
                text=True,
                timeout=5,
                check=True
            )
            agent_output = agent_result.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent program failed on input {sequence} with stderr: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent program timed out on input {sequence}")

        assert agent_output == oracle_output, (
            f"Output mismatch on sequence: {sequence}\n"
            f"Expected (Oracle): {oracle_output}\n"
            f"Got (Agent): {agent_output}"
        )