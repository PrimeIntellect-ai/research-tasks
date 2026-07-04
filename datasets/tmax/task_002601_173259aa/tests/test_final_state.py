# test_final_state.py

import os
import json
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/usr/local/bin/oracle_parse_fuzz.py"
AGENT_PATH = "/home/user/parse_fuzz.py"
NUM_TESTS = 1000
TIMEOUT_SECS = 2.0

def generate_random_json_value(depth=0):
    if depth > 3:
        return random.choice([None, True, False, random.randint(-1000, 1000), "".join(random.choices(string.ascii_letters, k=5))])

    val_type = random.choice(['dict', 'list', 'int', 'string', 'bool', 'null'])
    if val_type == 'dict':
        return {f"key_{i}": generate_random_json_value(depth + 1) for i in range(random.randint(0, 3))}
    elif val_type == 'list':
        return [generate_random_json_value(depth + 1) for _ in range(random.randint(0, 3))]
    elif val_type == 'int':
        return random.randint(-10000, 10000)
    elif val_type == 'string':
        return "".join(random.choices(string.ascii_letters + string.digits + " \t\n", k=random.randint(0, 20)))
    elif val_type == 'bool':
        return random.choice([True, False])
    else:
        return None

def generate_fuzz_inputs(n):
    random.seed(42)
    inputs = []
    for _ in range(n):
        choice = random.random()
        if choice < 0.3:
            # Valid JSON
            val = generate_random_json_value()
            inputs.append(json.dumps(val))
        elif choice < 0.6:
            # Malformed JSON (truncated or mutated)
            val = generate_random_json_value()
            s = json.dumps(val)
            if len(s) > 2:
                if random.random() < 0.5:
                    s = s[:random.randint(1, len(s)-1)]
                else:
                    idx = random.randint(0, len(s)-1)
                    s = s[:idx] + random.choice(string.printable) + s[idx+1:]
            inputs.append(s)
        else:
            # Unclosed objects with trailing commas
            val = generate_random_json_value()
            if not isinstance(val, dict):
                val = {"a": val}
            s = json.dumps(val)
            s = s[:-1] + ', "unclosed": '
            if random.random() < 0.5:
                s += '{"nested": 1, '
            inputs.append(s)

    return inputs

def test_parse_fuzz_exists():
    assert os.path.isfile(AGENT_PATH), f"Target script {AGENT_PATH} is missing."

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle script {ORACLE_PATH} is missing."

    inputs = generate_fuzz_inputs(NUM_TESTS)

    for i, inp in enumerate(inputs):
        inp_bytes = inp.encode('utf-8')

        # Run Oracle
        oracle_proc = subprocess.run(
            ["python3", ORACLE_PATH],
            input=inp_bytes,
            capture_output=True,
            timeout=TIMEOUT_SECS
        )
        oracle_out = oracle_proc.stdout.decode('utf-8', errors='replace').strip()
        oracle_err = oracle_proc.stderr.decode('utf-8', errors='replace').strip()
        oracle_code = oracle_proc.returncode

        # Run Agent
        try:
            agent_proc = subprocess.run(
                ["python3", AGENT_PATH],
                input=inp_bytes,
                capture_output=True,
                timeout=TIMEOUT_SECS
            )
            agent_out = agent_proc.stdout.decode('utf-8', errors='replace').strip()
            agent_err = agent_proc.stderr.decode('utf-8', errors='replace').strip()
            agent_code = agent_proc.returncode
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out (possible infinite loop/memory leak) on input:\n{inp!r}")

        assert agent_out == oracle_out, (
            f"Output mismatch on input {i}:\n"
            f"Input: {inp!r}\n"
            f"Oracle output: {oracle_out!r}\n"
            f"Agent output: {agent_out!r}\n"
            f"Oracle exit code: {oracle_code}, Agent exit code: {agent_code}"
        )