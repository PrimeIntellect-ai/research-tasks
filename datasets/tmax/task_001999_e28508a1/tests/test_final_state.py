# test_final_state.py

import os
import re
import pytest

def test_extract_math_script_exists():
    script_path = "/home/user/extract_math.py"
    assert os.path.exists(script_path), f"Expected script missing at {script_path}"
    assert os.path.isfile(script_path), f"Path {script_path} is not a file"

def test_ci_pipeline_script_exists():
    script_path = "/home/user/ci_pipeline.sh"
    assert os.path.exists(script_path), f"Expected script missing at {script_path}"
    assert os.path.isfile(script_path), f"Path {script_path} is not a file"

def test_trajectory_constants_accuracy():
    constants_path = "/home/user/sim_engine/src/trajectory_constants.rs"
    assert os.path.exists(constants_path), f"Generated file missing at {constants_path}"

    with open(constants_path, 'r') as f:
        content = f.read()

    a_match = re.search(r'COEFF_A:\s*f64\s*=\s*([-\d\.e]+);', content)
    b_match = re.search(r'COEFF_B:\s*f64\s*=\s*([-\d\.e]+);', content)
    c_match = re.search(r'COEFF_C:\s*f64\s*=\s*([-\d\.e]+);', content)

    assert a_match, "Could not find COEFF_A in trajectory_constants.rs"
    assert b_match, "Could not find COEFF_B in trajectory_constants.rs"
    assert c_match, "Could not find COEFF_C in trajectory_constants.rs"

    A_pred = float(a_match.group(1))
    B_pred = float(b_match.group(1))
    C_pred = float(c_match.group(1))

    A_true, B_true, C_true = 0.002, -1.2, 200.0

    err_a = abs((A_pred - A_true) / A_true)
    err_b = abs((B_pred - B_true) / B_true)
    err_c = abs((C_pred - C_true) / C_true)

    max_err = max(err_a, err_b, err_c)
    threshold = 0.05

    assert max_err <= threshold, (
        f"Maximum relative error {max_err:.4f} exceeds threshold {threshold}. "
        f"Predictions: A={A_pred}, B={B_pred}, C={C_pred}. "
        f"Expected: A={A_true}, B={B_true}, C={C_true}."
    )