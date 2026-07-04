# test_final_state.py
import os
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/token_checker"
AGENT_PATH = "/home/user/my_token_checker"

def generate_random_string(length):
    chars = string.ascii_letters + string.digits + ";= -"
    return ''.join(random.choice(chars) for _ in range(length))

def generate_valid_cookie():
    prefix_len = random.randint(0, 20)
    prefix = generate_random_string(prefix_len)

    # Valid SessionId requires even number of hex characters
    hex_len = random.randint(1, 20) * 2
    hex_chars = ''.join(random.choice(string.hexdigits) for _ in range(hex_len))

    suffix_len = random.randint(0, 20)
    suffix = generate_random_string(suffix_len)

    return f"{prefix}SessionId={hex_chars};{suffix}"

def generate_malformed_cookie():
    case = random.randint(0, 2)
    if case == 0:
        # Missing SessionId entirely
        return generate_random_string(random.randint(5, 50))
    elif case == 1:
        # Odd number of hex characters
        prefix = generate_random_string(random.randint(0, 20))
        hex_len = random.randint(0, 20) * 2 + 1
        hex_chars = ''.join(random.choice(string.hexdigits) for _ in range(hex_len))
        return f"{prefix}SessionId={hex_chars};"
    else:
        # Invalid characters in SessionId
        prefix = generate_random_string(random.randint(0, 20))
        hex_len = random.randint(1, 20) * 2
        hex_chars = ''.join(random.choice(string.hexdigits) for _ in range(hex_len - 1)) + "G"
        return f"{prefix}SessionId={hex_chars};"

def test_fuzz_equivalence():
    assert os.path.isfile(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary is not executable: {AGENT_PATH}"

    random.seed(1337)
    inputs = []

    # 250 validly formatted cookies
    for _ in range(250):
        inputs.append(generate_valid_cookie())

    # 250 malformed cookies
    for _ in range(250):
        inputs.append(generate_malformed_cookie())

    # Edge cases
    inputs.append(None) # Represents no arguments
    inputs.append("")   # Empty string argument

    for inp in inputs:
        if inp is None:
            oracle_cmd = [ORACLE_PATH]
            agent_cmd = [AGENT_PATH]
            display_inp = "<NO ARGUMENTS>"
        else:
            oracle_cmd = [ORACLE_PATH, inp]
            agent_cmd = [AGENT_PATH, inp]
            display_inp = repr(inp)

        oracle_res = subprocess.run(oracle_cmd, capture_output=True)
        agent_res = subprocess.run(agent_cmd, capture_output=True)

        assert oracle_res.returncode == agent_res.returncode, \
            f"Exit code mismatch for input {display_inp}.\nOracle: {oracle_res.returncode}\nAgent: {agent_res.returncode}"

        assert oracle_res.stdout == agent_res.stdout, \
            f"Stdout mismatch for input {display_inp}.\nOracle: {oracle_res.stdout!r}\nAgent: {agent_res.stdout!r}"

        assert oracle_res.stderr == agent_res.stderr, \
            f"Stderr mismatch for input {display_inp}.\nOracle: {oracle_res.stderr!r}\nAgent: {agent_res.stderr!r}"