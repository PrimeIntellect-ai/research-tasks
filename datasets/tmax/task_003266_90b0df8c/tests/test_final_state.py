# test_final_state.py
import os
import subprocess
import random
import string
import pytest

ORACLE_PATH = "/app/db_recover"
AGENT_PATH = "/home/user/recover.py"
NUM_ITERATIONS = 500

def generate_random_input(seed):
    random.seed(seed)
    num_lines = random.randint(10, 100)
    lines = []

    for _ in range(num_lines):
        tx_id = random.randint(1, 10000)
        local_ts = random.randint(1600000000, 1700000000)

        # Generate valid TZ offset
        sign = random.choice(['+', '-'])
        hh = random.randint(0, 14)
        if hh == 14:
            mm = 0
            sign = '+'
        elif hh == 12 and sign == '-':
            mm = 0
        else:
            mm = random.choice([0, 15, 30, 45])

        tz_offset = f"{sign}{hh:02d}{mm:02d}"

        operation = "SET" if random.random() < 0.8 else "DEL"

        key_len = random.randint(2, 5)
        key = ''.join(random.choices(string.ascii_letters + string.digits, k=key_len))

        val_len = random.randint(4, 8)
        value = ''.join(random.choices(string.ascii_letters + string.digits, k=val_len))

        line = f"{tx_id} {local_ts} {tz_offset} {operation} {key} {value}"
        lines.append(line)

    return "\n".join(lines) + "\n"

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
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"ERROR: {e.stderr}"
    except subprocess.TimeoutExpired:
        return "ERROR: Timeout"

def test_recover_script_exists():
    assert os.path.exists(AGENT_PATH), f"Agent script not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle {ORACLE_PATH} is not executable"

    for i in range(NUM_ITERATIONS):
        input_data = generate_random_input(seed=42 + i)

        oracle_output = run_program([ORACLE_PATH], input_data)
        agent_output = run_program(["python3", AGENT_PATH], input_data)

        if oracle_output != agent_output:
            error_msg = (
                f"Mismatch on iteration {i+1}!\n\n"
                f"INPUT:\n{input_data}\n"
                f"EXPECTED (Oracle):\n{oracle_output}\n"
                f"ACTUAL (Agent):\n{agent_output}\n"
            )
            pytest.fail(error_msg)