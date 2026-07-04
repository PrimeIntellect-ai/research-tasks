# test_final_state.py

import os
import random
import subprocess
import pytest

def test_transcript():
    transcript_path = "/home/user/transcript.txt"
    assert os.path.isfile(transcript_path), f"Missing transcript file: {transcript_path}"
    with open(transcript_path, "r") as f:
        content = f.read().strip().lower()

    # Remove any punctuation just in case
    import string
    content = content.translate(str.maketrans('', '', string.punctuation))

    expected = "project blackbird activated"
    assert content == expected, f"Transcript content incorrect. Expected '{expected}', got '{content}'"

def test_ci_build_script():
    script_path = "/home/user/ci_build.sh"
    assert os.path.isfile(script_path), f"Missing CI build script: {script_path}"
    assert os.access(script_path, os.X_OK), f"CI build script is not executable: {script_path}"

def test_fuzz_equivalence():
    agent_bin = "/home/user/bin/cleaner"
    oracle_bin = "/app/oracle_cleaner"

    assert os.path.isfile(agent_bin), f"Missing agent executable: {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary is not executable: {agent_bin}"

    assert os.path.isfile(oracle_bin), f"Missing oracle executable: {oracle_bin}"
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary is not executable: {oracle_bin}"

    random.seed(42)

    # We will run 50 iterations to keep the test reasonably fast, 
    # testing various lengths including edge cases.
    lengths = [0, 1, 2, 10, 100, 1024, 1024*1024] + [random.randint(100, 100000) for _ in range(43)]

    for i, length in enumerate(lengths):
        if length == 0:
            input_data = b""
        elif i % 5 == 0:
            input_data = b"\x00" * length
        elif i % 5 == 1:
            input_data = b"\xff" * length
        else:
            input_data = random.randbytes(length)

        agent_proc = subprocess.run([agent_bin], input=input_data, capture_output=True)
        oracle_proc = subprocess.run([oracle_bin], input=input_data, capture_output=True)

        assert agent_proc.returncode == oracle_proc.returncode, \
            f"Return code mismatch on iteration {i} (length {length}). Agent: {agent_proc.returncode}, Oracle: {oracle_proc.returncode}"

        assert agent_proc.stdout == oracle_proc.stdout, \
            f"Output mismatch on iteration {i} (length {length})."