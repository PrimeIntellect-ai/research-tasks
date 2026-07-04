# test_final_state.py

import os
import subprocess
import random
import string
import pytest

def generate_fuzz_input(num_lines=1000, seed=42):
    random.seed(seed)
    lines = []
    encodings = ["utf-8", "iso-8859-1", "windows-1252"]

    for _ in range(num_lines):
        ts = random.randint(1600000000, 1700000000)
        encoding = random.choice(encodings)

        # Determine if we should generate invalid hex
        if random.random() < 0.05:
            # Invalid hex
            hex_payload = "invalid_hex_string_xyz!"
        else:
            # Valid hex
            length = random.randint(10, 50)
            if encoding == "utf-8":
                chars = ''.join(random.choices(string.ascii_letters + string.digits + " \n\t", k=length))
                b = chars.encode('utf-8')
            elif encoding == "iso-8859-1":
                chars = ''.join(chr(random.randint(32, 255)) for _ in range(length))
                b = chars.encode('iso-8859-1', errors='replace')
            else:
                chars = ''.join(chr(random.randint(32, 255)) for _ in range(length))
                b = chars.encode('windows-1252', errors='replace')
            hex_payload = b.hex()

        lines.append(f"{ts},{encoding},{hex_payload}")

    return "\n".join(lines) + "\n"

def test_agent_program_fuzz_equivalence():
    agent_bin = "/home/user/transformer"
    oracle_bin = "/opt/oracle/transformer_oracle"

    assert os.path.isfile(agent_bin), f"Agent binary not found at {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary {agent_bin} is not executable"
    assert os.path.isfile(oracle_bin), f"Oracle binary not found at {oracle_bin}"
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary {oracle_bin} is not executable"

    fuzz_input = generate_fuzz_input(num_lines=1000, seed=1337)

    # Run oracle
    oracle_proc = subprocess.run(
        [oracle_bin],
        input=fuzz_input.encode('utf-8'),
        capture_output=True
    )
    assert oracle_proc.returncode == 0, f"Oracle failed: {oracle_proc.stderr.decode('utf-8', errors='replace')}"
    oracle_output = oracle_proc.stdout.decode('utf-8', errors='replace')

    # Run agent
    agent_proc = subprocess.run(
        [agent_bin],
        input=fuzz_input.encode('utf-8'),
        capture_output=True
    )
    assert agent_proc.returncode == 0, f"Agent program failed: {agent_proc.stderr.decode('utf-8', errors='replace')}"
    agent_output = agent_proc.stdout.decode('utf-8', errors='replace')

    if agent_output != oracle_output:
        # Limit output in error message
        max_len = 1000
        oracle_trunc = oracle_output[:max_len] + ("..." if len(oracle_output) > max_len else "")
        agent_trunc = agent_output[:max_len] + ("..." if len(agent_output) > max_len else "")
        pytest.fail(
            f"Agent output does not match oracle output.\n\n"
            f"--- Expected (Oracle) ---\n{oracle_trunc}\n\n"
            f"--- Actual (Agent) ---\n{agent_trunc}\n"
        )

def test_makefile_fixed():
    path = "/app/locales-dag/Makefile"
    assert os.path.isfile(path), f"File {path} does not exist"
    with open(path, "r") as f:
        lines = f.readlines()
    has_space_indent = any(line.startswith("    ") for line in lines)
    assert not has_space_indent, "Makefile still has spaces instead of tabs for indentation"

def test_scheduler_bug_fixed():
    path = "/app/locales-dag/scheduler.go"
    assert os.path.isfile(path), f"File {path} does not exist"
    with open(path, "r") as f:
        content = f.read()
    assert "len(sorted)-1" not in content, "scheduler.go still has the off-by-one bug"