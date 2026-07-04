# test_final_state.py

import os
import random
import subprocess
import pytest

def generate_rpn_expr():
    # Simple generator for valid RPN expressions
    length = random.randint(3, 15)
    if length % 2 == 0:
        length += 1

    stack_depth = 0
    expr = []

    for i in range(length):
        if stack_depth >= 2 and (length - i) <= stack_depth - 1:
            # Must reduce stack
            op = random.choice(['+', '-', '*'])
            expr.append(op)
            stack_depth -= 1
        elif stack_depth < 2:
            # Must push
            if random.random() < 0.2:
                # semver
                expr.append(f"{random.randint(0,20)}.{random.randint(0,20)}.{random.randint(0,20)}")
            else:
                expr.append(str(random.randint(0, 1000)))
            stack_depth += 1
        else:
            # Push or pop
            if random.random() < 0.5:
                if random.random() < 0.2:
                    expr.append(f"{random.randint(0,20)}.{random.randint(0,20)}.{random.randint(0,20)}")
                else:
                    expr.append(str(random.randint(0, 1000)))
                stack_depth += 1
            else:
                op = random.choice(['+', '-', '*', 'VER_LT', 'VER_GT', 'VER_EQ'])
                expr.append(op)
                stack_depth -= 1

    while stack_depth > 1:
        op = random.choice(['+', '-', '*'])
        expr.append(op)
        stack_depth -= 1

    return " ".join(expr)

def test_fuzz_equivalence():
    oracle_path = "/opt/oracle/rpn_cli_reference"
    agent_path = "/app/rpn_cli"

    assert os.path.isfile(oracle_path), f"Oracle missing: {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent binary missing: {agent_path}"

    random.seed(42)

    for _ in range(1000):
        expr = generate_rpn_expr()

        oracle_proc = subprocess.run([oracle_path, expr], capture_output=True, text=True)
        agent_proc = subprocess.run([agent_path, expr], capture_output=True, text=True)

        # We only strictly compare if the oracle succeeded (some generated expressions might have type mismatches like semver + semver)
        if oracle_proc.returncode == 0:
            assert agent_proc.returncode == 0, f"Agent failed on input: {expr}\nOracle output: {oracle_proc.stdout}"
            assert oracle_proc.stdout.strip() == agent_proc.stdout.strip(), \
                f"Mismatch on input: {expr}\nOracle: {oracle_proc.stdout.strip()}\nAgent: {agent_proc.stdout.strip()}"

def test_nginx_config_fixed():
    with open("/app/nginx.conf", "r") as f:
        conf = f.read()
    assert "5000" in conf, "Nginx config missing port 5000 (legacy)"
    assert "5001" in conf, "Nginx config missing port 5001 (fast)"