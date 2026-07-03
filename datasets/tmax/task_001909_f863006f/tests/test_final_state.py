# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def generate_random_log(num_records):
    levels = ["INFO", "WARN", "ERROR", "TRACE"]
    log_bytes = bytearray()
    for _ in range(num_records):
        year = random.randint(2000, 2025)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        sec = random.randint(0, 59)
        level = random.choice(levels)

        header = f"[{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{sec:02d}] [{level}]\n"
        log_bytes.extend(header.encode("utf-8"))

        num_lines = random.randint(1, 10)
        for _ in range(num_lines):
            line_len = random.randint(10, 50)
            # Mix of ASCII and ISO-8859-1 characters (e.g., accented characters)
            line = "".join(random.choice(string.ascii_letters + string.digits + " \t.,;:'\"!?\xC0\xC1\xC2\xC3\xC4\xC5\xE0\xE1\xE2\xE3\xE4\xE5") for _ in range(line_len))
            log_bytes.extend(line.encode("iso-8859-1"))
            log_bytes.extend(b"\n")

    return bytes(log_bytes)

def test_agent_script_exists():
    assert os.path.isfile("/home/user/log_filter.py"), "Agent script /home/user/log_filter.py is missing."

def test_fuzz_equivalence():
    agent_script = "/home/user/log_filter.py"
    oracle_script = "/opt/oracle/log_filter_oracle.py"

    assert os.path.isfile(agent_script), "Agent script not found."
    assert os.path.isfile(oracle_script), "Oracle script not found."

    random.seed(42)

    for i in range(100):
        num_records = random.randint(5, 50)
        input_data = generate_random_log(num_records)

        # Run oracle
        oracle_proc = subprocess.run(
            ["python3", oracle_script],
            input=input_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on test case {i}:\n{oracle_proc.stderr.decode(errors='replace')}"
        oracle_out = oracle_proc.stdout

        # Run agent
        # The agent script might need to be run as an executable or via python
        if os.access(agent_script, os.X_OK):
            cmd = [agent_script]
        else:
            cmd = ["python3", agent_script]

        agent_proc = subprocess.run(
            cmd,
            input=input_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        assert agent_proc.returncode == 0, f"Agent script failed on test case {i}:\n{agent_proc.stderr.decode(errors='replace')}"
        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            input_preview = input_data[:200].decode(errors="replace")
            oracle_preview = oracle_out[:200].decode(errors="replace")
            agent_preview = agent_out[:200].decode(errors="replace")
            pytest.fail(
                f"Mismatch on test case {i}.\n"
                f"Input preview:\n{input_preview}...\n\n"
                f"Expected output preview:\n{oracle_preview}...\n\n"
                f"Agent output preview:\n{agent_preview}..."
            )