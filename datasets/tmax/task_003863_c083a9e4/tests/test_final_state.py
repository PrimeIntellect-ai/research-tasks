# test_final_state.py

import os
import subprocess
import random
import string
import pytest

AGENT_SCRIPT = "/home/user/archive_filter.sh"
ORACLE_SCRIPT = "/app/oracle_archive_filter"

def test_agent_script_exists_and_executable():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script missing at {AGENT_SCRIPT}"
    assert os.access(AGENT_SCRIPT, os.X_OK), f"Agent script at {AGENT_SCRIPT} is not executable"

def generate_random_line():
    length = random.randint(5, 50)
    chars = string.ascii_letters + string.digits + " _-./"
    path = "".join(random.choice(chars) for _ in range(length))

    # Increase chances of hitting edge cases
    if random.random() < 0.5:
        path += random.choice([".log", ".bak", ".txt", ".csv"])
    if random.random() < 0.5:
        path = random.choice(["/var/tmp/", "/tmp/", "/home/user/", "/var/log/"]) + path

    size = random.randint(0, 10 * 1024**3)
    if random.random() < 0.5:
        size = random.randint(50000000, 60000000) # Around 50MB

    timestamp = random.randint(1500000000, 1700000000)

    return f"{path} {size} {timestamp}"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_SCRIPT), f"Oracle missing at {ORACLE_SCRIPT}"
    assert os.access(ORACLE_SCRIPT, os.X_OK), f"Oracle at {ORACLE_SCRIPT} is not executable"

    random.seed(42)

    # N=100 iterations, each with 1000 lines
    for i in range(100):
        lines = [generate_random_line() for _ in range(100)]
        input_data = "\n".join(lines) + "\n"

        oracle_proc = subprocess.run(
            [ORACLE_SCRIPT],
            input=input_data,
            text=True,
            capture_output=True
        )
        oracle_out = oracle_proc.stdout

        agent_proc = subprocess.run(
            [AGENT_SCRIPT],
            input=input_data,
            text=True,
            capture_output=True
        )
        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            # Find the first differing line for a better error message
            oracle_lines = oracle_out.splitlines()
            agent_lines = agent_out.splitlines()

            error_msg = f"Mismatch on iteration {i+1}.\n"
            error_msg += f"Oracle output lines: {len(oracle_lines)}, Agent output lines: {len(agent_lines)}\n"

            for j, (o_line, a_line) in enumerate(zip(oracle_lines, agent_lines)):
                if o_line != a_line:
                    error_msg += f"First difference at output line {j+1}:\n"
                    error_msg += f"Oracle: {o_line}\n"
                    error_msg += f"Agent:  {a_line}\n"
                    break
            else:
                if len(oracle_lines) > len(agent_lines):
                    error_msg += f"Agent is missing output line: {oracle_lines[len(agent_lines)]}\n"
                elif len(agent_lines) > len(oracle_lines):
                    error_msg += f"Agent has extra output line: {agent_lines[len(oracle_lines)]}\n"

            pytest.fail(error_msg)