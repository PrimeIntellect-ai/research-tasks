# test_final_state.py
import os
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/csv_processor_oracle"
AGENT_PATH = "/home/user/csv_processor"
NUM_TESTS = 10000

def generate_random_input() -> str:
    id_val = "".join(random.choices(string.digits, k=random.randint(1, 5)))

    first_name_len = random.randint(3, 8)
    first_name = random.choice(string.ascii_uppercase) + "".join(random.choices(string.ascii_lowercase, k=first_name_len))

    last_name_len = random.randint(4, 10)
    last_name = random.choice(string.ascii_uppercase) + "".join(random.choices(string.ascii_lowercase, k=last_name_len))

    email_len = random.randint(5, 10)
    email_prefix = "".join(random.choices(string.ascii_lowercase, k=email_len))
    domain = random.choice(["gmail", "yahoo", "hotmail"])
    email = f"{email_prefix}@{domain}.com"

    phone = "".join(random.choices(string.digits, k=10))

    return f"{id_val},{first_name},{last_name},{email},{phone}\n"

def test_agent_executable_exists():
    assert os.path.exists(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"{AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle executable not found at {ORACLE_PATH}"
    assert os.path.exists(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}"

    random.seed(42)

    for _ in range(NUM_TESTS):
        input_data = generate_random_input()

        try:
            oracle_proc = subprocess.run(
                [ORACLE_PATH],
                input=input_data,
                text=True,
                capture_output=True,
                check=True,
                timeout=1
            )
            oracle_out = oracle_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {input_data.strip()}: {e.stderr}")

        try:
            agent_proc = subprocess.run(
                [AGENT_PATH],
                input=input_data,
                text=True,
                capture_output=True,
                check=True,
                timeout=1
            )
            agent_out = agent_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent failed on input {input_data.strip()}: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent timed out on input {input_data.strip()}")

        assert agent_out == oracle_out, (
            f"Mismatch on input: {input_data.strip()}\n"
            f"Expected (Oracle): {oracle_out!r}\n"
            f"Got (Agent):       {agent_out!r}"
        )