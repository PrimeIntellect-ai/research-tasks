# test_final_state.py

import os
import subprocess
import random
import string
import pytest

ORACLE_PATH = "/app/conf_oracle"
AGENT_PATH = "/home/user/tracker/target/release/tracker"

def generate_random_input(seed):
    random.seed(seed)
    num_lines = random.randint(1, 50)
    lines = []

    # Mix of ascii, combining characters, emojis, etc.
    chars = string.ascii_letters + string.digits + " \t!@#$%^&*()_+"
    combining = [chr(c) for c in range(0x0300, 0x036F)]
    emojis = ["😀", "🚀", "👨‍👩‍👧‍👦", "ñ", "é", "ç", "ü"]

    for _ in range(num_lines):
        key_len = random.randint(2, 5)
        key = "".join(random.choices(string.ascii_letters + string.digits, k=key_len))

        payload_len = random.randint(1, 100)
        payload_chars = []
        for _ in range(payload_len):
            choice = random.random()
            if choice < 0.7:
                payload_chars.append(random.choice(chars))
            elif choice < 0.9:
                payload_chars.append(random.choice(emojis))
            else:
                # Add a base char and a combining mark
                payload_chars.append(random.choice(string.ascii_letters) + random.choice(combining))

        payload = "".join(payload_chars)
        # Ensure we don't have newlines in the payload
        payload = payload.replace("\n", " ")
        lines.append(f"{key} {payload}")

    return "\n".join(lines) + "\n"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"
    assert os.path.exists(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}. Did you compile it in release mode?"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary at {AGENT_PATH} is not executable."

    # Fuzz 500 iterations
    for i in range(500):
        test_input = generate_random_input(i + 42)

        # Run oracle
        proc_oracle = subprocess.run(
            [ORACLE_PATH],
            input=test_input.encode("utf-8"),
            capture_output=True
        )
        oracle_out = proc_oracle.stdout

        # Run agent
        proc_agent = subprocess.run(
            [AGENT_PATH],
            input=test_input.encode("utf-8"),
            capture_output=True
        )
        agent_out = proc_agent.stdout

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on iteration {i}.\n"
                f"--- Input ---\n{test_input}\n"
                f"--- Oracle Output ---\n{oracle_out.decode('utf-8', errors='replace')}\n"
                f"--- Agent Output ---\n{agent_out.decode('utf-8', errors='replace')}\n"
            )