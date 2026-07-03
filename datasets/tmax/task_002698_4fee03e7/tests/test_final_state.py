# test_final_state.py
import os
import subprocess
import random
import string
import pytest

ORACLE_PATH = "/app/legacy_redactor"
AGENT_PATH = "/home/user/redactor.py"
NUM_ITERATIONS = 5000

TRIGGERS = [
    "password=",
    "token=",
    "-----BEGIN RSA PRIVATE KEY-----",
    "-----END RSA PRIVATE KEY-----",
    "sudo su",
    "chmod +s",
    "password=supersecret ",
    "token=1234567890abcdef\n",
    "-----BEGIN RSA PRIVATE KEY-----\nMIICXQIBAAKBgQC\n-----END RSA PRIVATE KEY-----"
]

def generate_random_input(seed):
    random.seed(seed)
    length = random.randint(50, 2000)
    chars = string.ascii_letters + string.digits + string.punctuation + " \t\n"

    # Generate base random string
    res = "".join(random.choices(chars, k=length))

    # Inject random triggers to ensure code paths are hit
    num_triggers = random.randint(0, 5)
    for _ in range(num_triggers):
        trigger = random.choice(TRIGGERS)
        insert_pos = random.randint(0, len(res))
        res = res[:insert_pos] + trigger + res[insert_pos:]

    return res

def test_agent_exists_and_executable():
    assert os.path.exists(AGENT_PATH), f"Agent script {AGENT_PATH} does not exist."
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a regular file."
    assert os.access(AGENT_PATH, os.X_OK), f"{AGENT_PATH} is not executable. Did you forget to run chmod +x?"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle {ORACLE_PATH} is missing."
    assert os.path.exists(AGENT_PATH), f"Agent {AGENT_PATH} is missing."

    for i in range(NUM_ITERATIONS):
        inp = generate_random_input(i)

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [ORACLE_PATH],
                input=inp,
                capture_output=True,
                text=True,
                timeout=2
            )
            oracle_out = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on iteration {i}.")

        # Run agent
        try:
            agent_proc = subprocess.run(
                [AGENT_PATH],
                input=inp,
                capture_output=True,
                text=True,
                timeout=2
            )
            agent_out = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on iteration {i}.")

        if agent_proc.returncode != oracle_proc.returncode:
            pytest.fail(
                f"Return code mismatch on iteration {i}.\n"
                f"Oracle exited with {oracle_proc.returncode}, Agent exited with {agent_proc.returncode}.\n"
                f"Input:\n{inp!r}"
            )

        if oracle_out != agent_out:
            pytest.fail(
                f"Output mismatch on iteration {i}.\n"
                f"Input:\n{inp!r}\n"
                f"Oracle Output:\n{oracle_out!r}\n"
                f"Agent Output:\n{agent_out!r}"
            )