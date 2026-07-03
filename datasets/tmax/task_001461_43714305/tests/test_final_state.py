# test_final_state.py

import os
import subprocess
import random
import string
import pytest

def test_glitch_frames():
    glitch_file = "/home/user/glitch_frames.txt"
    assert os.path.exists(glitch_file), f"File {glitch_file} does not exist."

    with open(glitch_file, "r") as f:
        lines = f.read().strip().splitlines()

    actual_frames = []
    for line in lines:
        line = line.strip()
        if line:
            try:
                actual_frames.append(int(line))
            except ValueError:
                pytest.fail(f"Invalid non-integer line in {glitch_file}: {line}")

    expected_frames = [42, 43, 89, 144, 145, 146, 250]
    assert actual_frames == expected_frames, f"Expected frames {expected_frames}, but got {actual_frames}"

def generate_fuzz_input(num_lines=50000, seed=42):
    random.seed(seed)
    lines = []

    def rand_string(length):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def valid_timestamp():
        return f"{random.randint(2000, 2024):04d}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}T{random.randint(0, 23):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}Z"

    last_key = "initial_key"

    for _ in range(num_lines):
        r = random.random()
        if r < 0.40:
            # Valid
            if random.random() < 0.30:
                key = last_key
            else:
                key = rand_string(8)
                last_key = key
            email = f"{rand_string(5)}@{rand_string(5)}.com"
            lines.append(f"{valid_timestamp()}|{email}|{key}|{rand_string(10)}\n".encode('utf-8'))
        elif r < 0.70:
            # Malformed
            lines.append(f"BAD_TIME|{rand_string(5)}@{rand_string(5)}.com|key|text\n".encode('utf-8'))
        elif r < 0.90:
            # Edge-case emails
            email_type = random.choice(['1char', '2char', 'no_at', 'multi_at'])
            if email_type == '1char':
                email = f"a@{rand_string(5)}.com"
            elif email_type == '2char':
                email = f"ab@{rand_string(5)}.com"
            elif email_type == 'no_at':
                email = f"{rand_string(10)}.com"
            else:
                email = f"a@b@c.com"
            lines.append(f"{valid_timestamp()}|{email}|{rand_string(8)}|{rand_string(10)}\n".encode('utf-8'))
        else:
            # Binary noise
            length = random.randint(1, 1024)
            noise = bytes(random.choices(range(256), k=length))
            # Ensure it ends with newline to avoid hanging last line issues if not handled
            if not noise.endswith(b'\n'):
                noise = noise[:-1] + b'\n' if length > 1 else b'\n'
            lines.append(noise)

    return b''.join(lines)

def test_fuzz_equivalence():
    oracle_path = "/app/bin/oracle_process_loc"
    agent_path = "/home/user/process_loc"

    assert os.path.exists(agent_path), f"Agent binary not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary at {agent_path} is not executable"

    fuzz_input = generate_fuzz_input(50000, seed=1337)

    try:
        oracle_proc = subprocess.run([oracle_path], input=fuzz_input, capture_output=True, timeout=10)
        oracle_out = oracle_proc.stdout
    except subprocess.TimeoutExpired:
        pytest.fail("Oracle process timed out.")

    try:
        agent_proc = subprocess.run([agent_path], input=fuzz_input, capture_output=True, timeout=10)
        agent_out = agent_proc.stdout
    except subprocess.TimeoutExpired:
        pytest.fail("Agent process timed out. Check for infinite loops or inefficient processing.")

    if oracle_out != agent_out:
        # Find the first differing line
        oracle_lines = oracle_out.split(b'\n')
        agent_lines = agent_out.split(b'\n')

        diff_idx = -1
        for i in range(max(len(oracle_lines), len(agent_lines))):
            o_line = oracle_lines[i] if i < len(oracle_lines) else b"<EOF>"
            a_line = agent_lines[i] if i < len(agent_lines) else b"<EOF>"
            if o_line != a_line:
                diff_idx = i
                break

        pytest.fail(f"Output mismatch at line {diff_idx + 1}.\nOracle: {oracle_lines[diff_idx]}\nAgent: {agent_lines[diff_idx]}")