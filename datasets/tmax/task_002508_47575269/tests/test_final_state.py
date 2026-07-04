# test_final_state.py

import os
import pytest

def test_libcalc_so_exists():
    assert os.path.isfile("/home/user/workspace/libcalc.so"), "libcalc.so was not built in /home/user/workspace"

def test_evaluator_py_exists():
    assert os.path.isfile("/home/user/workspace/evaluator.py"), "evaluator.py is missing"

def test_results_txt_correct():
    results_path = "/home/user/workspace/results.txt"
    assert os.path.isfile(results_path), "results.txt is missing"

    with open(results_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected = ["15", "16", "42", "11"]
    assert lines == expected, f"results.txt content is incorrect. Expected {expected}, got {lines}"

def test_no_circular_dependency():
    util_path = "/home/user/workspace/go_calc/util/util.go"
    ops_path = "/home/user/workspace/go_calc/ops/ops.go"

    if os.path.isfile(util_path) and os.path.isfile(ops_path):
        with open(util_path, "r") as f:
            util_content = f.read()
        with open(ops_path, "r") as f:
            ops_content = f.read()

        util_imports_ops = '"go_calc/ops"' in util_content
        ops_imports_util = '"go_calc/util"' in ops_content

        assert not (util_imports_ops and ops_imports_util), "Circular dependency between util and ops still exists"