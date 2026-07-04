# test_final_state.py
import os
import random
import subprocess
import string
import pytest

def test_transcript_content():
    transcript_path = '/home/user/transcript.txt'
    assert os.path.isfile(transcript_path), f"{transcript_path} does not exist."

    with open(transcript_path, 'r') as f:
        content = f.read().strip()

    # Clean up punctuation and lowercase
    cleaned_content = content.lower().translate(str.maketrans('', '', string.punctuation))
    expected = "scientific computing with rust"

    assert cleaned_content == expected, f"Expected transcript to be '{expected}', but got '{cleaned_content}'"

def test_extractor_fuzz_equivalence():
    agent_bin = '/home/user/extractor/target/release/extractor'
    oracle_bin = '/app/oracle_extractor'

    assert os.path.isfile(agent_bin), f"Agent binary {agent_bin} does not exist."
    assert os.access(agent_bin, os.X_OK), f"Agent binary {agent_bin} is not executable."

    assert os.path.isfile(oracle_bin), f"Oracle binary {oracle_bin} does not exist."
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary {oracle_bin} is not executable."

    random.seed(42)
    lengths = [1024, 1152, 1280, 2048, 4096]

    for i in range(100):
        length = random.choice(lengths)
        floats = [random.uniform(-1.0, 1.0) for _ in range(length)]
        input_str = "\n".join(f"{f:.6f}" for f in floats) + "\n"

        agent_proc = subprocess.run(
            [agent_bin],
            input=input_str,
            text=True,
            capture_output=True
        )
        assert agent_proc.returncode == 0, f"Agent binary failed on iteration {i} with stderr: {agent_proc.stderr}"

        oracle_proc = subprocess.run(
            [oracle_bin],
            input=input_str,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle binary failed on iteration {i} with stderr: {oracle_proc.stderr}"

        agent_out = agent_proc.stdout.strip()
        oracle_out = oracle_proc.stdout.strip()

        assert agent_out == oracle_out, (
            f"Output mismatch on iteration {i} (length {length}).\n"
            f"Oracle output:\n{oracle_out}\n"
            f"Agent output:\n{agent_out}\n"
        )