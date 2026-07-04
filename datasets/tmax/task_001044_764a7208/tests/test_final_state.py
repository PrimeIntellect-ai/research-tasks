# test_final_state.py
import os
from decimal import Decimal

def test_final_result_accuracy():
    result_path = "/home/user/final_result.txt"
    assert os.path.isfile(result_path), f"Result file {result_path} not found. Did you run the test_flow.py script?"

    with open(result_path, "r") as f:
        content = f.read().strip()

    try:
        actual = Decimal(content)
    except Exception as e:
        assert False, f"Could not parse the content of {result_path} ('{content}') as a Decimal: {e}"

    expected = Decimal("42000.0")
    error = abs(actual - expected)
    threshold = Decimal("1e-8")

    assert error <= threshold, (
        f"Absolute error {error} exceeds the maximum allowed threshold of {threshold}. "
        f"Actual value: {actual}, Expected value: {expected}. "
        "Check your concurrency logic and floating-point precision handling."
    )