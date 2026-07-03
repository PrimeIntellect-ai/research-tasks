# test_final_state.py

import os
import subprocess
import base64
import random
import pytest

ORACLE_PATH = "/app/oracle_bin"
AGENT_PATH = "/home/user/evaluator.py"
N_TESTS = 1000

def generate_fuzz_inputs(n, seed=42):
    random.seed(seed)
    inputs = []
    for i in range(n):
        choice = random.random()
        if choice < 0.2:
            # Completely random bytes
            length = random.randint(10, 100)
            data = bytes(random.getrandbits(8) for _ in range(length))
        elif choice < 0.4:
            # Invalid header
            header = b"WRONG_HD"
            opcode = random.choice([0x10, 0x20, 0x30])
            payload = b" ".join(str(random.randint(-100, 100)).encode() for _ in range(random.randint(1, 10)))
            length = len(payload)
            data = header + bytes([opcode]) + length.to_bytes(2, 'big') + payload
        elif choice < 0.6:
            # Unknown opcode
            header = b"CALC_V2!"
            opcode = random.choice([0x00, 0x40, 0xFF])
            payload = b" ".join(str(random.randint(-100, 100)).encode() for _ in range(random.randint(1, 10)))
            length = len(payload)
            data = header + bytes([opcode]) + length.to_bytes(2, 'big') + payload
        elif choice < 0.8:
            # Malformed payload
            header = b"CALC_V2!"
            opcode = random.choice([0x10, 0x20, 0x30])
            payload = b"12 34 abc 56"
            length = len(payload)
            data = header + bytes([opcode]) + length.to_bytes(2, 'big') + payload
        else:
            # Valid payload
            header = b"CALC_V2!"
            opcode = random.choice([0x10, 0x20, 0x30])
            payload = b" ".join(str(random.randint(-100, 100)).encode() for _ in range(random.randint(1, 10)))
            length = len(payload)
            data = header + bytes([opcode]) + length.to_bytes(2, 'big') + payload

        inputs.append(base64.b64encode(data).decode('ascii'))
    return inputs

def run_cmd(cmd, arg):
    try:
        result = subprocess.run(
            cmd + [arg],
            capture_output=True,
            text=True,
            timeout=2
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"
    assert os.path.exists(AGENT_PATH), f"Agent script not found at {AGENT_PATH}"

    inputs = generate_fuzz_inputs(N_TESTS)

    for i, b64_input in enumerate(inputs):
        oracle_code, oracle_out, oracle_err = run_cmd([ORACLE_PATH], b64_input)
        agent_code, agent_out, agent_err = run_cmd(["python3", AGENT_PATH], b64_input)

        error_msg = (
            f"Mismatch on input {i}:\n"
            f"Input (base64): {b64_input}\n"
            f"Oracle return code: {oracle_code}, Agent return code: {agent_code}\n"
            f"Oracle stdout: {oracle_out!r}, Agent stdout: {agent_out!r}\n"
            f"Oracle stderr: {oracle_err!r}, Agent stderr: {agent_err!r}"
        )

        assert oracle_code == agent_code, error_msg
        assert oracle_out == agent_out, error_msg
        assert oracle_err == agent_err, error_msg