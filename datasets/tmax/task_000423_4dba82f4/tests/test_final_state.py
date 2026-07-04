# test_final_state.py

import os
import subprocess
import random
import string
import pytest

def test_fping_build():
    binary_path = '/app/fping-5.1/src/fping'
    assert os.path.isfile(binary_path), f"fping binary not found at {binary_path}. Did you compile it?"
    assert os.access(binary_path, os.X_OK), f"fping binary at {binary_path} is not executable."

    result = subprocess.run([binary_path, '-v'], capture_output=True, text=True)
    assert result.returncode == 0, f"fping -v failed with exit code {result.returncode}. Stderr: {result.stderr}"

    output = result.stdout + result.stderr
    assert "fping: Version 5.1" in output, f"Output does not contain 'fping: Version 5.1'. Output was:\n{output}"

def generate_fuzz_input():
    lines = []
    num_lines = random.randint(10, 500)
    for _ in range(num_lines):
        choice = random.choice(['garbage', 'valid_ipv4', 'valid_ipv6', 'interactive', 'ansi'])
        if choice == 'garbage':
            lines.append(''.join(random.choices(string.ascii_letters + string.digits + ' \t', k=random.randint(5, 50))) + '\n')
        elif choice == 'interactive':
            prefix = ''.join(random.choices(string.ascii_letters, k=5))
            lines.append(f"{prefix}interactive-prompt> " + ''.join(random.choices(string.ascii_letters, k=10)) + '\n')
        elif choice == 'valid_ipv4':
            ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
            loss = random.randint(0, 100)
            xmt = random.randint(10, 100)
            rcv = xmt - int(xmt * loss / 100)
            lines.append(f"{ip} : xmt/rcv/%loss = {xmt}/{rcv}/{loss}%\n")
        elif choice == 'valid_ipv6':
            ip = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
            loss = random.randint(0, 100)
            lines.append(f"{ip} : xmt/rcv/%loss = 100/100/{loss}%\n")
        elif choice == 'ansi':
            ip = f"10.0.0.{random.randint(1,255)}"
            loss = random.randint(0, 100)
            line = f"{ip} : xmt/rcv/%loss = 50/50/{loss}%\n"
            lines.append(f"\033[31m{line}\033[0m")
    return "".join(lines)

def test_uptime_parser_fuzz_equivalence():
    agent_path = '/home/user/uptime_parser'
    oracle_path = '/opt/oracle/uptime_parser_oracle.py'

    assert os.path.isfile(agent_path), f"Agent script not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent script at {agent_path} is not executable."
    assert os.path.isfile(oracle_path), f"Oracle script missing at {oracle_path}."

    random.seed(42)

    # Run 500 fuzz iterations to ensure robust equivalence
    for i in range(500):
        input_data = generate_fuzz_input()

        oracle_result = subprocess.run([oracle_path], input=input_data, capture_output=True, text=True)
        assert oracle_result.returncode == 0, "Oracle script failed unexpectedly."

        agent_result = subprocess.run([agent_path], input=input_data, capture_output=True, text=True)

        assert agent_result.returncode == 0, f"Agent script failed with exit code {agent_result.returncode} on fuzz input {i}.\nStderr: {agent_result.stderr}"

        if agent_result.stdout != oracle_result.stdout:
            pytest.fail(
                f"Mismatch on fuzz input stream {i}.\n"
                f"--- Input ---\n{input_data}\n"
                f"--- Expected Output (Oracle) ---\n{oracle_result.stdout}\n"
                f"--- Actual Output (Agent) ---\n{agent_result.stdout}"
            )