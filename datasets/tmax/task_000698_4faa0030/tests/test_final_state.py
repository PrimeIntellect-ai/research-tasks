# test_final_state.py

import os
import random
import string
import subprocess
import tempfile
import pytest

def generate_random_text(length):
    # ASCII letters, digits, punctuation, and whitespace including \n and \r
    chars = string.ascii_letters + string.digits + string.punctuation + ' \t\n\r'
    return ''.join(random.choice(chars) for _ in range(length))

def test_fuzz_equivalence():
    agent_script = "/home/user/run_minidiff.py"
    oracle_script = "/app/oracle/minidiff_oracle.pyc"

    assert os.path.isfile(agent_script), f"Agent script missing: {agent_script}"
    assert os.path.isfile(oracle_script), f"Oracle script missing: {oracle_script}"

    # Use a fixed seed for reproducible fuzzing
    random.seed(42)

    # 100 iterations is a reasonable balance between test robustness and execution time
    # given the overhead of spawning Python subprocesses.
    num_iterations = 100 

    with tempfile.TemporaryDirectory() as tmpdir:
        file1 = os.path.join(tmpdir, "file1.txt")
        file2 = os.path.join(tmpdir, "file2.txt")

        for i in range(num_iterations):
            len1 = random.randint(0, 5000)
            len2 = random.randint(0, 5000)

            text1 = generate_random_text(len1)
            text2 = generate_random_text(len2)

            with open(file1, "wb") as f:
                f.write(text1.encode('utf-8'))
            with open(file2, "wb") as f:
                f.write(text2.encode('utf-8'))

            agent_cmd = ["python3", agent_script, file1, file2]
            oracle_cmd = ["python3", oracle_script, file1, file2]

            agent_proc = subprocess.run(agent_cmd, capture_output=True)
            oracle_proc = subprocess.run(oracle_cmd, capture_output=True)

            assert agent_proc.returncode == oracle_proc.returncode, (
                f"Return code mismatch on iteration {i}.\n"
                f"Agent exit code: {agent_proc.returncode}\n"
                f"Oracle exit code: {oracle_proc.returncode}\n"
                f"Agent stderr: {agent_proc.stderr.decode('utf-8', errors='replace')}"
            )

            if oracle_proc.returncode == 0:
                assert agent_proc.stdout == oracle_proc.stdout, (
                    f"Output mismatch on iteration {i}.\n"
                    f"File 1 length: {len1}, File 2 length: {len2}\n"
                    f"Agent output length: {len(agent_proc.stdout)}\n"
                    f"Oracle output length: {len(oracle_proc.stdout)}"
                )