# test_final_state.py

import os
import subprocess
import random
import math
import pytest

def generate_rpn():
    while True:
        num_ops = random.randint(1, 15)
        tokens = []
        stack = []

        ops_left = num_ops
        operands_left = num_ops + 1

        valid = True

        while ops_left > 0 or operands_left > 0:
            choices = []
            if operands_left > 0:
                choices.append('push')
            if ops_left > 0 and len(stack) >= 2:
                choices.append('op')

            if not choices:
                valid = False
                break

            choice = random.choice(choices)
            if choice == 'push':
                val = random.randint(-1000, 1000)
                tokens.append(str(val))
                stack.append(val)
                operands_left -= 1
            else:
                op = random.choice(['+', '-', '*', '/'])
                b = stack.pop()
                a = stack.pop()
                if op == '/':
                    if b == 0:
                        valid = False
                        break
                    res = math.trunc(a / b)
                elif op == '+':
                    res = a + b
                elif op == '-':
                    res = a - b
                elif op == '*':
                    res = a * b

                if not (-1000000000 <= res <= 1000000000):
                    valid = False
                    break

                stack.append(res)
                tokens.append(op)
                ops_left -= 1

        if valid and len(stack) == 1:
            return " ".join(tokens)

def test_files_exist():
    assert os.path.exists("/home/user/src/rpn_calc"), "rpn_calc executable was not built."
    assert os.access("/home/user/src/rpn_calc", os.X_OK), "rpn_calc is not executable."
    assert os.path.exists("/home/user/test.sh"), "test.sh script is missing."
    assert os.access("/home/user/test.sh", os.X_OK), "test.sh is not executable."

def test_fuzz_equivalence():
    oracle_path = "/app/rpn_oracle"
    agent_path = "/home/user/src/rpn_calc"

    assert os.path.exists(oracle_path), "Oracle missing."
    assert os.path.exists(agent_path), "Agent binary missing."

    random.seed(42)
    for _ in range(500):
        expr = generate_rpn()

        oracle_proc = subprocess.run([oracle_path, expr], capture_output=True, text=True)
        agent_proc = subprocess.run([agent_path, expr], capture_output=True, text=True)

        assert oracle_proc.returncode == agent_proc.returncode, f"Return code mismatch on input: '{expr}'\nOracle: {oracle_proc.returncode}\nAgent: {agent_proc.returncode}"

        if oracle_proc.returncode == 0:
            oracle_out = oracle_proc.stdout.strip()
            agent_out = agent_proc.stdout.strip()
            assert oracle_out == agent_out, f"Output mismatch on input: '{expr}'\nOracle: {oracle_out}\nAgent: {agent_out}"