# test_final_state.py
import os
import subprocess
import random
import pytest

def test_agent_binary_exists():
    agent_path = "/home/user/auditor"
    assert os.path.isfile(agent_path), f"Agent binary {agent_path} does not exist."
    assert os.access(agent_path, os.X_OK), f"Agent binary {agent_path} is not executable."

def run_binary(binary_path, input_data):
    try:
        result = subprocess.run(
            [binary_path],
            input=input_data,
            capture_output=True,
            timeout=1
        )
        return result.stdout, result.returncode
    except subprocess.TimeoutExpired:
        return None, None

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_auditor"
    agent_path = "/home/user/auditor"

    assert os.path.isfile(oracle_path), f"Oracle binary {oracle_path} does not exist."
    assert os.access(oracle_path, os.X_OK), f"Oracle binary {oracle_path} is not executable."

    random.seed(42)

    # Generate random fuzzing inputs + targeted inputs to ensure branch coverage
    inputs = []

    # Targeted: ELF
    data = bytearray(os.urandom(32))
    data[0:4] = b'\x7fELF'
    inputs.append(bytes(data))

    # Targeted: SUID
    data = bytearray(os.urandom(32))
    data[0:4] = b'\x00\x00\x00\x00'
    data[4:6] = b'\x00\x08'
    inputs.append(bytes(data))

    # Targeted: PAYLOAD
    data = bytearray(os.urandom(32))
    data[0:4] = b'\x00\x00\x00\x00'
    data[4:6] = b'\x00\x00'
    data[16:20] = b'\x90\x90\x90\x90'
    inputs.append(bytes(data))

    # Random fuzzing
    for _ in range(10000):
        inputs.append(os.urandom(32))

    for i, input_data in enumerate(inputs):
        oracle_out, oracle_code = run_binary(oracle_path, input_data)
        agent_out, agent_code = run_binary(agent_path, input_data)

        assert agent_out is not None, f"Agent binary timed out on input {input_data.hex()}"
        assert agent_out == oracle_out, (
            f"Output mismatch on input {input_data.hex()}.\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output: {agent_out}"
        )
        assert agent_code == oracle_code, (
            f"Return code mismatch on input {input_data.hex()}.\n"
            f"Oracle code: {oracle_code}\n"
            f"Agent code: {agent_code}"
        )