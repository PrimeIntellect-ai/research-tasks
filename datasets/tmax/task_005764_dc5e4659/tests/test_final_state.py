# test_final_state.py

import os
import json
import math
import pytest

def test_bad_txn_txt():
    path = '/home/user/pipeline/bad_txn.txt'
    assert os.path.isfile(path), f"{path} is missing. The transaction ID was not extracted."

    with open(path, 'r') as f:
        content = f.read().strip()

    assert content == "TXN-A839F7X2", f"bad_txn.txt contains '{content}', expected exactly 'TXN-A839F7X2'."

def test_calc_c_fixes():
    path = '/home/user/pipeline/calc.c'
    assert os.path.isfile(path), f"{path} is missing."

    with open(path, 'r') as f:
        content = f.read()

    # Check precision fix
    assert "float sum" not in content, "calc.c still contains 'float sum'. The precision loss bug was not fixed."
    assert "double sum" in content, "calc.c does not contain 'double sum'. The accumulator should be upgraded to double."

    # Check off-by-one fix
    assert "i <= len" not in content, "calc.c still contains the off-by-one error 'i <= len'."
    assert "i < len" in content, "calc.c does not contain the fixed loop bounds 'i < len'."

def test_results_json():
    path = '/home/user/pipeline/results.json'
    assert os.path.isfile(path), f"{path} is missing. The script was not run successfully after compilation."

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{path} does not contain valid JSON.")

    assert "status" in data and data["status"] == "success", "results.json status is missing or not 'success'."
    assert "final_sum" in data, "results.json is missing 'final_sum'."

    # The expected sum is derived from:
    # chunk = 100000000.0 + 0.0000001 + 0.0000002 + 0.0000003 = 100000000.0000006
    # expected_sum = chunk * 10000 = 1000000000000.006
    expected_sum = 1000000000000.006
    actual_sum = data["final_sum"]

    assert math.isclose(actual_sum, expected_sum, rel_tol=1e-9), \
        f"final_sum {actual_sum} is not close to expected {expected_sum}. This indicates the bugs in calc.c were not properly fixed before running."