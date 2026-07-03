# test_final_state.py

import os
import sys
import json
import random
import subprocess
import pytest

def generate_fuzz_input(n=2000, seed=42):
    random.seed(seed)
    lines = []

    # Pre-generate some messages to allow duplicates
    messages = []
    for _ in range(n // 2):
        # Generate some unicode characters, including combining characters
        chars = []
        for _ in range(random.randint(5, 20)):
            base_char = chr(random.randint(0x0041, 0x005A)) # A-Z
            combining_char = chr(random.randint(0x0300, 0x036F)) # Combining Diacritical Marks
            chars.append(base_char + combining_char)
            # Add some other random characters
            if random.random() < 0.2:
                chars.append(chr(random.randint(0x0400, 0x04FF))) # Cyrillic
            if random.random() < 0.2:
                chars.append(chr(random.randint(0x3040, 0x309F))) # Hiragana
        messages.append("".join(chars))

    for _ in range(n):
        choice = random.random()
        if choice < 0.1:
            # Invalid JSON
            lines.append("this is not json { [")
        elif choice < 0.2:
            # Missing fields
            lines.append(json.dumps({"user_id": random.randint(1, 1000)}))
        elif choice < 0.3:
            # Duplicate message
            msg = random.choice(messages)
            lines.append(json.dumps({"user_id": random.randint(1, 1000), "message": msg}))
        else:
            # Valid new message
            msg = random.choice(messages)
            lines.append(json.dumps({"user_id": random.randint(1, 1000), "message": msg}))

    return "\n".join(lines) + "\n"

def test_log_filter_exists():
    path = "/home/user/log_filter.py"
    assert os.path.exists(path), f"Agent's script is missing: {path}"
    assert os.path.isfile(path), f"Path is not a file: {path}"

def test_fuzz_equivalence():
    agent_script = "/home/user/log_filter.py"
    oracle_script = "/verify/oracle_filter.py"

    assert os.path.exists(agent_script), "Agent script not found."
    assert os.path.exists(oracle_script), "Oracle script not found."

    fuzz_input = generate_fuzz_input(n=2000, seed=1337)

    # Run oracle
    oracle_proc = subprocess.run(
        [sys.executable, oracle_script],
        input=fuzz_input,
        text=True,
        capture_output=True,
        check=True
    )
    oracle_output = oracle_proc.stdout

    # Run agent
    agent_proc = subprocess.run(
        [sys.executable, agent_script],
        input=fuzz_input,
        text=True,
        capture_output=True
    )

    assert agent_proc.returncode == 0, f"Agent script failed with error:\n{agent_proc.stderr}"

    agent_output = agent_proc.stdout

    if oracle_output != agent_output:
        # Find the first differing line
        oracle_lines = oracle_output.splitlines()
        agent_lines = agent_output.splitlines()

        diff_idx = -1
        for i in range(max(len(oracle_lines), len(agent_lines))):
            o_line = oracle_lines[i] if i < len(oracle_lines) else "<EOF>"
            a_line = agent_lines[i] if i < len(agent_lines) else "<EOF>"
            if o_line != a_line:
                diff_idx = i
                break

        error_msg = (
            f"Output mismatch at line {diff_idx + 1}.\n"
            f"Expected (Oracle): {oracle_lines[diff_idx] if diff_idx < len(oracle_lines) else '<EOF>'}\n"
            f"Actual (Agent):   {agent_lines[diff_idx] if diff_idx < len(agent_lines) else '<EOF>'}\n"
        )
        pytest.fail(error_msg)