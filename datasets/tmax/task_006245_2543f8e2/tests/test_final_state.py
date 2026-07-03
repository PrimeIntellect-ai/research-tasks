# test_final_state.py

import os
import re
import pytest

def compute_expected_output(input_path):
    results = []
    with open(input_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Parse DEG, COEFFS, X
            deg_match = re.search(r'DEG:\s*(\d+)', line)
            coeffs_match = re.search(r'COEFFS:\s*([^|]+)', line)
            x_match = re.search(r'X:\s*([-\d\.]+)', line)

            if not (deg_match and coeffs_match and x_match):
                continue

            degree = int(deg_match.group(1))
            coeffs_str = coeffs_match.group(1).strip()
            x = float(x_match.group(1))

            coeffs = [float(c.strip()) for c in coeffs_str.split(',')]

            # Evaluate polynomial
            res = 0.0
            for i in range(min(degree + 1, len(coeffs))):
                res += coeffs[i] * (x ** i)

            results.append(res)
    return results

def test_output_log_exists_and_correct():
    input_path = "/home/user/poly_service/input.txt"
    output_path = "/home/user/poly_service/output.log"

    assert os.path.exists(input_path), f"Input file missing: {input_path}"
    assert os.path.exists(output_path), f"Output log missing: {output_path}"

    expected_results = compute_expected_output(input_path)

    with open(output_path, 'r') as f:
        output_lines = [line.strip() for line in f if line.strip()]

    assert len(output_lines) == len(expected_results), "Number of output lines does not match number of input lines"

    for i, (out_val, exp_val) in enumerate(zip(output_lines, expected_results)):
        try:
            out_float = float(out_val)
        except ValueError:
            pytest.fail(f"Output line {i+1} is not a valid float: {out_val}")

        assert abs(out_float - exp_val) < 1e-6, f"Line {i+1} mismatch: expected {exp_val}, got {out_float}"

def test_binary_exists_and_executable():
    binary_path = "/home/user/poly_service/poly_eval"
    assert os.path.isfile(binary_path), "Compiled binary 'poly_eval' is missing"
    assert os.access(binary_path, os.X_OK), "Compiled binary 'poly_eval' is not executable"

def test_makefile_fixed():
    makefile_path = "/home/user/poly_service/Makefile"
    assert os.path.exists(makefile_path), "Makefile is missing"

    with open(makefile_path, 'r') as f:
        content = f.read()

    # Check if libfastmath.a or fastmath.o is included in the compilation step for poly_eval
    # The original bug was missing libfastmath.a in the g++ -o poly_eval ... line
    assert re.search(r'g\+\+.*-o\s+poly_eval.*(libfastmath\.a|fastmath\.o|fastmath\.cpp)', content), "Makefile does not link fastmath correctly"

def test_poly_eval_cpp_fixes():
    cpp_path = "/home/user/poly_service/poly_eval.cpp"
    assert os.path.exists(cpp_path), "poly_eval.cpp is missing"

    with open(cpp_path, 'r') as f:
        content = f.read()

    # Check for memory leak fix
    assert "delete[]" in content or "std::vector" in content or "unique_ptr" in content, "Memory leak not fixed (missing delete[] or smart pointer/vector)"

    # Check for degree + 1 allocation fix
    assert "degree + 1" in content or "degree+1" in content or "std::vector" in content, "Array allocation size not fixed (should be degree + 1)"