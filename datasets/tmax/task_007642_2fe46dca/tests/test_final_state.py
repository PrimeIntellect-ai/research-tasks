# test_final_state.py

import os
import json
import base64

def test_evaluate_go_exists():
    assert os.path.isfile("/home/user/evaluate.go"), "The Go program /home/user/evaluate.go does not exist."

def test_result_txt_correct():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"The result file {result_path} does not exist."

    # Recompute expected result dynamically based on current inputs
    b64_path = "/home/user/pipeline_data.b64"
    vars_path = "/home/user/vars.json"

    assert os.path.isfile(b64_path), f"Input file {b64_path} missing."
    assert os.path.isfile(vars_path), f"Input file {vars_path} missing."

    with open(b64_path, 'r') as f:
        encoded_expr = f.read().strip()

    expr = base64.b64decode(encoded_expr).decode('utf-8')

    with open(vars_path, 'r') as f:
        variables = json.load(f)

    stack = []
    tokens = expr.split()

    for token in tokens:
        if token in ['+', '-', '*', '/']:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                stack.append(a // b)
        else:
            if token in variables:
                stack.append(variables[token])
            else:
                stack.append(int(token))

    expected_result = str(stack[0])

    with open(result_path, 'r') as f:
        actual_result = f.read().strip()

    assert actual_result == expected_result, f"Expected result {expected_result}, but got {actual_result} in {result_path}."