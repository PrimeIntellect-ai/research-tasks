# test_final_state.py

import os
import json
import pytest

def test_shared_library_built():
    so_path = '/home/user/math_system/libeval.so'
    assert os.path.isfile(so_path), f"Shared library {so_path} was not built."

    # Check if it's an ELF shared object
    with open(so_path, 'rb') as f:
        header = f.read(16)
    assert header.startswith(b'\x7fELF'), f"{so_path} is not a valid ELF file."
    # e_type is at offset 16
    with open(so_path, 'rb') as f:
        f.seek(16)
        e_type = int.from_bytes(f.read(2), byteorder='little')
    # ET_DYN is 3 (Shared object file)
    assert e_type == 3, f"{so_path} is not compiled as a shared library (missing -shared or -fPIC)."

def test_eval_c_updated():
    eval_c_path = '/home/user/math_system/eval.c'
    assert os.path.isfile(eval_c_path), f"{eval_c_path} is missing."
    with open(eval_c_path, 'r') as f:
        content = f.read()
    assert 'OP_DIV' in content, "eval.c is missing OP_DIV."
    assert 'OP_POW' in content, "eval.c is missing OP_POW."
    assert 'pow(' in content or 'pow (' in content, "eval.c does not seem to use the pow() function for OP_POW."

def test_results_json_correct():
    formulas_path = '/home/user/math_system/formulas.json'
    results_path = '/home/user/math_system/results.json'

    assert os.path.isfile(formulas_path), f"{formulas_path} is missing."
    assert os.path.isfile(results_path), f"The output file {results_path} was not created."

    with open(formulas_path, 'r') as f:
        formulas = json.load(f)

    def eval_expr(expr):
        op = expr["op"]
        if op == "val":
            return float(expr["value"])

        left = eval_expr(expr["left"])
        right = eval_expr(expr["right"])

        if op == "add":
            return left + right
        elif op == "sub":
            return left - right
        elif op == "mul":
            return left * right
        elif op == "div":
            return 0.0 if right == 0.0 else left / right
        elif op == "pow":
            return left ** right
        return 0.0

    expected_results = {}
    for item in formulas:
        expected_results[item["id"]] = eval_expr(item["expr"])

    with open(results_path, 'r') as f:
        try:
            actual_results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{results_path} does not contain valid JSON.")

    assert isinstance(actual_results, dict), f"{results_path} should contain a JSON object (dictionary)."

    for eq_id, expected_val in expected_results.items():
        assert eq_id in actual_results, f"Equation ID '{eq_id}' is missing from {results_path}."
        actual_val = actual_results[eq_id]
        assert isinstance(actual_val, (int, float)), f"Result for '{eq_id}' should be a number."
        assert abs(actual_val - expected_val) < 1e-6, f"Incorrect result for '{eq_id}'. Expected {expected_val}, got {actual_val}."