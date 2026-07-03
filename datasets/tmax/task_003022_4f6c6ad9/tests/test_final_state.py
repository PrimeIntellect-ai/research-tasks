# test_final_state.py

import os
import json
import random
import string
import subprocess
import pytest

AGENT_SCRIPT = "/home/user/auditor.py"
ORACLE_BINARY = "/app/audit_bin"

def generate_fuzz_input():
    nodes = [''.join(random.choices(string.ascii_uppercase, k=3)) for _ in range(10)]
    users = [''.join(random.choices(string.ascii_lowercase, k=4)) for _ in range(3)]
    ops = []

    # Add nodes
    for node in nodes:
        ops.append({"op": "add_node", "node": node, "is_sensitive": random.choice([True, False])})

    # Add edges
    for _ in range(15):
        ops.append({"op": "add_edge", "src": random.choice(nodes), "dst": random.choice(nodes)})

    # Grants
    for _ in range(10):
        ops.append({"op": "grant", "user": random.choice(users), "node": random.choice(nodes)})

    random.shuffle(ops)
    return json.dumps(ops)

def run_program(cmd, input_data):
    try:
        result = subprocess.run(
            cmd,
            input=input_data,
            text=True,
            capture_output=True,
            check=True,
            timeout=5
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"ERROR: Process exited with {e.returncode}\nStderr: {e.stderr}"
    except subprocess.TimeoutExpired:
        return "ERROR: Process timed out"

def test_auditor_script_exists():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"
    assert os.path.isfile(AGENT_SCRIPT), f"{AGENT_SCRIPT} is not a file"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_BINARY), f"Oracle binary missing at {ORACLE_BINARY}"
    assert os.access(ORACLE_BINARY, os.X_OK), f"Oracle binary not executable at {ORACLE_BINARY}"

    random.seed(42)  # Fixed seed for reproducibility

    for i in range(50):
        input_data = generate_fuzz_input()

        oracle_cmd = [ORACLE_BINARY]
        agent_cmd = ["python3", AGENT_SCRIPT]

        oracle_out = run_program(oracle_cmd, input_data)
        agent_out = run_program(agent_cmd, input_data)

        if oracle_out != agent_out:
            error_msg = (
                f"Mismatch on fuzz iteration {i+1}!\n"
                f"Input:\n{input_data}\n\n"
                f"Expected (Oracle):\n{oracle_out}\n\n"
                f"Actual (Agent):\n{agent_out}"
            )
            pytest.fail(error_msg)