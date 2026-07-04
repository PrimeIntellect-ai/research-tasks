# test_final_state.py

import os
import random
import string
import subprocess
import pytest

AGENT_PROGRAM = "/home/user/fast_hasher"
ORACLE_PROGRAM = "/app/.hidden/reference_hasher"
N_INPUTS = 10000

def test_agent_program_exists_and_executable():
    assert os.path.exists(AGENT_PROGRAM), f"Agent program not found at {AGENT_PROGRAM}"
    assert os.path.isfile(AGENT_PROGRAM), f"{AGENT_PROGRAM} is not a file"
    assert os.access(AGENT_PROGRAM, os.X_OK), f"{AGENT_PROGRAM} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PROGRAM), f"Oracle program missing at {ORACLE_PROGRAM}"
    assert os.access(ORACLE_PROGRAM, os.X_OK), f"Oracle program not executable"

    random.seed(42)
    charset = [chr(i) for i in range(0x20, 0x7F)]

    inputs = []
    for _ in range(N_INPUTS):
        length = random.randint(1, 1024)
        inp = "".join(random.choices(charset, k=length))
        inputs.append(inp)

    # Ensure some inputs contain "CRASH" to test the crash fix
    inputs[10] = "CRASH"
    inputs[100] = "FOOCRASHBAR"
    inputs[1000] = "CRASH" * 10

    input_data = "\n".join(inputs) + "\n"
    input_bytes = input_data.encode('utf-8')

    try:
        oracle_proc = subprocess.run(
            [ORACLE_PROGRAM],
            input=input_bytes,
            capture_output=True,
            check=True,
            timeout=10
        )
        oracle_output = oracle_proc.stdout.decode('utf-8').splitlines()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Oracle program failed: {e.stderr.decode('utf-8')}")
    except subprocess.TimeoutExpired:
        pytest.fail("Oracle program timed out")

    try:
        agent_proc = subprocess.run(
            [AGENT_PROGRAM],
            input=input_bytes,
            capture_output=True,
            check=False,
            timeout=10
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Agent program timed out")

    if agent_proc.returncode != 0:
        pytest.fail(f"Agent program exited with non-zero code {agent_proc.returncode}. Stderr: {agent_proc.stderr.decode('utf-8', errors='replace')}")

    agent_output = agent_proc.stdout.decode('utf-8').splitlines()

    assert len(agent_output) == len(oracle_output), \
        f"Output line count mismatch: expected {len(oracle_output)}, got {len(agent_output)}"

    for i, (oracle_line, agent_line) in enumerate(zip(oracle_output, agent_output)):
        if oracle_line != agent_line:
            failed_input = inputs[i]
            pytest.fail(
                f"Mismatch on input line {i+1}.\n"
                f"Input: {repr(failed_input)}\n"
                f"Expected output: {oracle_line}\n"
                f"Agent output: {agent_line}"
            )