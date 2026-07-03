# test_final_state.py

import os
import subprocess
import random
import string
import pytest

def test_ci_test_script():
    ci_script = "/home/user/ci_test.sh"
    assert os.path.exists(ci_script), f"Missing CI script: {ci_script}"
    assert os.path.isfile(ci_script), f"Not a file: {ci_script}"
    assert os.access(ci_script, os.X_OK), f"CI script is not executable: {ci_script}"

    result = subprocess.run([ci_script], capture_output=True)
    assert result.returncode == 0, f"CI script failed with exit code {result.returncode}. Stderr: {result.stderr.decode(errors='replace')}"

def generate_fuzz_input(length):
    choices = []
    # 70% printable ASCII
    printable = string.printable.encode('ascii')
    # Patterns to inject
    patterns = [b"%", b"%A", b"%1B", b"<script>", b"<<script>script>"]

    out = bytearray()
    while len(out) < length:
        r = random.random()
        if r < 0.7:
            out.append(random.choice(printable))
        elif r < 0.85:
            out.append(random.randint(0, 255))
        else:
            pat = random.choice(patterns)
            out.extend(pat)
    return bytes(out[:length])

def test_fuzz_equivalence():
    oracle_bin = "/app/legacy_sanitizer"
    agent_bin = "/home/user/sanitizer_fixed"

    assert os.path.exists(agent_bin), f"Missing fixed binary: {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Fixed binary is not executable: {agent_bin}"
    assert os.path.exists(oracle_bin), f"Missing oracle binary: {oracle_bin}"
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary is not executable: {oracle_bin}"

    random.seed(42)
    N = 10000

    for i in range(N):
        length = random.randint(0, 4096)
        # To speed up fuzzing in tests, we mostly use small lengths, but some large ones
        if random.random() < 0.9:
            length = random.randint(0, 128)

        test_input = generate_fuzz_input(length)

        oracle_proc = subprocess.run([oracle_bin], input=test_input, capture_output=True)
        agent_proc = subprocess.run([agent_bin], input=test_input, capture_output=True)

        assert oracle_proc.returncode == agent_proc.returncode, \
            f"Exit code mismatch on input {test_input[:100]!r}... Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}"

        assert oracle_proc.stdout == agent_proc.stdout, \
            f"Output mismatch on input {test_input[:100]!r}... \nOracle: {oracle_proc.stdout[:100]!r}\nAgent: {agent_proc.stdout[:100]!r}"