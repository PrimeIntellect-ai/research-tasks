# test_final_state.py

import os
import subprocess
import random
import string
import pytest

def test_part1_netlogs_dir():
    """Verify that the netlogs directory was created correctly."""
    assert os.path.isdir("/home/user/netlogs"), "Directory /home/user/netlogs does not exist. Did you transcribe the audio correctly?"

def test_part1_git_hook():
    """Verify that the post-receive hook is configured correctly."""
    hook_path = "/home/user/netconfig.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Hook file {hook_path} does not exist."
    assert os.access(hook_path, os.X_OK), f"Hook file {hook_path} is not executable."

    with open(hook_path, "r") as f:
        content = f.read()

    # Check for LOG_DIR assignment
    assert "LOG_DIR=/home/user/netlogs" in content or "LOG_DIR='/home/user/netlogs'" in content or 'LOG_DIR="/home/user/netlogs"' in content, \
        "LOG_DIR is not set correctly in the hook. It should be set to /home/user/netlogs"

def test_part2_fuzz_equivalence():
    """Fuzz the agent's C++ program against the oracle."""
    oracle = "/app/oracle_normalizer"
    agent = "/home/user/ip_normalizer"

    assert os.path.isfile(agent), f"Agent binary {agent} does not exist. Did you compile the C++ code?"
    assert os.access(agent, os.X_OK), f"Agent binary {agent} is not executable."

    random.seed(42)

    test_cases = []

    # 1. Valid cases
    for _ in range(1000):
        a = random.randint(0, 255)
        b = random.randint(0, 255)
        c = random.randint(0, 255)
        d = random.randint(0, 255)
        status = random.choice(["UP", "DOWN"])
        test_cases.append(f"{a}.{b}.{c}.{d} {status}")

    # 2. Invalid cases (out of range)
    for _ in range(1000):
        a = random.randint(256, 999)
        b = random.randint(0, 255)
        c = random.randint(0, 255)
        d = random.randint(0, 255)
        status = random.choice(["UP", "DOWN"])
        test_cases.append(f"{a}.{b}.{c}.{d} {status}")

    # 3. Invalid cases (leading zeros)
    for _ in range(500):
        test_cases.append(f"01.2.3.4 UP")
        test_cases.append(f"1.02.3.4 DOWN")
        test_cases.append(f"00.0.0.0 UP")

    # 4. Random garbage and edge cases
    for _ in range(2500):
        length = random.randint(1, 50)
        tc = "".join(random.choices(string.printable, k=length))
        test_cases.append(tc)

    test_cases.extend([
        "",
        "192.168.1.1  UP",
        " 192.168.1.1 UP",
        "192.168.1.1 UP ",
        "192.168.1.1 INVALID",
        "255.255.255.255 DOWN",
        "0.0.0.0 UP"
    ])

    for tc in test_cases:
        input_bytes = tc.encode('utf-8')

        oracle_proc = subprocess.run([oracle], input=input_bytes, capture_output=True)
        agent_proc = subprocess.run([agent], input=input_bytes, capture_output=True)

        oracle_out = oracle_proc.stdout
        agent_out = agent_proc.stdout

        assert oracle_out == agent_out, \
            f"Mismatch on input {repr(tc)}.\nOracle output: {repr(oracle_out)}\nAgent output: {repr(agent_out)}"