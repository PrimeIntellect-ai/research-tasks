# test_final_state.py

import os
import re
import math
import pytest

def test_result_file_exists():
    assert os.path.isfile("/home/user/result.txt"), "Error: /home/user/result.txt not found."

def test_result_value_correct():
    with open('/home/user/result.txt', 'r') as f:
        content = f.read()

    match = re.search(r"Result:\s*(-?\d+\.\d+)", content)
    assert match is not None, "Error: /home/user/result.txt does not contain 'Result: <float>'."

    val = float(match.group(1))
    expected_val = -0.7596879128598213

    assert abs(val - expected_val) < 1e-5, f"Error: Output {val} does not match expected {expected_val} within tolerance."

def test_rust_code_fixes():
    main_rs_path = "/home/user/diagnostic/src/main.rs"
    assert os.path.isfile(main_rs_path), f"{main_rs_path} is missing."

    with open(main_rs_path, "r") as f:
        content = f.read()

    # Check that f32 has been upgraded to f64
    assert "f32" not in content, "Error: f32 is still present in main.rs. Must be upgraded to f64."
    assert "f64" in content, "Error: f64 is not used in main.rs."

    # Check that the termination condition uses 1e-12
    assert "1e-12" in content or "1E-12" in content or "0.000000000001" in content, "Error: The termination condition must use 1e-12."