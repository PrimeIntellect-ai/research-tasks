# test_final_state.py

import os
import random
import subprocess
import tempfile
import pytest

ORACLE_PATH = "/app/legacy_config_gen"
AGENT_PATH = "/home/user/new_config_gen"
NUM_TESTS = 100

def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

def generate_random_input(num_lines):
    lines = []
    for _ in range(num_lines):
        choice = random.choice(["empty", "comment", "allow", "block"])
        if choice == "empty":
            lines.append("")
        elif choice == "comment":
            lines.append(f"# random comment {random.randint(1, 1000)}")
        elif choice == "allow":
            ip = generate_random_ip()
            p1 = random.randint(1, 30000)
            p2 = random.randint(p1, 65535)
            lines.append(f"ALLOW {ip} {p1}-{p2}")
        elif choice == "block":
            ip = generate_random_ip()
            p = random.randint(1, 65535)
            lines.append(f"BLOCK {ip} {p}")
    return "\n".join(lines) + "\n"

def test_agent_program_exists():
    assert os.path.exists(AGENT_PATH), f"Agent's program not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"{AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle program not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle program {ORACLE_PATH} is not executable"

    random.seed(42)

    for i in range(NUM_TESTS):
        num_lines = random.randint(1, 50)
        input_content = generate_random_input(num_lines)

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write(input_content)
            tmp_path = tmp.name

        try:
            oracle_result = subprocess.run([ORACLE_PATH, tmp_path], capture_output=True, text=True)
            agent_result = subprocess.run([AGENT_PATH, tmp_path], capture_output=True, text=True)

            assert oracle_result.returncode == agent_result.returncode, f"Return code mismatch on input:\n{input_content}\nOracle: {oracle_result.returncode}, Agent: {agent_result.returncode}"
            assert oracle_result.stdout == agent_result.stdout, f"Stdout mismatch on input:\n{input_content}\nOracle output:\n{oracle_result.stdout}\nAgent output:\n{agent_result.stdout}"
        finally:
            os.remove(tmp_path)