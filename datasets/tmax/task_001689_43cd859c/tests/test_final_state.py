# test_final_state.py
import os
import subprocess
import random
import pytest

def test_libxxhash_built():
    lib_path = "/app/vendored/xxHash-0.8.2/libxxhash.a"
    assert os.path.isfile(lib_path), f"Static library not found at {lib_path}. The Makefile perturbation might not be fixed or make was not run."

def test_executable_exists():
    executable_path = "/home/user/fast_hasher"
    assert os.path.isfile(executable_path), f"Executable not found at {executable_path}"
    assert os.access(executable_path, os.X_OK), f"File at {executable_path} is not executable"

def test_fuzz_equivalence():
    oracle_path = "/home/user/legacy_hasher.py"
    agent_path = "/home/user/fast_hasher"

    assert os.path.isfile(oracle_path), f"Oracle not found at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent executable not found at {agent_path}"

    # Generate 5000 random strings
    random.seed(42)
    printable_chars = [chr(i) for i in range(0x20, 0x7f)]

    inputs = []
    for _ in range(5000):
        length = random.randint(0, 256)
        s = "".join(random.choice(printable_chars) for _ in range(length))
        inputs.append(s)

    input_data = "\n".join(inputs) + "\n"

    # Run oracle
    oracle_proc = subprocess.run(
        [oracle_path],
        input=input_data,
        text=True,
        capture_output=True
    )
    assert oracle_proc.returncode == 0, f"Oracle failed: {oracle_proc.stderr}"

    # Run agent
    agent_proc = subprocess.run(
        [agent_path],
        input=input_data,
        text=True,
        capture_output=True
    )
    assert agent_proc.returncode == 0, f"Agent executable failed: {agent_proc.stderr}"

    oracle_lines = oracle_proc.stdout.splitlines()
    agent_lines = agent_proc.stdout.splitlines()

    if len(oracle_lines) != len(agent_lines):
        pytest.fail(f"Output line count mismatch: oracle={len(oracle_lines)}, agent={len(agent_lines)}")

    for i, (o_line, a_line) in enumerate(zip(oracle_lines, agent_lines)):
        if o_line != a_line:
            pytest.fail(f"Mismatch at output line {i}.\nExpected (Oracle): {o_line}\nGot (Agent): {a_line}")