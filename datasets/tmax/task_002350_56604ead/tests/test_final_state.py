# test_final_state.py

import os
import sys
import subprocess
import random
import string
import uuid
import pytest

AGENT_SCRIPT = "/home/user/audit_processor.py"
ORACLE_BINARY = "/app/legacy_audit_tool"

def generate_random_string(min_len=5, max_len=10):
    length = random.randint(min_len, max_len)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_csv_input():
    num_lines = random.randint(50, 500)
    lines = ["EventID,Actor,Target,ActionType,SeverityScore"]
    action_types = ['READ', 'WRITE', 'DELETE', 'GRANT']

    # To ensure some target/actor overlap, let's create a pool of actors and targets
    actors_pool = [generate_random_string() for _ in range(random.randint(5, 20))]
    targets_pool = [generate_random_string() for _ in range(random.randint(5, 20))]

    for _ in range(num_lines):
        event_id = str(uuid.uuid4())
        actor = random.choice(actors_pool)
        target = random.choice(targets_pool)
        action = random.choice(action_types)
        severity = random.randint(1, 20)
        lines.append(f"{event_id},{actor},{target},{action},{severity}")

    return "\n".join(lines) + "\n"

def test_audit_processor_exists():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script missing at {AGENT_SCRIPT}"
    assert os.path.isfile(AGENT_SCRIPT), f"{AGENT_SCRIPT} is not a file"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_BINARY), f"Oracle binary missing at {ORACLE_BINARY}"

    random.seed(42)
    num_iterations = 100

    for i in range(num_iterations):
        csv_data = generate_csv_input()

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [ORACLE_BINARY],
                input=csv_data,
                text=True,
                capture_output=True,
                check=True,
                timeout=5
            )
            oracle_out = oracle_proc.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on iteration {i}. Stderr: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on iteration {i}.")

        # Run agent
        try:
            agent_proc = subprocess.run(
                [sys.executable, AGENT_SCRIPT],
                input=csv_data,
                text=True,
                capture_output=True,
                check=True,
                timeout=5
            )
            agent_out = agent_proc.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent script failed on iteration {i}. Stderr: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on iteration {i}.")

        assert agent_out == oracle_out, (
            f"Output mismatch on iteration {i}!\n\n"
            f"Input CSV:\n{csv_data}\n\n"
            f"Oracle output:\n{oracle_out}\n\n"
            f"Agent output:\n{agent_out}"
        )