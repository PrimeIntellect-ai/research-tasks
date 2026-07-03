# test_final_state.py

import os
import random
import subprocess
import string
import pytest

AGENT_SCRIPT = "/home/user/analyze.sh"
ORACLE_SCRIPT = "/opt/oracle.sh"

def generate_fuzz_input(seed):
    random.seed(seed)
    num_lines = random.randint(10, 500)
    lines = []
    for _ in range(num_lines):
        timestamp = random.randint(1600000000, 1800000000)

        if random.random() < 0.2:
            value_str = "null"
        else:
            value_str = f"{random.uniform(-500.0, 500.0):.4f}"

        # Generate some invalid unicode escapes
        bad_escapes = [f"\\u{random.choice(string.ascii_uppercase)}{random.randint(100, 999)}", 
                       f"\\u00X{random.randint(0,9)}", 
                       "\\uZZZZ"]
        msg_chars = "".join(random.choices(string.ascii_letters + " ", k=10))
        msg = f"{msg_chars} {random.choice(bad_escapes)}"

        line = f'{{"timestamp": {timestamp}, "value": {value_str}, "message": "{msg}"}}'
        lines.append(line)

    return "\n".join(lines) + "\n"

def test_analyze_script_exists_and_executable():
    assert os.path.isfile(AGENT_SCRIPT), f"{AGENT_SCRIPT} does not exist."
    assert os.access(AGENT_SCRIPT, os.X_OK), f"{AGENT_SCRIPT} is not executable."

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_SCRIPT), f"Oracle script {ORACLE_SCRIPT} missing."

    for i in range(50):
        test_input = generate_fuzz_input(seed=42 + i)

        # Run agent
        agent_proc = subprocess.run(
            [AGENT_SCRIPT],
            input=test_input,
            text=True,
            capture_output=True
        )

        # Run oracle
        oracle_proc = subprocess.run(
            [ORACLE_SCRIPT],
            input=test_input,
            text=True,
            capture_output=True
        )

        assert agent_proc.returncode == 0, f"Agent script failed with return code {agent_proc.returncode}\nStderr: {agent_proc.stderr}"

        agent_out = agent_proc.stdout.strip()
        oracle_out = oracle_proc.stdout.strip()

        if agent_out != oracle_out:
            pytest.fail(
                f"Mismatch on fuzz test {i+1}/50.\n"
                f"Input (first 3 lines):\n{chr(10).join(test_input.split(chr(10))[:3])}\n...\n"
                f"Oracle output: {oracle_out}\n"
                f"Agent output: {agent_out}"
            )