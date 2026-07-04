# test_final_state.py

import os
import random
import subprocess
import pytest
from pathlib import Path

ORACLE_PATH = "/app/version_evaluator"
AGENT_PATH = "/home/user/evaluator.py"
NUM_ITERATIONS = 1000

def generate_valid_semver():
    major = random.randint(0, 5)
    minor = random.randint(0, 10)
    patch = random.randint(0, 20)
    base = f"{major}.{minor}.{patch}"
    if random.random() < 0.3:
        base += f"-{random.choice(['alpha', 'beta', 'rc'])}{random.randint(1, 5)}"
    if random.random() < 0.2:
        base += f"+build{random.randint(100, 999)}"
    return base

def generate_simple_constraint():
    op = random.choice(['=', '==', '!=', '>', '<', '>=', '<='])
    return f"{op}{generate_valid_semver()}"

def generate_complex_constraint(depth=0):
    if depth > 2 or random.random() < 0.4:
        return generate_simple_constraint()

    op = random.choice(['&&', '||'])
    left = generate_complex_constraint(depth + 1)
    right = generate_complex_constraint(depth + 1)

    if random.random() < 0.3:
        return f"({left} {op} {right})"
    else:
        return f"{left} {op} {right}"

def generate_invalid_input():
    choices = [
        "1.2", # missing patch
        "=>1.0.0", # invalid op
        "1.0.0-", # invalid prerelease
        "(>1.0.0", # unbalanced
        "garbage string",
        "==1.0.0 && || 2.0.0",
        ">1.x.0"
    ]
    return random.choice(choices)

def get_fuzz_case():
    r = random.random()
    if r < 0.4:
        # 40% valid complex expressions
        constraint = generate_complex_constraint()
        target = generate_valid_semver()
    elif r < 0.7:
        # 30% valid simple expressions
        constraint = generate_simple_constraint()
        target = generate_valid_semver()
    else:
        # 30% invalid inputs
        if random.random() < 0.5:
            constraint = generate_invalid_input()
            target = generate_valid_semver()
        else:
            constraint = generate_simple_constraint()
            target = generate_invalid_input()
    return constraint, target

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
        return result.stdout.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "TIMEOUT", -1

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle not executable at {ORACLE_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Agent script missing at {AGENT_PATH}"

    random.seed(42)

    for i in range(NUM_ITERATIONS):
        constraint, target = get_fuzz_case()

        oracle_cmd = [ORACLE_PATH, constraint, target]
        agent_cmd = ["python3", AGENT_PATH, constraint, target]

        oracle_out, oracle_code = run_cmd(oracle_cmd)
        agent_out, agent_code = run_cmd(agent_cmd)

        assert agent_code == oracle_code, (
            f"Exit code mismatch on iteration {i+1}.\n"
            f"Constraint: {constraint}\n"
            f"Target: {target}\n"
            f"Oracle code: {oracle_code}\n"
            f"Agent code: {agent_code}\n"
            f"Oracle out: {oracle_out}\n"
            f"Agent out: {agent_out}"
        )

        assert agent_out == oracle_out, (
            f"Stdout mismatch on iteration {i+1}.\n"
            f"Constraint: {constraint}\n"
            f"Target: {target}\n"
            f"Oracle out: {oracle_out}\n"
            f"Agent out: {agent_out}"
        )