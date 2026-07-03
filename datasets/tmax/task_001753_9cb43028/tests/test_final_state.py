# test_final_state.py

import os
import subprocess
import random
import string
import pytest

def test_makefile_fixed():
    path = "/app/loc-processor-1.0.0/Makefile"
    assert os.path.isfile(path), f"Makefile {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "-DFAIL_DEDUP=1" not in content, "Makefile still contains the deliberate perturbation -DFAIL_DEDUP=1."

    objs_lines = [line for line in content.splitlines() if line.strip().startswith("OBJS")]
    if objs_lines:
        assert "join.o" in objs_lines[0], "Makefile OBJS variable does not include join.o."

def test_agent_executable_exists():
    path = "/home/user/format_translations"
    assert os.path.isfile(path), f"Agent executable {path} does not exist. Did you compile format_translations.c?"
    assert os.access(path, os.X_OK), f"Agent program {path} is not executable."

def generate_random_csv_input(num_rows):
    lines = []
    for _ in range(num_rows):
        year = random.randint(2000, 2025)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        timestamp = f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}"

        # Sometimes generate invalid timestamps
        if random.random() < 0.05:
            timestamp = "invalid_timestamp"

        key = "".join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 15)))

        langs = []
        for _ in range(3):
            if random.random() < 0.3:
                # Missing value
                langs.append("")
            else:
                # Random string without comma or newline
                chars = string.ascii_letters + string.digits + " .!?-+"
                langs.append("".join(random.choices(chars, k=random.randint(1, 30))))

        row = f"{timestamp},{key},{langs[0]},{langs[1]},{langs[2]}"
        lines.append(row)
    return "\n".join(lines) + "\n"

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_formatter"
    agent_path = "/home/user/format_translations"

    assert os.path.isfile(oracle_path), f"Oracle program {oracle_path} missing."
    assert os.path.isfile(agent_path), f"Agent program {agent_path} missing."

    random.seed(42)

    for i in range(1000):
        num_rows = random.randint(1, 20)
        csv_input = generate_random_csv_input(num_rows)

        oracle_proc = subprocess.run([oracle_path], input=csv_input.encode("utf-8"), capture_output=True)
        agent_proc = subprocess.run([agent_path], input=csv_input.encode("utf-8"), capture_output=True)

        oracle_out = oracle_proc.stdout.decode("utf-8", errors="replace")
        agent_out = agent_proc.stdout.decode("utf-8", errors="replace")

        if oracle_out != agent_out:
            pytest.fail(
                f"Output mismatch on fuzz iteration {i}.\n"
                f"Input CSV:\n{csv_input}\n"
                f"Expected Output (Oracle):\n{oracle_out}\n"
                f"Actual Output (Agent):\n{agent_out}\n"
            )