# test_final_state.py

import os
import subprocess
import random
import pytest

def encode_varint(value: int) -> bytes:
    if value == 0:
        return b'\x00'
    res = bytearray()
    while value:
        byte = value & 0x7f
        value >>= 7
        if value:
            res.append(byte | 0x80)
        else:
            res.append(byte)
    return bytes(res)

def encode_operations(values: list[int]) -> str:
    payload = b''.join(encode_varint(v) for v in values)
    if not payload:
        return ""
    msg = b'\x0a' + encode_varint(len(payload)) + payload
    return msg.hex()

def test_solution_exists():
    assert os.path.isfile("/home/user/solution.py"), "The solution script /home/user/solution.py does not exist."

def test_fuzz_equivalence():
    oracle_path = "/app/oracle"
    agent_cmd = ["python3", "/home/user/solution.py"]

    assert os.path.isfile(oracle_path), f"Oracle not found at {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle at {oracle_path} is not executable"

    random.seed(42)

    for i in range(100):
        # Generate random length between 0 and 20
        length = random.randint(0, 20)
        # Generate random uint64 values
        values = [random.randint(0, (1 << 64) - 1) for _ in range(length)]

        hex_input = encode_operations(values)

        # Run oracle
        try:
            oracle_res = subprocess.run([oracle_path, hex_input], capture_output=True, text=True, timeout=5)
            oracle_output = oracle_res.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail("Oracle timed out on input.")

        # Run agent
        try:
            agent_res = subprocess.run(agent_cmd + [hex_input], capture_output=True, text=True, timeout=5)
            agent_output = agent_res.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent timed out on input: {hex_input}")

        assert agent_res.returncode == 0, f"Agent script failed with return code {agent_res.returncode}. Stderr: {agent_res.stderr}"
        assert agent_output == oracle_output, f"Mismatch on input {hex_input}\nExpected: {oracle_output}\nGot: {agent_output}"