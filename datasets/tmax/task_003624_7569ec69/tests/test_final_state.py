# test_final_state.py

import os
import subprocess
import random
import string
import pytest

def generate_csv(num_rows):
    devices = [f"DEV_{i}" for i in range(15)]

    lines = []
    lines.append("Timestamp,DeviceID,IPAddress,EventLog\n")

    for _ in range(num_rows):
        ts = str(random.randint(1600000000, 1700000000))
        dev = random.choice(devices)

        dots = random.randint(0, 4)
        if dots == 0:
            ip = "".join(random.choices(string.ascii_letters, k=10))
        else:
            ip = ".".join(str(random.randint(0, 255)) for _ in range(dots + 1))

        if random.random() < 0.15:
            # Embedded newline
            evt = f'"Event log part 1\npart 2 {random.randint(0, 1000)}"'
        else:
            evt = f"Normal event {random.randint(0, 1000)}"

        lines.append(f"{ts},{dev},{ip},{evt}\n")

    return "".join(lines)

def test_fuzz_equivalence():
    agent_bin = "/home/user/cleaner"
    oracle_bin = "/app/oracle_cleaner"

    assert os.path.exists(agent_bin), f"Agent binary not found at {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary not executable at {agent_bin}"

    assert os.path.exists(oracle_bin), f"Oracle binary not found at {oracle_bin}"
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary not executable at {oracle_bin}"

    random.seed(42)

    for i in range(500):
        num_rows = random.randint(0, 500)
        csv_data = generate_csv(num_rows)

        try:
            agent_proc = subprocess.run([agent_bin], input=csv_data.encode('utf-8'), capture_output=True, timeout=2)
            agent_out = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent binary timed out on fuzz input {i} (rows={num_rows}).")

        try:
            oracle_proc = subprocess.run([oracle_bin], input=csv_data.encode('utf-8'), capture_output=True, timeout=2)
            oracle_out = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle binary timed out on fuzz input {i} (rows={num_rows}).")

        if agent_out != oracle_out:
            # Truncate input for display if it's too long
            display_input = csv_data if len(csv_data) < 1000 else csv_data[:1000] + "\n...[truncated]"
            pytest.fail(
                f"Mismatch on fuzz input {i} (rows={num_rows}).\n\n"
                f"--- Oracle Output Length ---\n{len(oracle_out)} bytes\n\n"
                f"--- Agent Output Length ---\n{len(agent_out)} bytes\n\n"
                f"--- Input CSV (first 1000 chars) ---\n{display_input}"
            )