# test_final_state.py

import os
import subprocess
import random
import string
import pytest

def test_vendored_regex_fixed():
    path = "/app/vendor/regex-1.10.4/Cargo.toml"
    assert os.path.isfile(path), f"Cargo.toml is missing at {path}"

    with open(path, "r") as f:
        content = f.read()

    assert 'name = "regex"' in content and 'name = "regex-broken"' not in content, \
        f"Cargo.toml at {path} was not properly fixed to 'name = \"regex\"'"

def test_agent_binary_exists():
    path = "/home/user/audit_tool/target/release/sanitizer"
    assert os.path.isfile(path), f"Agent binary is missing at {path}"
    assert os.access(path, os.X_OK), f"Agent binary at {path} is not executable"

def generate_fuzz_inputs(n=1000, seed=42):
    random.seed(seed)
    chars = string.ascii_letters + string.digits + string.punctuation + " "
    inputs = []

    for _ in range(n):
        length = random.randint(10, 256)
        s = "".join(random.choice(chars) for _ in range(length))

        # Deliberate insertions
        if random.random() < 0.3:
            insert_pos = random.randint(0, len(s))
            s = s[:insert_pos] + "CWE-79" + s[insert_pos:]
        if random.random() < 0.3:
            insert_pos = random.randint(0, len(s))
            s = s[:insert_pos] + "CWE-89" + s[insert_pos:]
        if random.random() < 0.3:
            insert_pos = random.randint(0, len(s))
            digits = "".join(random.choice(string.digits) for _ in range(random.randint(1, 5)))
            s = s[:insert_pos] + f"pin={digits}" + s[insert_pos:]

        inputs.append(s)
    return inputs

def test_fuzz_equivalence():
    oracle_path = "/app/oracle/audit_sanitizer"
    agent_path = "/home/user/audit_tool/target/release/sanitizer"

    assert os.path.isfile(oracle_path), f"Oracle binary missing at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent binary missing at {agent_path}"

    inputs = generate_fuzz_inputs(n=1000)

    # Run both processes
    oracle_proc = subprocess.Popen([oracle_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    agent_proc = subprocess.Popen([agent_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # We can pass all inputs joined by newline
    input_text = "\n".join(inputs) + "\n"

    oracle_out, _ = oracle_proc.communicate(input=input_text)
    agent_out, _ = agent_proc.communicate(input=input_text)

    oracle_lines = oracle_out.splitlines()
    agent_lines = agent_out.splitlines()

    assert len(oracle_lines) == len(inputs), "Oracle did not produce the expected number of output lines"
    assert len(agent_lines) == len(inputs), "Agent did not produce the expected number of output lines"

    for i, (inp, oracle_line, agent_line) in enumerate(zip(inputs, oracle_lines, agent_lines)):
        assert oracle_line == agent_line, (
            f"Mismatch on input {i}:\n"
            f"Input: {inp!r}\n"
            f"Oracle output: {oracle_line!r}\n"
            f"Agent output:  {agent_line!r}"
        )