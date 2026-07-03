# test_final_state.py

import os
import random
import subprocess
import string
import pytest

def generate_random_string(length):
    # ASCII letters, digits, and some safe punctuation
    chars = string.ascii_letters + string.digits + " !@#$%^&*()_+-=[]{}|;:'\"<>.?/~`"
    # Add some Unicode ranges (Hiragana and Latin-1 Supplement)
    chars += "".join(chr(i) for i in range(0x3041, 0x3096))
    chars += "".join(chr(i) for i in range(0x00C0, 0x00FF))
    # Ensure no commas or newlines are included
    chars = chars.replace(",", "").replace("\n", "").replace("\r", "")
    return "".join(random.choice(chars) for _ in range(length))

def generate_csv_row():
    # 6 fields per row, length 1 to 50
    fields = [generate_random_string(random.randint(1, 50)) for _ in range(6)]
    return ",".join(fields)

def test_fuzz_equivalence():
    agent_script = "/home/user/new_loc_scorer.py"
    oracle_binary = "/app/legacy_loc_scorer"

    assert os.path.exists(agent_script), f"Agent script not found at {agent_script}"
    assert os.path.exists(oracle_binary), f"Oracle binary not found at {oracle_binary}"

    random.seed(42)
    # Generate N=10,000 CSV rows
    input_lines = [generate_csv_row() for _ in range(10000)]
    input_data = "\n".join(input_lines) + "\n"
    input_bytes = input_data.encode("utf-8")

    # Run oracle
    oracle_proc = subprocess.run(
        [oracle_binary],
        input=input_bytes,
        capture_output=True
    )
    assert oracle_proc.returncode == 0, f"Oracle failed to process input. Stderr: {oracle_proc.stderr.decode('utf-8', errors='replace')}"

    # Run agent
    agent_proc = subprocess.run(
        ["python3", agent_script],
        input=input_bytes,
        capture_output=True
    )

    if agent_proc.returncode != 0:
        pytest.fail(f"Agent script failed with return code {agent_proc.returncode}.\nStderr: {agent_proc.stderr.decode('utf-8', errors='replace')}")

    oracle_out = oracle_proc.stdout.decode("utf-8", errors="replace")
    agent_out = agent_proc.stdout.decode("utf-8", errors="replace")

    if oracle_out != agent_out:
        oracle_lines = oracle_out.splitlines()
        agent_lines = agent_out.splitlines()

        for i, (oline, aline) in enumerate(zip(oracle_lines, agent_lines)):
            if oline != aline:
                # Find the corresponding input row
                input_row_idx = i // 4
                input_row = input_lines[input_row_idx]
                pytest.fail(
                    f"Mismatch at output line {i+1} (Input row {input_row_idx+1}):\n"
                    f"Input : {input_row}\n"
                    f"Oracle: {oline}\n"
                    f"Agent : {aline}"
                )

        if len(oracle_lines) != len(agent_lines):
            pytest.fail(f"Output length mismatch: Oracle has {len(oracle_lines)} lines, Agent has {len(agent_lines)} lines.")