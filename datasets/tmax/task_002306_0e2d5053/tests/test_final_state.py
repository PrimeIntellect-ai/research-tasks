# test_final_state.py
import os
import subprocess
import random
import struct
import pytest

AGENT_SCRIPT = "/home/user/chunk_decoder.py"
ORACLE_SCRIPT = "/opt/verifier/oracle_chunk_decoder.py"

def generate_fuzz_inputs(n=500):
    random.seed(42)
    inputs = []
    for i in range(n):
        category = i % 5
        if category == 0:
            # Random bytes for INVALID_MAGIC
            length = random.randint(1, 20)
            data = bytes(random.randint(0, 255) for _ in range(length))
            if len(data) >= 4 and data[:4] == b'SUBZ':
                data = b'X' + data[1:]
            inputs.append(data)
        elif category == 1:
            # Valid magic, invalid encoding
            enc = random.choice([0] + list(range(4, 256)))
            data = b'SUBZ' + bytes([enc]) + bytes(random.randint(0, 255) for _ in range(10))
            inputs.append(data)
        elif category == 2:
            # Valid magic, valid encoding, truncated payload
            enc = random.choice([1, 2, 3])
            frame = random.randint(0, 1000)
            payload_len = random.randint(5, 50)
            actual_len = random.randint(0, payload_len - 1)
            payload = bytes(random.randint(0, 255) for _ in range(actual_len))
            data = b'SUBZ' + bytes([enc]) + struct.pack(">IH", frame, payload_len) + payload
            inputs.append(data)
        elif category == 3:
            # Valid magic, valid encoding, valid payload, frame > 450
            enc = random.choice([1, 2, 3])
            frame = random.randint(451, 10000)
            payload_len = random.randint(1, 50)
            payload = bytes(random.randint(0, 255) for _ in range(payload_len))
            data = b'SUBZ' + bytes([enc]) + struct.pack(">IH", frame, payload_len) + payload
            inputs.append(data)
        elif category == 4:
            # Perfectly valid
            enc = random.choice([1, 2, 3])
            frame = random.randint(0, 450)
            payload_len = random.randint(1, 50)
            payload = bytes(random.randint(0, 255) for _ in range(payload_len))
            data = b'SUBZ' + bytes([enc]) + struct.pack(">IH", frame, payload_len) + payload
            inputs.append(data)
    return inputs

def test_chunk_decoder_fuzz_equivalence():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script {AGENT_SCRIPT} not found."
    assert os.access(AGENT_SCRIPT, os.X_OK), f"Agent script {AGENT_SCRIPT} is not executable."
    assert os.path.isfile(ORACLE_SCRIPT), f"Oracle script {ORACLE_SCRIPT} not found."

    inputs = generate_fuzz_inputs(500)

    for idx, data in enumerate(inputs):
        try:
            proc_oracle = subprocess.run(
                [ORACLE_SCRIPT],
                input=data,
                capture_output=True,
                timeout=2
            )
            oracle_out = proc_oracle.stdout
        except Exception as e:
            pytest.fail(f"Oracle script failed to run: {e}")

        try:
            proc_agent = subprocess.run(
                [AGENT_SCRIPT],
                input=data,
                capture_output=True,
                timeout=2
            )
            agent_out = proc_agent.stdout
            agent_err = proc_agent.stderr
        except Exception as e:
            pytest.fail(f"Agent script failed to run: {e}")

        assert agent_out == oracle_out, (
            f"Mismatch on fuzz input {idx}.\n"
            f"Input (hex): {data.hex()}\n"
            f"Expected stdout: {oracle_out!r}\n"
            f"Got stdout: {agent_out!r}\n"
            f"Agent stderr: {agent_err!r}"
        )