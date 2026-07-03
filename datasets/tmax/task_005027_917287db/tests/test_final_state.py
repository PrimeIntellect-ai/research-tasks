# test_final_state.py
import os
import subprocess
import random
import string
import pytest

ORACLE_PATH = "/app/oracle"
AGENT_PATH = "/home/user/cleaner"

def generate_random_csv(num_lines=5000):
    lines = []
    domains = [".edu", ".com", ".org", ".net", ".io"]
    for _ in range(num_lines):
        # 10% chance of malformed line
        if random.random() < 0.1:
            if random.random() < 0.5:
                # Missing columns
                lines.append(f"{random.randint(1609459200, 1700000000)},{random.randint(1, 10000)}")
            else:
                # Extra columns
                lines.append(f"{random.randint(1609459200, 1700000000)},{random.randint(1, 10000)},a@b.com,1.23,extra")
            continue

        timestamp = random.randint(1609459200, 1700000000)
        user_id = random.randint(1, 1000000)

        # Email
        user_len = random.randint(1, 10)
        user_part = "".join(random.choices(string.ascii_lowercase, k=user_len))
        domain_len = random.randint(3, 8)
        domain_part = "".join(random.choices(string.ascii_lowercase, k=domain_len))
        tld = random.choice(domains)

        # 5% chance of invalid email (no @)
        if random.random() < 0.05:
            email = f"{user_part}{domain_part}{tld}"
        else:
            email = f"{user_part}@{domain_part}{tld}"

        value = random.uniform(-1000.0, 1000.0)
        lines.append(f"{timestamp},{user_id},{email},{value:.4f}")

    return "\n".join(lines) + "\n"

def test_agent_executable_exists():
    assert os.path.isfile(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent executable at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle not found at {ORACLE_PATH}"

    random.seed(42)

    for i in range(10):
        input_data = generate_random_csv(5000)

        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=input_data,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, "Oracle failed to run"

        agent_proc = subprocess.run(
            [AGENT_PATH],
            input=input_data,
            text=True,
            capture_output=True
        )
        assert agent_proc.returncode == 0, "Agent program failed to run"

        if oracle_proc.stdout != agent_proc.stdout:
            # Find the first differing line
            oracle_lines = oracle_proc.stdout.splitlines()
            agent_lines = agent_proc.stdout.splitlines()

            error_msg = f"Mismatch in round {i+1}:\n"
            for j, (oline, aline) in enumerate(zip(oracle_lines, agent_lines)):
                if oline != aline:
                    error_msg += f"Line {j+1}:\nOracle: {oline}\nAgent:  {aline}\n"
                    break
            if len(oracle_lines) != len(agent_lines):
                error_msg += f"Line counts differ: Oracle={len(oracle_lines)}, Agent={len(agent_lines)}\n"
            pytest.fail(error_msg)