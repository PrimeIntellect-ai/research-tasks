# test_final_state.py
import os
import subprocess
import random
import string
import pytest

ORACLE_PATH = "/app/bin/query_formatter"
AGENT_PATH = "/home/user/formatter.sh"

def generate_random_input(seed):
    random.seed(seed)
    num_lines = random.randint(1, 10)
    lines = []
    for _ in range(num_lines):
        num_fields = random.randint(2, 6)
        fields = []
        for _ in range(num_fields):
            field_len = random.randint(1, 15)
            field = ''.join(random.choices(string.ascii_letters + string.digits, k=field_len))
            fields.append(field)
        lines.append("|".join(fields))
    return "\n".join(lines) + "\n"

def test_agent_script_exists_and_executable():
    assert os.path.exists(AGENT_PATH), f"Agent script not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"{AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle not executable at {ORACLE_PATH}"

    for i in range(100):
        input_data = generate_random_input(seed=42 + i)

        # Run oracle
        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=input_data,
            text=True,
            capture_output=True,
            check=True
        )
        oracle_output = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            [AGENT_PATH],
            input=input_data,
            text=True,
            capture_output=True
        )

        assert agent_proc.returncode == 0, f"Agent script failed with return code {agent_proc.returncode}\nStderr: {agent_proc.stderr}"

        agent_output = agent_proc.stdout

        if oracle_output != agent_output:
            pytest.fail(
                f"Output mismatch on run {i+1}!\n"
                f"Input:\n{input_data}\n"
                f"Expected (Oracle):\n{oracle_output}\n"
                f"Got (Agent):\n{agent_output}"
            )