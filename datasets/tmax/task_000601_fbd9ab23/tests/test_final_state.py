# test_final_state.py

import os
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/log_packer"
AGENT_PATH = "/home/user/log_packer/target/release/log_packer"

def generate_random_string(length):
    chars = string.ascii_letters + string.digits + string.punctuation + " \n"
    return "".join(random.choice(chars) for _ in range(length))

def generate_fuzz_input():
    num_entries = random.randint(5, 50)
    entries = []
    prev_entry = ""

    for _ in range(num_entries):
        if prev_entry and random.random() < 0.5:
            prefix_len = int(len(prev_entry) * random.uniform(0.5, 0.9))
            prefix = prev_entry[:prefix_len]
            suffix_len = random.randint(10, 1000)
            entry = prefix + generate_random_string(suffix_len)
            # Ensure total length isn't too huge, cap to 1000 if needed, but the prompt says length bounded 10 to 1000. 
            # Let's just truncate to max 1000
            entry = entry[:1000]
            if len(entry) < 10:
                entry += generate_random_string(10 - len(entry))
        else:
            length = random.randint(10, 1000)
            entry = generate_random_string(length)

        # Ensure no accidental "===\n" in the entry itself to avoid messing up the delimiter logic
        entry = entry.replace("===\n", "== \n")

        entries.append(entry)
        prev_entry = entry

    return "".join(f"{entry}===\n" for entry in entries).encode('utf-8')

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary missing at {ORACLE_PATH}"
    assert os.path.exists(AGENT_PATH), f"Agent binary missing at {AGENT_PATH}. Did you compile in release mode?"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary at {AGENT_PATH} is not executable."

    random.seed(42)
    N = 1000

    for i in range(N):
        fuzz_input = generate_fuzz_input()

        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=fuzz_input,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i}"

        agent_proc = subprocess.run(
            [AGENT_PATH],
            input=fuzz_input,
            capture_output=True
        )

        if agent_proc.returncode != 0:
            pytest.fail(f"Agent program crashed or returned non-zero exit code on iteration {i}.\nStderr: {agent_proc.stderr.decode('utf-8', errors='replace')}")

        if oracle_proc.stdout != agent_proc.stdout:
            # To avoid massive output, truncate the hex dumps if they are huge
            oracle_hex = oracle_proc.stdout.hex()
            agent_hex = agent_proc.stdout.hex()

            oracle_disp = oracle_hex[:200] + ("..." if len(oracle_hex) > 200 else "")
            agent_disp = agent_hex[:200] + ("..." if len(agent_hex) > 200 else "")

            pytest.fail(
                f"Output mismatch on iteration {i}.\n"
                f"Input length: {len(fuzz_input)} bytes\n"
                f"Oracle output (hex): {oracle_disp}\n"
                f"Agent output (hex):  {agent_disp}\n"
            )