# test_final_state.py

import os
import json
import sys
import importlib.util

def test_sparse_poly_fixed():
    """Verify that sparse_poly.py correctly implements polynomial multiplication."""
    file_path = "/home/user/sparse_poly_pr/sparse_poly.py"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    spec = importlib.util.spec_from_file_location("sparse_poly", file_path)
    sparse_poly = importlib.util.module_from_spec(spec)
    sys.modules["sparse_poly"] = sparse_poly
    spec.loader.exec_module(sparse_poly)

    SparsePolynomial = sparse_poly.SparsePolynomial

    # Test (2x^2 + 3) * (x + 4) = 2x^3 + 8x^2 + 3x + 12
    p1 = SparsePolynomial({2: 2, 0: 3})
    p2 = SparsePolynomial({1: 1, 0: 4})
    p3 = p1 * p2
    assert p3.coeffs == {3: 2, 2: 8, 1: 3, 0: 12}, "Multiplication logic is incorrect for basic polynomials."

    # Test (x + 1) * (x - 1) = x^2 - 1
    p4 = SparsePolynomial({1: 1, 0: 1})
    p5 = SparsePolynomial({1: 1, 0: -1})
    p6 = p4 * p5
    assert p6.coeffs == {2: 1, 0: -1}, "Multiplication logic failed to cancel out zero coefficients."

def test_test_suite_exists_and_contains_functions():
    """Verify that test_sparse_poly.py contains the required test functions."""
    file_path = "/home/user/sparse_poly_pr/test_sparse_poly.py"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, 'r') as f:
        content = f.read()

    assert "def test_mult_basic" in content, "Missing test_mult_basic function."
    assert "def test_mult_zero_cancellation" in content, "Missing test_mult_zero_cancellation function."
    assert "def test_mult_large_sparse" in content, "Missing test_mult_large_sparse function."

def test_run_tests_script():
    """Verify that run_tests.sh exists, is executable, and has correct contents."""
    file_path = "/home/user/sparse_poly_pr/run_tests.sh"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."
    assert os.access(file_path, os.X_OK), f"File {file_path} is not executable."

    with open(file_path, 'r') as f:
        content = f.read()

    assert "pytest" in content, "Script does not invoke pytest."
    assert "pytest-json-report" in content or "pytest_json_report" in content or "--json-report" in content, "Script does not use json-report."

def test_test_report_json():
    """Verify that test_report.json exists, is valid JSON, and shows 3 passed tests."""
    file_path = "/home/user/sparse_poly_pr/test_report.json"
    assert os.path.isfile(file_path), f"File {file_path} does not exist. Did the orchestration script run?"

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not valid JSON.")

    assert "summary" in data, "JSON report missing 'summary' key."
    assert data["summary"].get("passed", 0) >= 3, "Expected at least 3 passed tests in the JSON report."