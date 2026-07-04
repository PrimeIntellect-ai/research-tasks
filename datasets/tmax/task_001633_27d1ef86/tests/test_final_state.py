# test_final_state.py
import os
import random
import subprocess
import pytest

ORACLE_PATH = "/app/bin/oracle_parser"
AGENT_PATH = "/home/user/fast_parser_fixed"

def test_agent_executable_exists():
    assert os.path.isfile(AGENT_PATH), f"Expected executable {AGENT_PATH} is missing. Did you compile your fixed code?"
    assert os.access(AGENT_PATH, os.X_OK), f"Expected {AGENT_PATH} to be executable."

def generate_input():
    ops = []
    length = random.randint(0, 100)
    for _ in range(length):
        op_type = random.choice(['ADD', 'SUB', 'MUL', 'HEX', 'REV', 'END'])
        if op_type in ['ADD', 'SUB', 'MUL']:
            ops.append(f"{op_type} {random.randint(-1000, 1000)}")
        elif op_type == 'HEX':
            # Mix valid and invalid hex to test the bug fix
            if random.random() < 0.5:
                ops.append(f"HEX {random.choice('0123456789ABCDEF')}{random.choice('0123456789ABCDEF')}")
            else:
                ops.append(f"HEX {random.choice('0123456789GHIJKLMNOPQRSTUVWXYZ')}{random.choice('0123456789GHIJKLMNOPQRSTUVWXYZ')}")
        else:
            ops.append(op_type)
    return " ".join(ops)

def test_fuzz_equivalence():
    random.seed(42)

    # Run 1000 random inputs to ensure equivalence without timing out the test suite
    N = 1000
    for i in range(N):
        test_input = generate_input()

        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=test_input,
            text=True,
            capture_output=True
        )

        agent_proc = subprocess.run(
            [AGENT_PATH],
            input=test_input,
            text=True,
            capture_output=True
        )

        assert agent_proc.returncode == oracle_proc.returncode, (
            f"Return code mismatch on input: '{test_input}'\n"
            f"Oracle returned: {oracle_proc.returncode}\n"
            f"Agent returned: {agent_proc.returncode}\n"
            f"Agent stderr: {agent_proc.stderr}"
        )

        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Stdout mismatch on input: '{test_input}'\n"
            f"Oracle stdout: {oracle_proc.stdout!r}\n"
            f"Agent stdout: {agent_proc.stdout!r}"
        )