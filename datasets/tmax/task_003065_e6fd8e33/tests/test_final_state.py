# test_final_state.py
import os
import random
import string
import subprocess
import pytest

def test_executable_exists():
    """Check that the compiled executable exists at the required location."""
    agent_path = "/home/user/processor"
    assert os.path.isfile(agent_path), f"{agent_path} does not exist. Did you copy the compiled binary?"
    assert os.access(agent_path, os.X_OK), f"{agent_path} is not executable."

def test_fuzz_equivalence():
    """Fuzz the agent's executable against the oracle to ensure absolute bit-exact equivalence."""
    random.seed(42)
    oracle_path = "/opt/oracle/processor_oracle"
    agent_path = "/home/user/processor"

    assert os.path.isfile(oracle_path), "Oracle missing at /opt/oracle/processor_oracle"
    assert os.path.isfile(agent_path), "Agent executable missing at /home/user/processor"

    non_ascii_pool = "áéíóúñüçøæå你好世界こんにちは😂🔥👍"
    ascii_pool = [chr(c) for c in range(32, 127) if c != 44]  # ASCII 32-126 excluding comma (44)

    for i in range(1000):
        num_lines = random.randint(1, 50)
        lines = []
        for _ in range(num_lines):
            ts = str(random.randint(1000000000, 2000000000))
            uid = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 15)))
            x = f"{random.uniform(-1000.0, 1000.0):.6f}"
            y = f"{random.uniform(-1000.0, 1000.0):.6f}"

            notes_len = random.randint(0, 50)
            notes_chars = random.choices(ascii_pool, k=notes_len)

            # 50% chance to include a non-ASCII character
            if random.random() < 0.5 and notes_len > 0:
                notes_chars[random.randint(0, notes_len - 1)] = random.choice(non_ascii_pool)

            notes = ''.join(notes_chars)
            lines.append(f"{ts},{uid},{x},{y},{notes}")

        csv_input = "\n".join(lines) + "\n"
        input_bytes = csv_input.encode('utf-8')

        oracle_proc = subprocess.run([oracle_path], input=input_bytes, capture_output=True)
        agent_proc = subprocess.run([agent_path], input=input_bytes, capture_output=True)

        assert oracle_proc.returncode == agent_proc.returncode, (
            f"Return code mismatch on input:\n{csv_input}\n"
            f"Oracle returned {oracle_proc.returncode}, Agent returned {agent_proc.returncode}"
        )

        assert oracle_proc.stdout == agent_proc.stdout, (
            f"Stdout mismatch on input:\n{csv_input}\n"
            f"Oracle Output:\n{oracle_proc.stdout.decode('utf-8', errors='replace')}\n"
            f"Agent Output:\n{agent_proc.stdout.decode('utf-8', errors='replace')}"
        )