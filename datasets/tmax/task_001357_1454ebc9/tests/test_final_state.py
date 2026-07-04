# test_final_state.py
import os
import subprocess
import random
import struct
import string
import pytest

def generate_valid_payload(length):
    payload = bytearray()
    while len(payload) < length:
        is_secret = random.choice([True, False])
        line_len = random.randint(1, 100)
        line = ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=line_len))
        if is_secret:
            line = 'SECRET:' + line
        payload.extend(line.encode('ascii') + b'\n')
    return bytes(payload[:length])

def generate_fuzz_inputs(n=500):
    inputs = []
    random.seed(42)
    for _ in range(n):
        choice = random.random()
        if choice < 0.2:
            # invalid magic bytes
            magic = bytes(random.choices(range(256), k=4))
            if magic == b'BKA\x01':
                magic = b'BKA\x00'
            payload = b'test_payload'
            length = struct.pack('<I', len(payload))
            csum = struct.pack('<I', sum(payload) % (2**32))
            inputs.append(magic + length + payload + csum)
        elif choice < 0.4:
            # truncated payloads
            magic = b'BKA\x01'
            payload = generate_valid_payload(random.randint(10, 1000))
            length = struct.pack('<I', len(payload) + random.randint(1, 100))
            csum = struct.pack('<I', sum(payload) % (2**32))
            inputs.append(magic + length + payload + csum)
        elif choice < 0.6:
            # bad checksum
            magic = b'BKA\x01'
            payload = generate_valid_payload(random.randint(10, 1000))
            length = struct.pack('<I', len(payload))
            csum = struct.pack('<I', (sum(payload) + random.randint(1, 1000)) % (2**32))
            inputs.append(magic + length + payload + csum)
        else:
            # valid archive
            magic = b'BKA\x01'
            payload = generate_valid_payload(random.randint(0, 50000))
            length = struct.pack('<I', len(payload))
            csum = struct.pack('<I', sum(payload) % (2**32))
            inputs.append(magic + length + payload + csum)
    return inputs

def run_binary(binary_path, input_data):
    try:
        proc = subprocess.run(
            [binary_path],
            input=input_data,
            capture_output=True,
            timeout=2
        )
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return -1, b"", b"Timeout"
    except Exception as e:
        return -2, b"", str(e).encode()

def test_fuzz_equivalence():
    oracle_path = "/app/oracle/bup_filter_oracle"
    agent_path = "/home/user/bup_filter"

    assert os.path.isfile(agent_path), f"Agent binary not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary at {agent_path} is not executable"

    inputs = generate_fuzz_inputs(500)

    for i, input_data in enumerate(inputs):
        oracle_rc, oracle_out, oracle_err = run_binary(oracle_path, input_data)
        agent_rc, agent_out, agent_err = run_binary(agent_path, input_data)

        assert agent_rc == oracle_rc, f"Return code mismatch on input {i}. Oracle: {oracle_rc}, Agent: {agent_rc}\nInput snippet: {input_data[:50]}"
        assert agent_out == oracle_out, f"Stdout mismatch on input {i}.\nOracle: {oracle_out[:100]}\nAgent: {agent_out[:100]}"
        assert agent_err == oracle_err, f"Stderr mismatch on input {i}.\nOracle: {oracle_err}\nAgent: {agent_err}"

def test_proxy_script_exists():
    script_path = "/home/user/start_proxy.sh"
    assert os.path.isfile(script_path), f"Proxy script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Proxy script at {script_path} is not executable"

def test_end_to_end_flow():
    success_file = "/tmp/flow_success"
    assert os.path.isfile(success_file), f"End-to-end flow success file {success_file} not found. The proxy might not be running or forwarding data correctly."