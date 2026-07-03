# test_final_state.py
import os
import random
import string
import subprocess
import urllib.parse
import pytest

ORACLE_PATH = "/app/oracle_investigate"
AGENT_PATH = "/home/user/investigate"
NUM_TESTS = 1000

def generate_random_query_string():
    parts = []
    has_payload = random.random() > 0.2
    num_params = random.randint(1, 10)

    def random_string(length):
        chars = string.ascii_letters + string.digits + "+ <>%"
        res = []
        for c in random.choices(chars, k=length):
            if c == ' ':
                res.append(random.choice(['+', '%20']))
            elif c == '<':
                res.append('%3C')
            elif c == '>':
                res.append('%3E')
            elif c == '%':
                res.append('%25')
            else:
                res.append(c)
        return "".join(res)

    for _ in range(num_params):
        k = random_string(random.randint(1, 10))
        v = random_string(random.randint(1, 20))
        if k.lower() == 'payload':
            k = 'not_payload'
        parts.append(f"{k}={v}")

    if has_payload:
        v = random_string(random.randint(1, 50))
        parts.append(f"payload={v}")

    random.shuffle(parts)
    query = "&".join(parts)

    # Pad or truncate to fit length constraints (10 to 500)
    if len(query) < 10:
        query += "&pad=" + random_string(10 - len(query))
    if len(query) > 500:
        query = query[:500]

    return query

def test_agent_executable_exists():
    assert os.path.isfile(AGENT_PATH), f"Agent binary {AGENT_PATH} is missing. Did you compile your Go program?"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary {AGENT_PATH} is not executable."

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle binary {ORACLE_PATH} is missing."
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary {ORACLE_PATH} is not executable."

    random.seed(42)

    for i in range(NUM_TESTS):
        input_data = generate_random_query_string().encode('utf-8')

        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=input_data,
            capture_output=True
        )
        oracle_out = oracle_proc.stdout

        agent_proc = subprocess.run(
            [AGENT_PATH],
            input=input_data,
            capture_output=True
        )
        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            error_msg = (
                f"Fuzz equivalence failed on test {i+1}/{NUM_TESTS}.\n"
                f"Input (hex): {input_data.hex()}\n"
                f"Input (repr): {repr(input_data)}\n"
                f"Oracle output: {repr(oracle_out)}\n"
                f"Agent output: {repr(agent_out)}\n"
            )
            pytest.fail(error_msg)