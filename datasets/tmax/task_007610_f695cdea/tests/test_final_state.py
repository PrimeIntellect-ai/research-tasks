# test_final_state.py
import os
import math

def test_convergence_order_file():
    filepath = "/home/user/convergence_order.txt"
    assert os.path.isfile(filepath), f"Missing output file: {filepath}"

    with open(filepath, 'r') as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        assert False, f"Content of {filepath} is not a valid float: '{content}'"

    expected = 2.052
    assert math.isclose(val, expected, abs_tol=0.005), f"Expected value close to {expected}, but got {val}"