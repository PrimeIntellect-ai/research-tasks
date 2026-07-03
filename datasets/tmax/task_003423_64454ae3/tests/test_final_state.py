# test_final_state.py
import os
import random
import subprocess
import pytest

def encode_varint(value):
    if value < 0:
        value = (1 << 64) + value
    out = bytearray()
    while True:
        b = value & 0x7f
        value >>= 7
        if value:
            out.append(b | 0x80)
        else:
            out.append(b)
            break
    return bytes(out)

def encode_legacy_log(id_val, py2_message_bytes):
    out = bytearray()
    # Field 1: id (int32), tag = 8
    out.extend(encode_varint(8))
    out.extend(encode_varint(id_val))

    # Field 2: py2_message (bytes), tag = 18
    out.extend(encode_varint(18))
    out.extend(encode_varint(len(py2_message_bytes)))
    out.extend(py2_message_bytes)

    return bytes(out)

def test_migrator_fuzz_equivalence():
    agent_bin = "/home/user/migrator"
    oracle_bin = "/app/oracle_migrator"

    assert os.path.isfile(agent_bin), f"Agent binary not found at {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary at {agent_bin} is not executable"

    assert os.path.isfile(oracle_bin), f"Oracle binary not found at {oracle_bin}"
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary at {oracle_bin} is not executable"

    random.seed(42)

    for i in range(100):
        # Generate random data
        id_val = random.randint(-10000, 10000)
        msg_len = random.randint(5, 200)
        py2_message = bytes([random.randint(0, 255) for _ in range(msg_len)])

        # Create serialized input
        input_data = encode_legacy_log(id_val, py2_message)

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_bin],
            input=input_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input {i}"
        oracle_output = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            [agent_bin],
            input=input_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        assert agent_proc.returncode == 0, f"Agent binary failed (exit code {agent_proc.returncode}) on input {i}:\nstderr: {agent_proc.stderr.decode(errors='replace')}"
        agent_output = agent_proc.stdout

        assert agent_output == oracle_output, (
            f"Output mismatch on input {i} (id={id_val}, msg_len={msg_len}).\n"
            f"Expected {len(oracle_output)} bytes, got {len(agent_output)} bytes.\n"
            f"Oracle output (hex): {oracle_output.hex()}\n"
            f"Agent output (hex): {agent_output.hex()}"
        )