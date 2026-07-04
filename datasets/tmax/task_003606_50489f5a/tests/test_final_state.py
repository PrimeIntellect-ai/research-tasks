# test_final_state.py

import os
import subprocess
import random
import string
import pytest

ORACLE_PATH = "/app/legacy_parser"
AGENT_PATH = "/home/user/parser"

def generate_input():
    num_commas = random.randint(0, 5)
    chars = string.ascii_letters + string.digits + " "
    parts = []
    for _ in range(num_commas + 1):
        length = random.randint(0, 20)
        parts.append("".join(random.choices(chars, k=length)))
    res = ",".join(parts)
    return res[:100]

def get_test_inputs():
    random.seed(42)
    inputs = [
        "",
        "   ",
        " , , , ",
        "prod,fr_FR.UTF-8,CET,4",
        "  prod  ,  fr_FR.UTF-8  ,  CET  ,  4  ",
        "dev, , , 0",
        "test,en_GB,GMT,-1",
        "stage, , , abc",
        "stage, , , 2.5",
        "a,b,c,d,e,f",
    ]
    for _ in range(1000 - len(inputs)):
        inputs.append(generate_input())
    return inputs

def test_fuzz_equivalence():
    assert os.path.exists(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent executable is not executable: {AGENT_PATH}"

    inputs = get_test_inputs()

    for test_input in inputs:
        oracle_proc = subprocess.run(
            [ORACLE_PATH, test_input],
            capture_output=True,
            text=True
        )

        agent_proc = subprocess.run(
            [AGENT_PATH, test_input],
            capture_output=True,
            text=True
        )

        assert oracle_proc.stdout == agent_proc.stdout, \
            f"Stdout mismatch on input {repr(test_input)}.\nOracle:\n{repr(oracle_proc.stdout)}\nAgent:\n{repr(agent_proc.stdout)}"