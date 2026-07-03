# test_final_state.py
import json
import os
import random
import subprocess
import string
import pytest

ORACLE_PATH = "/app/legacy_calc"
AGENT_PATH = "/home/user/calc"
N_TESTS = 2000

def generate_invalid_json():
    choices = [
        "",
        "{",
        "{\"expression\": \"1 + 1\"",
        "not a json",
        "[1, 2, 3]",
        "{\"expression\": \"1 + 1\", \"context\": {",
    ]
    return random.choice(choices)

def generate_missing_keys():
    choices = [
        {"expression": "1 + 1"},
        {"context": {"a": 1}},
        {},
        {"expr": "1 + 1", "ctx": {}},
    ]
    return json.dumps(choices)

def generate_valid_expression(depth=0, force_div_zero=False):
    if depth > 3:
        # Leaf node
        if force_div_zero:
            return "0", []
        if random.random() < 0.5:
            val = str(random.randint(0, 100))
            return val, []
        else:
            var = random.choice(string.ascii_lowercase)
            return var, [var]

    op = random.choice(["+", "-", "*", "/"])
    if force_div_zero and random.random() < 0.5:
        op = "/"

    left, left_vars = generate_valid_expression(depth + 1)

    if op == "/":
        if force_div_zero:
            right, right_vars = generate_valid_expression(depth + 1, force_div_zero=True)
            if right != "0":
                right = "0"
        else:
            right, right_vars = generate_valid_expression(depth + 1)
            # Avoid literal 0
            if right == "0":
                right = "1"
    else:
        right, right_vars = generate_valid_expression(depth + 1, force_div_zero)

    expr = f"{left} {op} {right}"
    if random.random() < 0.3:
        expr = f"({expr})"

    return expr, left_vars + right_vars

def format_expression(expr):
    # Randomize spaces
    res = ""
    for char in expr:
        if char in "+-*/()":
            res += " " * random.randint(0, 2) + char + " " * random.randint(0, 2)
        else:
            res += char
    # collapse multiple spaces
    return " ".join(res.split())

def generate_test_cases():
    random.seed(42)
    cases = []

    # 10% invalid JSON
    for _ in range(int(N_TESTS * 0.1)):
        cases.append(generate_invalid_json())

    # 10% missing keys
    for _ in range(int(N_TESTS * 0.1)):
        cases.append(generate_missing_keys())

    # 80% valid JSON structure
    valid_count = int(N_TESTS * 0.8)

    # 20% syntax errors (25% of valid)
    for _ in range(int(valid_count * 0.25)):
        expr, vars_ = generate_valid_expression()
        # Corrupt it
        corruption = random.choice([
            lambda e: e + " +",
            lambda e: "(" + e,
            lambda e: e + ")",
            lambda e: e.replace("+", "++"),
            lambda e: e + " invalid",
            lambda e: "!" + e
        ])
        cases.append(json.dumps({
            "expression": corruption(expr),
            "context": {v: random.randint(0, 100) for v in vars_}
        }))

    # 10% div by zero (12.5% of valid)
    for _ in range(int(valid_count * 0.125)):
        expr, vars_ = generate_valid_expression(force_div_zero=True)
        # ensure there is a / 0
        if "/ 0" not in expr:
            expr += " / 0"
        cases.append(json.dumps({
            "expression": expr,
            "context": {v: random.randint(0, 100) for v in vars_}
        }))

    # 10% undefined variables (12.5% of valid)
    for _ in range(int(valid_count * 0.125)):
        expr, vars_ = generate_valid_expression()
        if not vars_:
            expr += " + undefined_var"
            vars_.append("undefined_var")
        ctx = {v: random.randint(0, 100) for v in vars_}
        # Remove one
        if vars_:
            ctx.pop(vars_[0], None)
        cases.append(json.dumps({
            "expression": expr,
            "context": ctx
        }))

    # 40% valid expressions (50% of valid)
    for _ in range(int(valid_count * 0.5)):
        expr, vars_ = generate_valid_expression()
        cases.append(json.dumps({
            "expression": format_expression(expr),
            "context": {v: random.randint(1, 100) for v in vars_}
        }))

    random.shuffle(cases)
    return cases

def run_process(executable, input_data):
    try:
        result = subprocess.run(
            [executable],
            input=input_data.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=1
        )
        return result.stdout.decode('utf-8')
    except subprocess.TimeoutExpired:
        return "<TIMEOUT>"
    except Exception as e:
        return f"<ERROR: {e}>"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Agent executable missing at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent executable {AGENT_PATH} is not executable"

    test_cases = generate_test_cases()

    for i, case in enumerate(test_cases):
        oracle_out = run_process(ORACLE_PATH, case)
        agent_out = run_process(AGENT_PATH, case)

        assert oracle_out == agent_out, (
            f"Mismatch on test case {i+1}:\n"
            f"Input: {case}\n"
            f"Oracle output: {repr(oracle_out)}\n"
            f"Agent output:  {repr(agent_out)}"
        )