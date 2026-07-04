# test_final_state.py
import os
import random
import subprocess
import tempfile
import string
import pytest

def generate_fuzz_input(seed):
    random.seed(seed)
    length = random.randint(10, 500)
    out = bytearray(random.getrandbits(8) for _ in range(length))

    # Inject magic numbers to trigger edge cases
    num_injects = random.randint(0, 3)
    for _ in range(num_injects):
        if length < 6:
            continue
        idx = random.randint(0, length - 6)
        out[idx:idx+4] = b'\xef\xbe\xad\xde'
        # Random length
        out[idx+4] = random.randint(0, 255)
        out[idx+5] = random.randint(0, 255)

    # Occasionally inject a completely valid record to ensure it parses correctly
    if random.random() < 0.2:
        payload = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 20))).encode('ascii')
        L = len(payload)
        record = bytearray(b'\xef\xbe\xad\xde')
        record.append(L & 0xFF)
        record.append((L >> 8) & 0xFF)
        record.extend(payload)
        checksum = 0
        for b in payload:
            checksum ^= b
        record.append(checksum)
        # Randomly place it or append it
        if len(out) > len(record):
            idx = random.randint(0, len(out) - len(record))
            out[idx:idx+len(record)] = record

    return bytes(out)

def test_fuzz_equivalence():
    agent_script = '/home/user/recover.py'
    oracle_bin = '/app/wal_recovery_tool_oracle'

    assert os.path.isfile(agent_script), f"Agent script {agent_script} not found."
    assert os.path.isfile(oracle_bin), f"Oracle binary {oracle_bin} not found."

    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, 'input.wal')

        for i in range(1000):
            data = generate_fuzz_input(i)
            with open(input_file, 'wb') as f:
                f.write(data)

            # Run oracle
            try:
                oracle_proc = subprocess.run([oracle_bin, input_file], capture_output=True, timeout=2)
                oracle_out = oracle_proc.stdout
            except subprocess.TimeoutExpired:
                pytest.fail(f"Oracle script timed out on input seed {i}. This shouldn't happen.")

            # Run agent
            try:
                agent_proc = subprocess.run(['python3', agent_script, input_file], capture_output=True, timeout=2)
                agent_out = agent_proc.stdout
            except subprocess.TimeoutExpired:
                pytest.fail(f"Agent script timed out on input seed {i} (possible infinite loop).")

            if agent_out != oracle_out:
                pytest.fail(
                    f"Mismatch on seed {i}.\n"
                    f"Input hex: {data.hex()}\n"
                    f"Oracle output: {oracle_out}\n"
                    f"Agent output: {agent_out}"
                )