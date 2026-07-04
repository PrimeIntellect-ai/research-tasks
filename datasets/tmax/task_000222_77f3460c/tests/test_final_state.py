# test_final_state.py

import os
import random
import subprocess
import string
import pytest

AGENT_PROGRAM = "/home/user/telemetry_filter"
ORACLE_PROGRAM = "/app/oracle_telemetry_filter"

def generate_random_ip(in_subnet=False):
    if in_subnet:
        # 172.16.0.0/12 means first octet 172, second octet 16-31
        return f"172.{random.randint(16, 31)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
    else:
        return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

def generate_malformed_ip():
    choices = [
        "256.256.256.256",
        "172.16.0",
        "not.an.ip.address",
        "172.16.0.0/12",
        "172.16.0.0.0"
    ]
    return random.choice(choices)

def generate_test_data(n=1000, seed=42):
    random.seed(seed)
    lines = []
    statuses = ["OFFLINE", "ONLINE", "ERROR", "REBOOTING"]

    for _ in range(n):
        dev_id_len = random.randint(5, 15)
        dev_id = ''.join(random.choices(string.ascii_letters + string.digits, k=dev_id_len))

        ip_choice = random.random()
        if ip_choice < 0.05:
            ip = generate_malformed_ip()
        elif ip_choice < 0.525: # roughly 50% of the remaining 95% + some to make it 50% overall
            ip = generate_random_ip(in_subnet=True)
        else:
            ip = generate_random_ip(in_subnet=False)

        status = random.choice(statuses)
        lines.append(f"{dev_id},{ip},{status}")

    return "\n".join(lines)

def test_agent_program_exists():
    assert os.path.exists(AGENT_PROGRAM), f"Agent program not found at {AGENT_PROGRAM}"
    assert os.path.isfile(AGENT_PROGRAM), f"{AGENT_PROGRAM} is not a file"
    assert os.access(AGENT_PROGRAM, os.X_OK), f"{AGENT_PROGRAM} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PROGRAM), f"Oracle program not found at {ORACLE_PROGRAM}"
    assert os.access(ORACLE_PROGRAM, os.X_OK), f"Oracle program is not executable"

    test_input = generate_test_data(1000, seed=1337)

    oracle_proc = subprocess.run(
        [ORACLE_PROGRAM],
        input=test_input,
        text=True,
        capture_output=True,
        check=False
    )
    assert oracle_proc.returncode == 0, f"Oracle program failed with stderr: {oracle_proc.stderr}"

    agent_proc = subprocess.run(
        [AGENT_PROGRAM],
        input=test_input,
        text=True,
        capture_output=True,
        check=False
    )

    if agent_proc.returncode != 0:
        pytest.fail(f"Agent program failed with exit code {agent_proc.returncode}. Stderr: {agent_proc.stderr}")

    oracle_lines = oracle_proc.stdout.strip().split('\n')
    agent_lines = agent_proc.stdout.strip().split('\n')

    if len(oracle_lines) != len(agent_lines):
        pytest.fail(f"Output line count mismatch. Expected {len(oracle_lines)} lines, got {len(agent_lines)} lines.")

    input_lines = test_input.split('\n')

    for i, (oracle_line, agent_line) in enumerate(zip(oracle_lines, agent_lines)):
        if oracle_line != agent_line:
            pytest.fail(
                f"Output mismatch at line {i+1}:\n"
                f"Input : {input_lines[i]}\n"
                f"Oracle: {oracle_line}\n"
                f"Agent : {agent_line}"
            )