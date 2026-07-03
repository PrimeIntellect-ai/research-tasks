# test_final_state.py
import os
import random
import string
import subprocess
import pytest

AGENT_VERIFIER = "/home/user/verifier"
ORACLE_VERIFIER = "/app/oracle_verifier_new_salt"
N_TESTS = 1000

def generate_random_input():
    length = random.randint(1, 100)
    chars = string.printable
    base_str = "".join(random.choice(chars) for _ in range(length))

    # Inject payloads randomly to ensure sanitization logic is tested
    if random.random() < 0.3:
        insert_pos = random.randint(0, len(base_str))
        base_str = base_str[:insert_pos] + "' OR '1'='1" + base_str[insert_pos:]
    if random.random() < 0.3:
        insert_pos = random.randint(0, len(base_str))
        base_str = base_str[:insert_pos] + "<script>" + base_str[insert_pos:]

    return base_str[:100] if len(base_str) > 100 else base_str

def test_verifier_exists_and_executable():
    assert os.path.isfile(AGENT_VERIFIER), f"Agent verifier not found at {AGENT_VERIFIER}"
    assert os.access(AGENT_VERIFIER, os.X_OK), f"Agent verifier at {AGENT_VERIFIER} is not executable"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_VERIFIER), f"Oracle verifier missing at {ORACLE_VERIFIER}"
    assert os.access(ORACLE_VERIFIER, os.X_OK), f"Oracle verifier not executable"

    random.seed(42)

    for i in range(N_TESTS):
        test_input = generate_random_input()

        # Run oracle
        try:
            oracle_res = subprocess.run(
                [ORACLE_VERIFIER, test_input],
                capture_output=True,
                text=True,
                timeout=2,
                check=True
            )
            oracle_output = oracle_res.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {repr(test_input)}: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input {repr(test_input)}")

        # Run agent
        try:
            agent_res = subprocess.run(
                [AGENT_VERIFIER, test_input],
                capture_output=True,
                text=True,
                timeout=2
            )
            agent_output = agent_res.stdout

            if agent_res.returncode != 0:
                pytest.fail(f"Agent verifier failed with code {agent_res.returncode} on input {repr(test_input)}\nStderr: {agent_res.stderr}")

        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent verifier timed out on input {repr(test_input)}")

        assert agent_output == oracle_output, (
            f"Mismatch on input {repr(test_input)}.\n"
            f"Expected (Oracle): {repr(oracle_output)}\n"
            f"Got (Agent): {repr(agent_output)}"
        )