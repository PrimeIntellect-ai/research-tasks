# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_compiled_binaries_exist():
    tester_amd64 = "/home/user/bin/tester_amd64"
    tester_arm64 = "/home/user/bin/tester_arm64"
    tester_go = "/home/user/tester/tester.go"

    assert os.path.isfile(tester_go), f"Missing Go source file: {tester_go}"
    assert os.path.isfile(tester_amd64), f"Missing compiled binary: {tester_amd64}"
    assert os.path.isfile(tester_arm64), f"Missing compiled binary: {tester_arm64}"

    # Check executable permissions
    assert os.access(tester_amd64, os.X_OK), f"{tester_amd64} is not executable"
    assert os.access(tester_arm64, os.X_OK), f"{tester_arm64} is not executable"

def generate_fuzz_inputs(n=1000, seed=42):
    random.seed(seed)
    chars = string.ascii_letters + string.digits + "_."
    inputs = []
    for _ in range(n):
        length = random.randint(5, 25)
        base = "".join(random.choices(chars, k=length))

        # Bias the inputs
        prob = random.random()
        if prob < 0.15:
            base = "test_" + base[5:]
        elif prob < 0.30:
            base = base[:-3] + ".go"
        elif prob < 0.45:
            insert_pos = random.randint(0, len(base))
            base = base[:insert_pos] + "config" + base[insert_pos:]
        elif prob < 0.55:
            # combination
            base = "test_" + base[5:-3] + ".go"

        # Ensure length constraints roughly if needed, but oracle handles any length
        inputs.append(base)
    return inputs

def test_fuzz_equivalence():
    agent_script = "/home/user/router.py"
    oracle_bin = "/app/legacy_router"

    assert os.path.isfile(agent_script), f"Agent script missing: {agent_script}"
    assert os.path.isfile(oracle_bin), f"Oracle binary missing: {oracle_bin}"

    inputs = generate_fuzz_inputs(n=1000)

    for val in inputs:
        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_bin, val],
            capture_output=True,
            text=True
        )
        oracle_out = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            ["python3", agent_script, val],
            capture_output=True,
            text=True
        )
        agent_out = agent_proc.stdout

        assert oracle_out == agent_out, (
            f"Output mismatch for input: '{val}'\n"
            f"Oracle output: '{oracle_out}'\n"
            f"Agent output: '{agent_out}'\n"
            f"Agent stderr: '{agent_proc.stderr}'"
        )