# test_final_state.py
import os
import subprocess
import random
import string
import pytest

AGENT_EXE = "/home/user/emulator_project/build/vm_emulator"
ORACLE_EXE = "/app/reference_emulator"
N_FUZZ = 10000

def test_agent_executable_exists():
    assert os.path.isfile(AGENT_EXE), f"Executable not found at {AGENT_EXE}. Did you build the project?"
    assert os.access(AGENT_EXE, os.X_OK), f"File at {AGENT_EXE} is not executable."

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_EXE), f"Oracle executable not found at {ORACLE_EXE}"
    assert os.access(ORACLE_EXE, os.X_OK), f"Oracle at {ORACLE_EXE} is not executable"

    # Use a fixed seed for reproducibility
    random.seed(42)
    chars = string.ascii_letters + string.digits + string.punctuation

    for _ in range(N_FUZZ):
        length = random.randint(10, 100)
        fuzz_input = "".join(random.choices(chars, k=length))

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [ORACLE_EXE, fuzz_input],
                capture_output=True,
                text=True,
                timeout=2
            )
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input: {fuzz_input}")

        assert oracle_proc.returncode == 0, f"Oracle failed on input: {fuzz_input}"
        oracle_out = oracle_proc.stdout.strip()

        # Run agent
        try:
            agent_proc = subprocess.run(
                [AGENT_EXE, fuzz_input],
                capture_output=True,
                text=True,
                timeout=2
            )
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent executable timed out on input: {fuzz_input}")

        assert agent_proc.returncode == 0, (
            f"Agent executable failed (crashed/errored) on input: {fuzz_input}\n"
            f"Stderr: {agent_proc.stderr}"
        )
        agent_out = agent_proc.stdout.strip()

        assert agent_out == oracle_out, (
            f"Output mismatch on input: {fuzz_input}\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent): {agent_out}"
        )