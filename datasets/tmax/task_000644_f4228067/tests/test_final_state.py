# test_final_state.py

import os
import sys
import pytest

# Add the math_api directory to sys.path so we can import the modules
sys.path.insert(0, "/home/user/math_api")

def test_result_file():
    """Verify that result.txt exists and contains the correct rounded root."""
    result_path = "/home/user/result.txt"
    assert os.path.exists(result_path), f"{result_path} does not exist. Did you save the output?"

    with open(result_path, "r") as f:
        val = f.read().strip()

    assert val == "1.492043", f"Expected '1.492043' in result.txt, got '{val}'"

def test_decoder_fixed():
    """Verify that decoder.py correctly decodes a hex string to ascii after XORing bytes."""
    try:
        from decoder import decode_query
    except ImportError:
        pytest.fail("Could not import decode_query from decoder.py")

    test_hex = "12626e276c70227222726c7122726c7322727c622562732c22"
    expected = "P -10.0 0.0 3.0 1.0 | G 1.0"

    try:
        result = decode_query(test_hex)
    except Exception as e:
        pytest.fail(f"decode_query raised an exception: {e}")

    assert result == expected, f"Expected decode_query to return '{expected}', but got '{result}'"

def test_parser_fixed():
    """Verify that parser.py correctly handles negative signs and spaces."""
    try:
        from parser import parse_query
    except ImportError:
        pytest.fail("Could not import parse_query from parser.py")

    query_str = "P -10.0 0.0 3.0 1.0 | G 1.0"
    expected_coeffs = [-10.0, 0.0, 3.0, 1.0]
    expected_guess = 1.0

    try:
        coeffs, guess = parse_query(query_str)
    except Exception as e:
        pytest.fail(f"parse_query raised an exception: {e}")

    assert coeffs == expected_coeffs, f"Expected coefficients {expected_coeffs}, got {coeffs}"
    assert guess == expected_guess, f"Expected guess {expected_guess}, got {guess}"

def test_solver_fixed():
    """Verify that solver.py correctly computes the derivative and root."""
    try:
        from solver import evaluate_derivative, newton_root
    except ImportError:
        pytest.fail("Could not import evaluate_derivative and newton_root from solver.py")

    coeffs = [-10.0, 0.0, 3.0, 1.0]  # x^3 + 3x^2 - 10

    # Test derivative at x=1.0: f'(x) = 3x^2 + 6x => f'(1.0) = 9.0
    try:
        dfx = evaluate_derivative(coeffs, 1.0)
    except Exception as e:
        pytest.fail(f"evaluate_derivative raised an exception: {e}")

    assert abs(dfx - 9.0) < 1e-9, f"Expected derivative at x=1.0 to be 9.0, got {dfx}"

    # Test newton_root
    try:
        root = newton_root(coeffs, 1.0)
    except Exception as e:
        pytest.fail(f"newton_root raised an exception: {e}")

    expected_root = 1.492043
    assert abs(root - expected_root) < 1e-5, f"Expected root near {expected_root}, got {root}"